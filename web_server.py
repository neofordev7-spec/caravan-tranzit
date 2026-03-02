import os
from aiohttp import web
import logging
from payme_api import PaymeAPI
from click_api import ClickAPI

logger = logging.getLogger(__name__)

async def create_web_app():
    """Create aiohttp web application for serving static files"""
    app = web.Application()

    port = int(os.getenv('PORT', 8080))
    miniapp_path = os.path.join(os.path.dirname(__file__), 'miniapp')

    # MUHIM: Root endpoint endi 200 qaytaradi (Railway Health Check uchun)
    async def root_handler(request):
        return web.Response(text="Bot and Mini App are running!", status=200)

    # Alohida health check manzilini saqlab qolamiz
    async def health_check(request):
        return web.json_response({'status': 'ok'})

    async def miniapp_index(request):
        index_path = os.path.join(miniapp_path, 'index.html')
        if os.path.exists(index_path):
            with open(index_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return web.Response(text=content, content_type='text/html')
        else:
            return web.Response(text='Mini App not found', status=404)

    async def miniapp_api_submit(request):
        try:
            data = await request.json()
            app_code = f"{data.get('service_type', 'EP')}-{os.urandom(3).hex().upper()}"
            logger.info(f"Mini App submission: {data}")
            return web.json_response({'success': True, 'app_code': app_code})
        except Exception as e:
            return web.json_response({'success': False, 'error': str(e)}, status=400)

    async def payme_endpoint(request):
        return await PaymeAPI.handle_request(request)

    # Routes (Tartibga solindi)
    app.router.add_get('/', root_handler)           # ENDI 200 OK QAYTARADI
    app.router.add_get('/health', health_check)     # Health check
    app.router.add_get('/miniapp', miniapp_index)
    app.router.add_get('/miniapp/', miniapp_index)
    
    # API va To'lovlar
    app.router.add_post('/api/applications', miniapp_api_submit)
    app.router.add_post('/api/payme', payme_endpoint)
    
    # Static files
    if os.path.exists(miniapp_path):
        app.router.add_static('/miniapp/', miniapp_path, name='miniapp')

    logger.info(f"✅ Web server configured on port {port}")
    return app, port

async def start_web_server():
    app, port = await create_web_app()
    runner = web.AppRunner(app)
    await runner.setup()
    # 0.0.0.0 Railway uchun shart
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    logger.info(f"🌐 Web server started on http://0.0.0.0:{port}")
    return runner
