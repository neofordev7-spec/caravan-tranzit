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
ADMIN_ID = os.getenv("ADMIN_ID") # O'zingizning shaxsiy ID-ingiz (masalan: 3463212374)

if not BOT_TOKEN:
    logging.error("❌ BOT_TOKEN environment variable is not set!")
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
        
        # Admin ID ni tekshirish (Faqat siz kira olasiz)
        if user and str(user.id) != str(ADMIN_ID):
            if isinstance(event, types.Message):
                await event.answer("⚠️ **Kirish taqiqlangan!**\nBu bo'lim faqat asosiy admin uchun.")
            return # Handlerga o'tkazmasdan to'xtatadi
            
        return await handler(event, data)
# --------------------------------------------

async def main():
    web_runner = None

    # 4. MA'LUMOTLAR BAZASIGA ULANISH
    try:
        await db.connect()
        await db.seed_customs_posts()
        await db.seed_test_agents()
        print("✅ Baza ulandi!")
    except Exception as e:
        print(f"❌ Baza xatosi: {e}")
        return

    # 5. WEB SERVER (Mini App va To'lovlar)
    try:
        web_runner = await start_web_server()
        print("✅ Web server ishga tushdi!")
    except Exception as e:
        print(f"⚠️ Web server xatosi: {e}")

    # --- 6. MIDDLEWARENI FAQAT ADMIN ROUTERGA ULASH ---
    # Shunda oddiy foydalanuvchilar botning boshqa qismlaridan bemalol foydalana oladi
    admin_router.message.middleware(AdminAccessMiddleware())
    admin_router.callback_query.middleware(AdminAccessMiddleware())

    # Routerlarni ulash
    dp.include_router(payment_router)
    dp.include_router(admin_router)
    dp.include_router(webapp_router)
    dp.include_router(router)

    # 7. KONFLIKTNI OLDINI OLISH
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
        if bot.session:
            await bot.session.close()
            await asyncio.sleep(0.2)
        print("🛑 Bot to'xtatildi.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("🛑 Dastur to'xtatildi.")
