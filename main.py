import asyncio
import logging
import sys
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties # MUHIM YANGILIK
from aiogram.enums import ParseMode # MUHIM YANGILIK
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from handlers import router
from web_app_handlers import router as webapp_router
from admin_handlers import router as admin_router
from payment_handlers import router as payment_router
from database import db
from web_server import start_web_server

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

async def main():
    load_dotenv()
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN environment variable is not set!")
        return

    try:
        await db.connect()
        await db.create_tables()
        await db.seed_customs_posts()
        await db.seed_test_agents()
        print("✅ Baza ulandi va seed data yuklandi!")
    except Exception as e:
        print(f"❌ Baza xatosi: {e}")
        return

    # Start web server for Mini App
    try:
        web_runner = await start_web_server()
        print("✅ Web server Mini App uchun ishga tushdi!")
        print(f"📱 Mini App URL: https://caravan-tranzit-production.up.railway.app/miniapp/")
    except Exception as e:
        print(f"⚠️ Web server xatosi (bot ishlaydi): {e}")

    # --- O'ZGARISH SHU YERDA ---
    # parse_mode=ParseMode.MARKDOWN -> Bu **text** ni qalin qiladi
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))

    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(payment_router)  # Payment handlers (birinchi o'rinda)
    dp.include_router(admin_router)     # Admin handlers
    dp.include_router(webapp_router)    # Web App handlers
    dp.include_router(router)           # Boshqa handlerlar

    print("🚀 Bot ishga tushdi!")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Stop.")
