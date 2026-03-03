import os
import logging
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

    # 1. ROOT HANDLER (Asosiy linkka kirganda avtomatik Mini Appni ochadi)
    async def root_handler(request):
        # Foydalanuvchini / dan /miniapp/ ga yo'naltiramiz (302 Redirect)
        return web.HTTPFound('/miniapp/')

    # 2. HEALTH CHECK (Railway uchun status)
    async def health_check(request):
        return web.json_response({'status': 'ok', 'server': 'CaravanTranzit'})

    # 3. MINI APP INDEX HANDLER (index.html faylini xavfsiz o'qish)
    async def miniapp_index(request):
        """Mini Appning asosiy sahifasini (index.html) ko'rsatish"""
        index_path = os.path.join(miniapp_path, 'index.html')
        if os.path.exists(index_path):
            # web.FileResponse - faylni o'qib, brauzerga to'g'ri formatda uzatadi
            return web.FileResponse(index_path)
        else:
            logger.error(f"❌ Mini App topilmadi: {index_path}")
            return web.Response(text='Mini App topilmadi (index.html missing)', status=404)

    async def miniapp_api_submit(request):
        """Mini Appdan kelgan ariza ma'lumotlarini qabul qilish"""
        try:
            data = await request.json()
            import os as os_lib
            app_code = f"{data.get('service_type', 'EP')}-{os_lib.urandom(3).hex().upper()}"
            logger.info(f"🆕 Mini App submission: {data}")
            return web.json_response({'success': True, 'app_code': app_code})
        except Exception as e:
            logger.error(f"❌ Mini App submission xatosi: {e}")
            return web.json_response({'success': False, 'error': str(e)}, status=400)

    # --- ROUTES (YO'NALISHLAR) - Tartib juda muhim! ---
    
    # 1. Avval asosiy yo'naltirish (Redirect)
    app.router.add_get('/', root_handler)
    
    # 2. Health check
    app.router.add_get('/health', health_check)
    
    # 3. Mini App Index (Slash bilan va slashsiz)
    app.router.add_get('/miniapp', miniapp_index)
    app.router.add_get('/miniapp/', miniapp_index)
    
    # 4. API Endpoints
    app.router.add_post('/api/applications', miniapp_api_submit)
    app.router.add_post('/api/payme', PaymeAPI.handle_request)
    app.router.add_post('/api/click', ClickAPI.handle_request)
    
    # 5. Statik fayllar (CSS, JS, Images) - Oxirida bo'lishi shart!
    if os.path.exists(miniapp_path):
        # Bu qator style.css, app.js kabi fayllarni avtomatik topishga yordam beradi
        app.router.add_static('/miniapp/', miniapp_path, name='miniapp_static')
        logger.info(f"📁 Statik fayllar yo'li: {miniapp_path}")

    logger.info(f"✅ Web server {port}-portda muvaffaqiyatli sozlandi.")
    return app, port

async def start_web_server():
    """Railway muhitida serverni ishga tushirish"""
    app, port = await create_web_app()
    runner = web.AppRunner(app)
    await runner.setup()
    
    # '0.0.0.0' Railway konteynerlari uchun majburiy
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    
    logger.info(f"🌐 Web server ishga tushdi: http://0.0.0.0:{port}")
    return runner
