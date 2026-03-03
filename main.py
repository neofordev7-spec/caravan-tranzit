import asyncio
import logging
import sys
import os
from typing import Any, Callable, Dict, Awaitable
from aiogram import Bot, Dispatcher, types, BaseMiddleware
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

# 2. KONFIGURATSIYA
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
# ID raqami kodda yozilmagan, u faqat Railway Variables'dan olinadi
ADMIN_ID = os.getenv("ADMIN_ID") 

if not BOT_TOKEN:
    logging.error("❌ BOT_TOKEN topilmadi!")
    sys.exit(1)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher(storage=MemoryStorage())

# --- 3. KIBERXAVFSIZLIK: ADMIN MIDDLEWARE ---
class AdminAccessMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: types.TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        user = data.get("event_from_user")
        
        # Muhim: ADMIN_ID Railway'da o'rnatilganligini tekshiramiz
        if not ADMIN_ID:
            logging.warning("⚠️ ADMIN_ID o'zgaruvchisi o'rnatilmagan!")
        
        # Faqat ADMIN_ID ga mos keladigan foydalanuvchini o'tkazadi
        if user and str(user.id) != str(ADMIN_ID):
            if isinstance(event, types.Message):
                await event.answer("⚠️ **Kirish taqiqlangan!**\nSizda admin huquqlari yo'q.")
            return 
            
        return await handler(event, data)
# --------------------------------------------

async def main():
    web_runner = None

    # 4. BAZA VA SERVER
    try:
        await db.connect()
        await db.seed_customs_posts()
        print("✅ Baza ulandi!")
    except Exception as e:
        print(f"❌ Baza xatosi: {e}")
        return

    try:
        web_runner = await start_web_server()
        print("✅ Web server ishga tushdi!")
    except Exception as e:
        print(f"⚠️ Web server xatosi: {e}")

    # --- 5. MIDDLEWARE ULASH ---
    admin_router.message.middleware(AdminAccessMiddleware())
    admin_router.callback_query.middleware(AdminAccessMiddleware())

    # Routerlar
    dp.include_router(payment_router)
    dp.include_router(admin_router)
    dp.include_router(webapp_router)
    dp.include_router(router)

    # 6. KONFLIKT VA POLLING
    await bot.delete_webhook(drop_pending_updates=True)
    print("⏳ Conflict oldini olish uchun 5 soniya kutilmoqda...")
    await asyncio.sleep(5)

    print(f"🚀 Bot polling rejimida ishga tushdi!")

    try:
        await dp.start_polling(bot)
    finally:
        print("🛑 Graceful shutdown boshlandi...")
        if web_runner:
            await web_runner.cleanup()
        await db.close()
        if bot.session:
            await bot.session.close()
            await asyncio.sleep(0.2) # Sessiyani tozalash uchun pauza
        print("🛑 Bot to'xtatildi.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("🛑 Dastur to'xtatildi.")
