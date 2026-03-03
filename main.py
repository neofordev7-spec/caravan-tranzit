import asyncio
import logging
import sys
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

# Loyiha modullari (Routerlar va Database)
from handlers import router
from web_app_handlers import router as webapp_router
from admin_handlers import router as admin_router
from payment_handlers import router as payment_router
from database import db
from web_server import start_web_server

# 1. LOGLARNI SOZLASH
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# 2. KONFIGURATSIYANI YUKLASH VA BOTNI GLOBAL QILISH
# Bu qism payme_api.py avtomatik xabar yuborishi uchun juda muhim
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    logging.error("❌ BOT_TOKEN environment variable is not set!")
    sys.exit(1)

# Bot va Dispatcher obyektlarini global darajada yaratish
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher(storage=MemoryStorage())

async def main():
    web_runner = None

    # 3. MA'LUMOTLAR BAZASIGA ULANISH
    try:
        await db.connect() # Railway Postgres bazasiga ulanish
        await db.seed_customs_posts() # Baza jadvallarini tekshirish
        await db.seed_test_agents()
        print("✅ Baza ulandi va seed data yuklandi!")
    except Exception as e:
        print(f"❌ Baza xatosi: {e}")
        return

    # 4. WEB SERVERNI ISHGA TUSHIRISH (Mini App va To'lovlar uchun)
    try:
        web_runner = await start_web_server() 
        print("✅ Web server Mini App uchun ishga tushdi!")
        print(f"📱 Mini App URL: https://caravan-tranzit-production.up.railway.app/miniapp/")
    except Exception as e:
        print(f"⚠️ Web server xatosi (bot ishlaydi): {e}")

    # 5. ROUTERLARNI ULASH
    dp.include_router(payment_router)  # Payme/Click
    dp.include_router(admin_router)    # Admin
    dp.include_router(webapp_router)   # Web App
    dp.include_router(router)          # Asosiy handlerlar

    # 6. KONFLIKTNI OLDINI OLISH
    # Railway'da eski konteyner o'chishiga ulgurishi uchun webhookni o'chirib 5 soniya kutamiz
    await bot.delete_webhook(drop_pending_updates=True)
    print("⏳ Conflict oldini olish uchun 5 soniya kutilmoqda...")
    await asyncio.sleep(5)

    print("🚀 Bot polling rejimida ishga tushdi!")

    try:
        # Pollingni boshlash
        await dp.start_polling(bot)
    finally:
        # 7. GRACEFUL SHUTDOWN (Madaniyatli yopilish)
        print("🛑 Graceful shutdown boshlandi...")

        if web_runner:
            await web_runner.cleanup()
            print("✅ Web server yopildi.")

        await db.close()
        print("✅ Database pool yopildi.")

        # BOT SESSIYASINI TOZA YOPISH
        if bot.session:
            await bot.session.close()
            # SIZ SO'RAGAN MUHIM PAUZA:
            await asyncio.sleep(0.2) 
            print("✅ Bot session va tarmoq ulanishlari yopildi.")

        print("🛑 Bot to'xtatildi.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("🛑 Dastur to'xtatildi.")
