import asyncio
import logging
import sys
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from handlers import router
from web_app_handlers import router as webapp_router
from admin_handlers import router as admin_router
from payment_handlers import router as payment_router
from database import db
from web_server import start_web_server

# Loglarni sozlash
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# --- 1. BOT VA DISPATCHERNI GLOBAL QILAMIZ ---
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    print("❌ BOT_TOKEN environment variable is not set!")
    sys.exit(1)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher(storage=MemoryStorage())
# --------------------------------------------

async def main():
    web_runner = None

    # Ma'lumotlar bazasiga ulanish
    try:
        await db.connect()
        await db.seed_customs_posts()
        await db.seed_test_agents()
        print("✅ Baza ulandi va seed data yuklandi!")
    except Exception as e:
        print(f"❌ Baza xatosi: {e}")
        return

    # Web serverni Mini App va API uchun ishga tushirish
    try:
        web_runner = await start_web_server()
        print("✅ Web server ishga tushdi!")
    except Exception as e:
        print(f"⚠️ Web server xatosi: {e}")

    # Routerlarni ulash
    dp.include_router(payment_router)
    dp.include_router(admin_router)
    dp.include_router(webapp_router)
    dp.include_router(router)

    # Konfliktni oldini olish
    await bot.delete_webhook(drop_pending_updates=True)
    print("⏳ Conflict oldini olish uchun 5 soniya kutilmoqda...")
    await asyncio.sleep(5) 

    print("🚀 Bot polling rejimida ishga tushdi!")

    try:
        await dp.start_polling(bot)
    finally:
        print("🛑 Graceful shutdown boshlandi...")
        if web_runner:
            await web_runner.cleanup()
        await db.close()
        await bot.session.close()
        print("🛑 Bot to'xtatildi.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("🛑 Stop.")
