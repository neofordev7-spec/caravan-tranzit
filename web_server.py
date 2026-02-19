"""
CARAVAN TRANZIT Web Server
Serves Mini App static files alongside the Telegram bot
+ Payme Merchant API endpoint (JSON-RPC 2.0)
+ Click API endpoint
"""
import os
import json
import random
from datetime import datetime
from aiohttp import web
import logging
from payme_api import PaymeAPI
from click_api import ClickAPI
from database import db

logger = logging.getLogger(__name__)

# Admin group ID (same as in handlers)
ADMIN_GROUP_ID = -1003463212374


async def create_web_app(bot=None):
    """Create aiohttp web application for serving static files"""
    app = web.Application()
    app['bot'] = bot  # Store bot instance for API endpoints

    # Get port from environment (Railway provides PORT env variable)
    port = int(os.getenv('PORT', 8080))

    # Serve miniapp static files
    miniapp_path = os.path.join(os.path.dirname(__file__), 'miniapp')

    # Health check endpoint
    async def health_check(request):
        return web.json_response({
            'status': 'ok',
            'service': 'CARAVAN TRANZIT Bot + Mini App',
            'miniapp_url': '/miniapp/'
        })

    # Root endpoint - redirect directly to Mini App
    async def root_handler(request):
        raise web.HTTPFound('/miniapp/')

    # Miniapp index handler to ensure index.html is served
    async def miniapp_index(request):
        """Serve the miniapp index.html file"""
        index_path = os.path.join(miniapp_path, 'index.html')
        if os.path.exists(index_path):
            with open(index_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return web.Response(text=content, content_type='text/html')
        else:
            return web.Response(text='Mini App not found', status=404)

    # API endpoint for Mini App submissions (fallback when sendData() fails)
    async def miniapp_api_submit(request):
        try:
            data = await request.json()
            app_code = data.get('code')
            service_type = data.get('service_type', 'EPI')
            user_id = data.get('user_id')
            vehicle_number = data.get('vehicle_number', '')
            border_post = data.get('border_post', '-')
            destination = data.get('destination', '-')
            user_name = data.get('user_name', 'Unknown')
            lang = data.get('language', 'uz')

            # Generate code if not provided
            if not app_code:
                app_code = f"{service_type}-{datetime.now().year}-{random.randint(1000, 9999)}"

            logger.info(f"Mini App API submission: {app_code} from user {user_id}")

            # Save to database
            metadata = {
                'service_type': service_type,
                'border_post': border_post,
                'destination': destination,
                'agent_name': data.get('agent_name', '-'),
                'vehicle_type': data.get('vehicle_type', 'truck'),
                'files_count': data.get('files_count', 0),
                'language': lang,
                'via_webapp': True,
                'via_api': True,
                'status': 'new'
            }

            try:
                if user_id:
                    await db.create_application(
                        app_code, int(user_id), service_type, vehicle_number, metadata
                    )
            except Exception as db_err:
                logger.error(f"DB save error: {db_err}")

            # Send notification to admin group via bot
            bot_instance = request.app.get('bot')
            if bot_instance and user_id:
                try:
                    admin_msg = (
                        f"🆕 <b>YANGI ARIZA</b> (Mini App API)\n\n"
                        f"🆔 <b>Kod:</b> <code>{app_code}</code>\n"
                        f"👤 Foydalanuvchi: {user_name}\n"
                        f"🔑 ID: <code>{user_id}</code>\n"
                        f"📋 Xizmat: {service_type}\n"
                        f"📍 Post: {border_post}\n"
                        f"📍 Manzil: {destination}\n"
                        f"🚛 Mashina: {vehicle_number}\n\n"
                        f"⚠️ <i>Hujjatlar hali yuborilmagan. Foydalanuvchidan kutilmoqda.</i>"
                    )
                    await bot_instance.send_message(
                        ADMIN_GROUP_ID, admin_msg, parse_mode="HTML"
                    )

                    # Tell the user to upload files in bot chat
                    await bot_instance.send_message(
                        int(user_id),
                        f"✅ Ariza qabul qilindi!\n\n"
                        f"🆔 Kod: `{app_code}`\n\n"
                        f"📸 **Endi hujjatlaringizni shu yerga yuboring:**\n"
                        f"Rasmlar, PDF, Word fayllarni yuboring va ✅ tugmasini bosing.",
                        parse_mode="Markdown"
                    )
                except Exception as bot_err:
                    logger.error(f"Bot send error: {bot_err}")

            return web.json_response({
                'success': True,
                'app_code': app_code,
                'message': 'Ariza qabul qilindi!'
            })
        except Exception as e:
            logger.error(f"API error: {e}")
            import traceback
            traceback.print_exc()
            return web.json_response({
                'success': False,
                'error': str(e)
            }, status=400)

    # Payme API endpoint (JSON-RPC 2.0)
    async def payme_endpoint(request):
        """Payme Merchant API - JSON-RPC 2.0 endpoint"""
        return await PaymeAPI.handle_request(request)

    # Click API endpoints
    async def click_prepare(request):
        """Click Prepare endpoint"""
        try:
            data = await request.post()
            result = await ClickAPI.prepare_payment(
                click_trans_id=int(data.get('click_trans_id', 0)),
                merchant_trans_id=data.get('merchant_trans_id', ''),
                amount=float(data.get('amount', 0)),
                sign_time=data.get('sign_time', ''),
                sign_string=data.get('sign_string', '')
            )
            return web.json_response(result)
        except Exception as e:
            logger.error(f"Click prepare error: {e}")
            return web.json_response({"error": -9, "error_note": str(e)})

    async def click_complete(request):
        """Click Complete endpoint"""
        try:
            data = await request.post()
            result = await ClickAPI.complete_payment(
                click_trans_id=int(data.get('click_trans_id', 0)),
                merchant_trans_id=data.get('merchant_trans_id', ''),
                merchant_prepare_id=data.get('merchant_prepare_id', ''),
                amount=float(data.get('amount', 0)),
                sign_time=data.get('sign_time', ''),
                sign_string=data.get('sign_string', ''),
                error=int(data.get('error', 0))
            )
            return web.json_response(result)
        except Exception as e:
            logger.error(f"Click complete error: {e}")
            return web.json_response({"error": -9, "error_note": str(e)})

    # Setup routes
    app.router.add_get('/', root_handler)
    app.router.add_get('/health', health_check)
    app.router.add_get('/miniapp', miniapp_index)  # Redirect without trailing slash
    app.router.add_get('/miniapp/', miniapp_index)  # Main miniapp entry point
    app.router.add_post('/api/applications', miniapp_api_submit)

    # Payment API routes
    app.router.add_post('/api/payme', payme_endpoint)          # Payme JSON-RPC
    app.router.add_post('/api/click/prepare', click_prepare)   # Click Prepare
    app.router.add_post('/api/click/complete', click_complete)  # Click Complete

    # Serve miniapp static files (CSS, JS, images, etc.)
    app.router.add_static('/miniapp/', miniapp_path, name='miniapp', show_index=True)

    logger.info(f"✅ Web server configured on port {port}")
    logger.info(f"📱 Mini App will be available at: /miniapp/")

    return app, port

async def start_web_server(bot=None):
    """Start the web server"""
    app, port = await create_web_app(bot)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    logger.info(f"🌐 Web server started on http://0.0.0.0:{port}")
    return runner

if __name__ == '__main__':
    async def run():
        app, port = await create_web_app(bot=None)
        return app

    logging.basicConfig(level=logging.INFO)
    web.run_app(run())
