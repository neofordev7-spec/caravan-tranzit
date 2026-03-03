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

    # 1. ROOT HANDLER (Railway sog'lomlikni tekshirishi uchun 200 OK qaytaradi)
    async def root_handler(request):
        return web.Response(text="🚀 Caravan Tranzit Bot and Mini App are running smoothly!", status=200)

    # 2. HEALTH CHECK (Tizim holati uchun JSON)
    async def health_check(request):
        return web.json_response({'status': 'ok', 'server': 'CaravanTranzit'})

    # 3. MINI APP HANDLERS
    async def miniapp_index(request):
        """Mini Appning asosiy sahifasini (index.html) ko'rsatish"""
        index_path = os.path.join(miniapp_path, 'index.html')
        if os.path.exists(index_path):
            with open(index_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return web.Response(text=content, content_type='text/html')
        else:
            logger.error(f"❌ Mini App topilmadi: {index_path}")
            return web.Response(text='Mini App topilmadi (index.html missing)', status=404)

    async def miniapp_api_submit(request):
        """Mini Appdan kelgan ariza ma'lumotlarini qabul qilish"""
        try:
            data = await request.json()
            # Tasodifiy ariza kodi yaratish
            import os as os_lib
            app_code = f"{data.get('service_type', 'EP')}-{os_lib.urandom(3).hex().upper()}"
            logger.info(f"🆕 Mini App submission: {data}")
            return web.json_response({'success': True, 'app_code': app_code})
        except Exception as e:
            logger.error(f"❌ Mini App submission xatosi: {e}")
            return web.json_response({'success': False, 'error': str(e)}, status=400)

    # --- ROUTES (YO'NALISHLAR) ---
    
    # Asosiy va Health Check
    app.router.add_get('/', root_handler)
    app.router.add_get('/health', health_check)
    
    # Mini App sahifalari
    app.router.add_get('/miniapp', miniapp_index)
    app.router.add_get('/miniapp/', miniapp_index)
    
    # API: Arizalar
    app.router.add_post('/api/applications', miniapp_api_submit)
    
    # 💰 TO'LOV TIZIMLARI (Secure Endpoints)
    # Payme so'rovlarini qabul qilish
    app.router.add_post('/api/payme', PaymeAPI.handle_request)
    # Click so'rovlarini qabul qilish (YANGI QO'SHILDI)
    app.router.add_post('/api/click', ClickAPI.handle_request)
    
    # Mini App uchun statik fayllar (CSS, JS, Images)
    if os.path.exists(miniapp_path):
        app.router.add_static('/miniapp/', miniapp_path, name='miniapp_static')
        logger.info(f"📁 Statik fayllar yo'li: {miniapp_path}")

    logger.info(f"✅ Web server 8080-portda (v{port}) muvaffaqiyatli sozlandi.")
    return app, port

async def start_web_server():
    """Railway muhitida serverni ishga tushirish"""
    app, port = await create_web_app()
    runner = web.AppRunner(app)
    await runner.setup()
    
    # '0.0.0.0' Railway konteynerlari uchun majburiy (tashqi dunyo ulanishi uchun)
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    
    logger.info(f"🌐 Web server ishga tushdi: http://0.0.0.0:{port}")
    return runner
