import os
import re
import logging
from aiohttp import web
from payme_api import PaymeAPI
from click_api import ClickAPI

# Loglarni sozlash
logger = logging.getLogger(__name__)

# Same sanitization as main.py — must stay in sync
WEBHOOK_SECRET = re.sub(r"[^A-Za-z0-9_\-]", "", os.getenv("WEBHOOK_SECRET", ""))


async def create_web_app(bot=None, dp=None, webhook_path=None):
    """Mini App, Payme, Click va Webhook uchun aiohttp web ilovasini yaratish"""
    # database moduli - circular import xavfi yo'q (singleton)
    from database import db

    app = web.Application()
    # Bot va Dispatcher'ni app state'ga saqlaymiz (circular import o'rniga)
    app['bot'] = bot
    app['dp'] = dp

    port = int(os.getenv('PORT', 8080))
    miniapp_path = os.path.join(os.path.dirname(__file__), 'miniapp')

    # 1. ROOT HANDLER (Avtomatik yo'naltirish)
    async def root_handler(request):
        return web.HTTPFound('/miniapp/')

    # 2. FAVICON HANDLER — 404 loglarini to'xtatadi
    async def favicon_handler(request):
        return web.Response(status=204)

    # 3. HEALTH CHECK
    async def health_check(request):
        return web.json_response({'status': 'ok', 'server': 'CaravanTranzit'})

    # 4. MINI APP INDEX HANDLER
    async def miniapp_index(request):
        index_path = os.path.join(miniapp_path, 'index.html')
        if os.path.exists(index_path):
            return web.FileResponse(index_path)
        logger.error(f"❌ Mini App topilmadi: {index_path}")
        return web.Response(text='Mini App topilmadi', status=404)

    # 5. MINI APP API SUBMIT — asosiy tuzatmalar bu yerda
    async def miniapp_api_submit(request):
        # JSON parse xatosini ushlaymiz
        try:
            data = await request.json()
        except Exception:
            return web.json_response(
                {'success': False, 'error': 'Invalid JSON body'}, status=400
            )

        # --- KIRITISH TEKSHIRUVI (Input Validation / Kiberxavfsizlik) ---
        user_id_raw = data.get('user_id')
        service = str(data.get('service_type', '')).strip().upper()
        vehicle = str(data.get('vehicle_number', '')).strip()

        if not user_id_raw:
            return web.json_response(
                {'success': False, 'error': 'user_id is required'}, status=400
            )
        if service not in ('EPI', 'MB', 'EP', 'KGD'):
            return web.json_response(
                {'success': False, 'error': 'Invalid service_type'}, status=400
            )
        if not vehicle or len(vehicle) < 3:
            return web.json_response(
                {'success': False, 'error': 'vehicle_number must be at least 3 chars'}, status=400
            )

        try:
            user_id = int(user_id_raw)
        except (ValueError, TypeError):
            return web.json_response(
                {'success': False, 'error': 'user_id must be an integer'}, status=400
            )

        # Toza satrlar (XSS / injection oldini olish)
        user_name = str(data.get('user_name', 'Mini App User'))[:100]
        language = str(data.get('language', 'uz'))[:10]
        border_post = str(data.get('border_post', 'Noma\'lum'))[:150]
        destination = str(data.get('destination', 'Noma\'lum'))[:150]

        random_suffix = os.urandom(2).hex().upper()
        app_code = f"{service}-2026-{random_suffix}"

        logger.info(f"📩 Yangi ariza: {app_code} (User: {user_id})")

        try:
            # Foydalanuvchi mavjudligini ta'minlaymiz.
            # Bu FK (foreign key) xatosini oldini oladi:
            # applications.user_id → users.telegram_id
            await db.ensure_user_from_miniapp(user_id, user_name, language)

            # Ma'lumotlar bazasiga saqlash (parameterized query — SQL injection yo'q)
            await db.create_application(
                app_code=app_code,
                user_id=user_id,
                app_type=service,
                car_number=vehicle,
                metadata=data
            )
        except Exception as e:
            logger.error(f"❌ Baza xatosi: {e}")
            return web.json_response(
                {'success': False, 'error': 'Database error'}, status=500
            )

        # 📢 Admin guruhga xabar yuborish
        # bot'ni app state'dan olamiz — circular import yo'q
        bot_instance = request.app.get('bot')
        admin_group_id_str = os.getenv("ADMIN_GROUP_ID")

        if bot_instance and admin_group_id_str:
            try:
                admin_group_id = int(admin_group_id_str)
                msg = (
                    f"🆕 **Yangi ariza kelib tushdi!**\n\n"
                    f"🆔 **Kod:** `{app_code}`\n"
                    f"🚛 **Mashina:** `{vehicle}`\n"
                    f"🏢 **Post:** {border_post}\n"
                    f"📍 **Manzil:** {destination}\n"
                    f"👤 **Foydalanuvchi:** {user_name} (ID: `{user_id}`)"
                )
                await bot_instance.send_message(
                    chat_id=admin_group_id, text=msg, parse_mode="Markdown"
                )
            except Exception as e:
                logger.error(f"❌ Admin guruhga xabar yuborishda xato: {e}")

        return web.json_response({'success': True, 'app_code': app_code})

    # 6. TELEGRAM WEBHOOK HANDLER (Webhook rejimi uchun)
    async def telegram_webhook(request):
        from aiogram.types import Update

        # Secret token tekshiruvi (Man-in-the-middle oldini olish)
        if WEBHOOK_SECRET:
            header_token = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
            if header_token != WEBHOOK_SECRET:
                logger.warning("⚠️ Webhook: noto'g'ri secret token!")
                return web.Response(status=403)

        bot_instance = request.app.get('bot')
        dp_instance = request.app.get('dp')

        if not bot_instance or not dp_instance:
            logger.error("❌ Webhook: bot yoki dp app state'da yo'q!")
            return web.Response(status=500)

        try:
            data = await request.json()
            # aiogram 3.x pydantic v2 uslubi
            try:
                update = Update.model_validate(data)
            except AttributeError:
                update = Update(**data)  # pydantic v1 fallback
            await dp_instance.feed_update(bot_instance, update)
        except Exception as e:
            logger.error(f"❌ Webhook update xatosi: {e}")

        # Telegram 200 kutadi — har doim 200 qaytaramiz
        return web.Response(status=200)

    # --- ROUTES (YO'NALISHLAR) ---
    app.router.add_get('/', root_handler)
    app.router.add_get('/favicon.ico', favicon_handler)  # 404 loglarini to'xtatadi
    app.router.add_get('/health', health_check)
    app.router.add_get('/miniapp', miniapp_index)
    app.router.add_get('/miniapp/', miniapp_index)

    # API yo'nalishlari
    app.router.add_post('/api/applications', miniapp_api_submit)
    app.router.add_post('/api/payme', PaymeAPI.handle_request)
    app.router.add_post('/api/click', ClickAPI.handle_request)

    # Webhook yo'nalishi (faqat production webhook rejimida)
    if dp and webhook_path:
        app.router.add_post(webhook_path, telegram_webhook)
        logger.info(f"🔗 Webhook yo'nalishi qo'shildi: {webhook_path}")

    # Statik fayllar (CSS, JS, rasmlar)
    if os.path.exists(miniapp_path):
        app.router.add_static('/miniapp/', miniapp_path, name='miniapp_static')

    logger.info(f"✅ Web server {port}-portda muvaffaqiyatli sozlandi.")
    return app, port


async def start_web_server(bot=None, dp=None, webhook_path=None):
    """Railway muhitida serverni ishga tushirish"""
    app, port = await create_web_app(bot=bot, dp=dp, webhook_path=webhook_path)
    runner = web.AppRunner(app)
    await runner.setup()

    # Railway tashqi ulanish uchun 0.0.0.0 talab qiladi
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

    logger.info(f"🌐 Web server faol: http://0.0.0.0:{port}")
    return runner
