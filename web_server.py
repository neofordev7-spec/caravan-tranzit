import os
import logging
import hashlib
from aiohttp import web
from payme_api import PaymeAPI
from click_api import ClickAPI

# Loglarni sozlash
logger = logging.getLogger(__name__)

async def create_web_app():
    """Mini App, Payme va Click uchun aiohttp web ilovasini yaratish"""
    app = web.Application()

    port = int(os.getenv('PORT', 8080))
    # Mini App fayllari joylashgan papka manzili
    miniapp_path = os.path.join(os.path.dirname(__file__), 'miniapp')

    # 1. ROOT HANDLER (Avtomatik yo'naltirish)
    async def root_handler(request):
        # Foydalanuvchini / dan /miniapp/ ga yo'naltiramiz
        return web.HTTPFound('/miniapp/')

    # 2. HEALTH CHECK
    async def health_check(request):
        return web.json_response({'status': 'ok', 'server': 'CaravanTranzit'})

    # 3. MINI APP INDEX HANDLER
    async def miniapp_index(request):
        index_path = os.path.join(miniapp_path, 'index.html')
        if os.path.exists(index_path):
            return web.FileResponse(index_path)
        else:
            logger.error(f"❌ Mini App topilmadi: {index_path}")
            return web.Response(text='Mini App topilmadi', status=404)

    # 4. 🚀 MINI APP API SUBMIT (Baza va Admin xabarnomasi bilan)
    async def miniapp_api_submit(request):
        # Importlar funksiya ichida (Circular import oldini olish uchun)
        from main import bot
        from database import db
        
        try:
            data = await request.json()
            
            # Xizmat turi va yildan foydalanib kod yaratish
            service = data.get('service_type', 'EP')
            random_suffix = os.urandom(2).hex().upper()
            app_code = f"{service}-2026-{random_suffix}"
            
            logger.info(f"📩 Yangi ariza: {app_code} (User: {data.get('user_id')})")

            # 1. Ma'lumotlar bazasiga saqlash
            await db.create_application(
                app_code=app_code,
                user_id=int(data.get('user_id', 0)),
                app_type=service,
                car_number=data.get('vehicle_number', 'Noma\'lum'),
                metadata=data
            )

            # 2. 📢 ADMIN GURUHGA XABAR YUBORISH
            admin_group_id = os.getenv("ADMIN_GROUP_ID")
            if admin_group_id:
                msg = (
                    f"🆕 **Yangi ariza kelib tushdi!**\n\n"
                    f"🆔 **Kod:** `{app_code}`\n"
                    f"🚛 **Mashina:** `{data.get('vehicle_number')}`\n"
                    f"🏢 **Post:** {data.get('border_post')}\n"
                    f"📍 **Manzil:** {data.get('destination')}\n"
                    f"👤 **Foydalanuvchi:** {data.get('user_name', 'Noma\'lum')} (ID: {data.get('user_id')})"
                )
                try:
                    await bot.send_message(chat_id=admin_group_id, text=msg, parse_mode="Markdown")
                except Exception as e:
                    logger.error(f"❌ Admin guruhga xabar yuborishda xato: {e}")

            return web.json_response({'success': True, 'app_code': app_code})
            
        except Exception as e:
            logger.error(f"❌ Mini App submission xatosi: {e}")
            return web.json_response({'success': False, 'error': str(e)}, status=400)

    # --- ROUTES (YO'NALISHLAR) ---
    app.router.add_get('/', root_handler)
    app.router.add_get('/health', health_check)
    app.router.add_get('/miniapp', miniapp_index)
    app.router.add_get('/miniapp/', miniapp_index)
    
    # API yo'nalishlari
    app.router.add_post('/api/applications', miniapp_api_submit)
    app.router.add_post('/api/payme', PaymeAPI.handle_request)
    app.router.add_post('/api/click', ClickAPI.handle_request)
    
    # Statik fayllar (Style, JS, Rasmlar)
    if os.path.exists(miniapp_path):
        app.router.add_static('/miniapp/', miniapp_path, name='miniapp_static')

    logger.info(f"✅ Web server {port}-portda muvaffaqiyatli sozlandi.")
    return app, port

async def start_web_server():
    """Railway muhitida serverni ishga tushirish"""
    app, port = await create_web_app()
    runner = web.AppRunner(app)
    await runner.setup()
    
    # Railway tashqi ulanish uchun 0.0.0.0 talab qiladi
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    
    logger.info(f"🌐 Web server faol: http://0.0.0.0:{port}")
    return runner
