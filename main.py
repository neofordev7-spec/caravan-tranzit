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

# Loyiha modullari
from handlers import router
from web_app_handlers import router as webapp_router
from admin_handlers import router as admin_router
from payment_handlers import router as payment_router
from database import db
from web_server import start_web_server

# 1. LOGLARNI SOZLASH
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# 2. BOT VA DISPATCHERNI GLOBAL QILAMIZ
# Bu boshqa fayllar (payme_api.py) botdan foydalanishi uchun shart
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    logging.error("❌ BOT_TOKEN topilmadi! .env fayli yoki Railway Variablesni tekshiring.")
    sys.exit(1)

# Bot va Dispatcher obyektlari
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher(storage=MemoryStorage())

async def main():
    web_runner = None

    # 3. MA'LUMOTLAR BAZASIGA ULANISH
    try:
        await db.connect() # Caravan Tranzit bazasiga ulanish
        await db.seed_customs_posts()
        await db.seed_test_agents()
        print("✅ Baza ulandi va seed data yuklandi!")
    except Exception as e:
        print(f"❌ Baza xatosi: {e}")
        return

    # 4. WEB SERVERNI ISHGA TUSHIRISH (Mini App va To'lovlar uchun)
    try:
        web_runner = await start_web_server() # Port 8080 da ishga tushadi
        print("✅ Web server Mini App uchun ishga tushdi!")
        print(f"📱 Mini App URL: https://caravan-tranzit-production.up.railway.app/miniapp/")
    except Exception as e:
        print(f"⚠️ Web server xatosi (bot ishlaydi): {e}")

    # 5. ROUTERLARNI ULASH
    dp.include_router(payment_router)  # Payme/Click handlerlari
    dp.include_router(admin_router)    # Admin boshqaruvi
    dp.include_router(webapp_router)   # Mini App handlerlari
    dp.include_router(router)          # Umumiy handlerlar

    # 6. KONFLIKTNI OLDINI OLISH (Railway uchun maxsus)
    # Avval eski webhooklarni tozalaymiz
    await bot.delete_webhook(drop_pending_updates=True)
    
    # Railway eskisini o'chirib ulgurishi uchun 5 soniya pauza
    print("⏳ Conflict (to'qnashuv) xatosini oldini olish uchun 5 soniya kutilmoqda...")
    await asyncio.sleep(5) 

    print("🚀 Bot polling rejimida ishga tushdi!")

    try:
        # Pollingni boshlash
        await dp.start_polling(bot)
    finally:
        # 7. GRACEFUL SHUTDOWN (Madaniyatli yopilish)
        # Railway SIGTERM yuborganida barcha resurslarni xavfsiz yopamiz
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
        print("🛑 Dastur to'xtatildi.")
