import os
import hashlib
import time
import logging
from decimal import Decimal
from aiohttp import web
from database import db

# Loglarni sozlash
logger = logging.getLogger(__name__)

# 1. KONFIGURATSIYA (Railway Variables'dan olinadi)
CLICK_SERVICE_ID = os.getenv("CLICK_SERVICE_ID", "")
CLICK_MERCHANT_ID = os.getenv("CLICK_MERCHANT_ID", "")
CLICK_SECRET_KEY = os.getenv("CLICK_SECRET_KEY", "")
ADMIN_GROUP_ID = os.getenv("ADMIN_GROUP_ID")

# 🛡 KIBERXAVFSIZLIK: Click rasmiy IP manzillari
CLICK_IPS = ["185.178.209.155", "185.178.209.156"]

class ClickAPI:
    """Click.uz to'lov tizimi uchun xavfsiz API handler"""

    @staticmethod
    async def handle_request(request: web.Request) -> web.Response:
        """Click serveridan kelgan POST so'rovni qabul qilish"""
        
        # 🛡 1-QALQON: IP Tekshiruvi (IP Whitelisting)
        client_ip = request.headers.get("X-Forwarded-For", request.remote).split(',')[0].strip()
        if client_ip not in CLICK_IPS:
            logger.warning(f"🚫 CLICK: Begona IP ({client_ip}) urinishi!")
            # Productionda 403 qaytarish shart
            return web.json_response({"error": "-8", "error_note": "Forbidden IP"}, status=403)

        # Click so'rovlari application/x-www-form-urlencoded formatida keladi
        data = await request.post()
        
        click_trans_id = data.get('click_trans_id')
        service_id = data.get('service_id')
        click_paydoc_id = data.get('click_paydoc_id')
        merchant_trans_id = data.get('merchant_trans_id') # Bu bizning app_code
        amount = data.get('amount')
        action = data.get('action')
        error = data.get('error')
        sign_time = data.get('sign_time')
        sign_string = data.get('sign_string')

        # 🛡 2-QALQON: MD5 Signature (Xesh) tekshiruvi
        # Click formulasi: md5(click_trans_id + service_id + secret_key + merchant_trans_id + amount + action + sign_time)
        check_payload = (
            f"{click_trans_id}{service_id}{CLICK_SECRET_KEY}{merchant_trans_id}"
            f"{click_paydoc_id if action == '1' else ''}{amount}{action}{sign_time}"
        )
        my_sign = hashlib.md5(check_payload.encode()).hexdigest()

        if my_sign != sign_string:
            logger.error(f"❌ CLICK: Sign xatosi! App: {merchant_trans_id}")
            return web.json_response({"error": "-1", "error_note": "SIGN CHECK FAILED!"})

        # 3. ACTIONLARGA QARAB ISHLASH (0: Prepare, 1: Complete)
        if action == '0':
            return await ClickAPI.prepare(merchant_trans_id, amount, click_trans_id)
        elif action == '1':
            return await ClickAPI.complete(merchant_trans_id, amount, click_trans_id, error)
        
        return web.json_response({"error": "-3", "error_note": "Action not found"})

    @staticmethod
    async def prepare(app_code, amount, click_id):
        """Action 0: Arizani va summani tekshirish"""
        app = await db.get_application_by_code(app_code)
        
        if not app:
            return web.json_response({"error": "-5", "error_note": "Application not found"})
        
        if app['status'] == 'paid':
            return web.json_response({"error": "-4", "error_note": "Already paid"})

        # Narxni tekshirish (ixtiyoriy, agar narx qat'iy bo'lsa)
        if app['price'] and Decimal(str(amount)) != app['price']:
            return web.json_response({"error": "-2", "error_note": "Incorrect amount"})

        # Tranzaksiyani yaratish (Pending holatida)
        await db.create_transaction(
            user_id=app['user_id'],
            application_id=app['id'],
            amount=Decimal(str(amount)),
            trans_type='card_payment',
            payment_provider='click',
            payment_id=str(click_id),
            create_time=int(time.time() * 1000)
        )
        
        return web.json_response({
            "click_trans_id": click_id,
            "merchant_trans_id": app_code,
            "merchant_prepare_id": click_id,
            "error": "0",
            "error_note": "Success"
        })

    @staticmethod
    async def complete(app_code, amount, click_id, error):
        """Action 1: To'lovni yakunlash"""
        if error != '0':
            logger.warning(f"⚠️ CLICK: To'lov bekor qilindi. Click ID: {click_id}")
            return web.json_response({"error": "-9", "error_note": "Transaction cancelled"})

        from main import bot
        app = await db.get_application_by_code(app_code)
        transaction = await db.get_transaction_by_payment_id(str(click_id))

        if not transaction:
            return web.json_response({"error": "-6", "error_note": "Transaction not found"})

        # Bazani yangilash
        now_ms = int(time.time() * 1000)
        await db.update_transaction_status(transaction['id'], 'completed', str(click_id), perform_time=now_ms)
        await db.update_application_status(app_code, 'paid')

        # 📱 FOYDALANUVCHIGA XABAR
        try:
            await bot.send_message(
                chat_id=app['user_id'],
                text=f"✅ **Click orqali to'lov qabul qilindi!**\n\n🆔 Ariza: `{app_code}`\n💰 Summa: {amount} so'm"
            )
        except: pass

        # 💰 ADMINGA XABAR
        if ADMIN_GROUP_ID:
            try:
                await bot.send_message(chat_id=ADMIN_GROUP_ID, text=f"💰 **Yangi Click to'lovi!**\nAriza: `{app_code}`")
            except: pass

        return web.json_response({
            "click_trans_id": click_id,
            "merchant_trans_id": app_code,
            "merchant_confirm_id": click_id,
            "error": "0",
            "error_note": "Success"
        })

    @staticmethod
    def generate_payment_url(app_code: str, amount: Decimal) -> str:
        """
        Telefondagi Click ilovasini (App) ochadigan Universal Link yaratish.
        """
        # my.click.uz linki mobil ilovani avtomatik taniydi
        return (
            f"https://my.click.uz/services/pay"
            f"?service_id={CLICK_SERVICE_ID}"
            f"&merchant_id={CLICK_MERCHANT_ID}"
            f"&amount={float(amount)}"
            f"&transaction_param={app_code}"
            f"&return_url=https://t.me/caravan_tranzit_bot"
        )
