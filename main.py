import asyncio
import logging
import signal
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

async def main():
    load_dotenv()
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN environment variable is not set!")
        return

    web_runner = None

    # 1. Ma'lumotlar bazasiga ulanish
    try:
        await db.connect()
        await db.seed_customs_posts()
        await db.seed_test_agents()
        print("✅ Baza ulandi va seed data yuklandi!")
    except Exception as e:
        print(f"❌ Baza xatosi: {e}")
        return

    # 2. Web serverni Mini App uchun ishga tushirish
    try:
        web_runner = await start_web_server()
        print("✅ Web server Mini App uchun ishga tushdi!")
        print(f"📱 Mini App URL: https://caravan-tranzit-production.up.railway.app/miniapp/")
    except Exception as e:
        print(f"⚠️ Web server xatosi (bot ishlaydi): {e}")

    # 3. Bot va Dispatcher obyektlarini yaratish
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
    dp = Dispatcher(storage=MemoryStorage())

    # Routerlarni ulash
    dp.include_router(payment_router)  # To'lov handlerlari
    dp.include_router(admin_router)    # Admin handlerlari
    dp.include_router(webapp_router)   # Web App handlerlari
    dp.include_router(router)          # Boshqa asosiy handlerlar

    # --- KONFLIKTNI OLIDINI OLISH (REDKSIYA) ---
    # 4. Eski webhook/sessiyalarni majburiy tozalash
    await bot.delete_webhook(drop_pending_updates=True)
    
    # 5. Telegram serveriga eski ulanishni yopish uchun 5 soniya vaqt beramiz
    print("⏳ Conflict xatosini oldini olish uchun 5 soniya kutilmoqda...")
    await asyncio.sleep(5) 
    # ------------------------------------------

    print("🚀 Bot polling rejimida ishga tushdi!")

    try:
        # Pollingni boshlash
        await dp.start_polling(bot)
    finally:
        # Graceful shutdown: barcha resurslarni tozalash
        print("🛑 Graceful shutdown boshlandi...")

        if web_runner:
            await web_runner.cleanup()
            print("✅ Web server yopildi.")

        await db.close()
        print("✅ Database pool yopildi.")

        await bot.session.close()
        print("✅ Bot session yopildi.")

        print("🛑 Bot to'xtatildi.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("🛑 Stop.")
