import os
import base64
import time
import logging
from decimal import Decimal
from aiohttp import web
from database import db

# Loglarni sozlash
logger = logging.getLogger(__name__)

# 1. KONFIGURATSIYA
PAYME_MERCHANT_ID = os.getenv("PAYME_MERCHANT_ID", "")
PAYME_MERCHANT_KEY = os.getenv("PAYME_MERCHANT_KEY", "")
# ⚡️ YANGILANISH: Ilovani (App) ochish uchun yangi URL
PAYME_APP_URL = "https://payme.uz/pay"
ADMIN_GROUP_ID = os.getenv("ADMIN_GROUP_ID") 

# 🛡 KIBERXAVFSIZLIK: Payme rasmiy IP manzillari
PAYME_IPS = ["195.158.31.134", "195.158.31.135", "195.158.28.14"]

# =============================================================
# ⚡️ APP REDIRECT FUNKSIYASI (ASOSIY O'ZGARISH)
# =============================================================
def generate_checkout_url(order_id: str, amount_uzs: Decimal) -> str:
    """
    Payme ilovasini (App) to'g'ridan-to'g'ri ochish uchun URL yaratish.
    Agar telefon bo'lsa - ilovani, kompyuter bo'lsa - brauzerni ochadi.
    """
    amount_tiyin = int(amount_uzs * 100)
    # Parametrlarni shakllantirish
    params = f"m={PAYME_MERCHANT_ID};ac.order_id={order_id};a={amount_tiyin}"
    # Base64 formatiga o'tkazish
    encoded = base64.b64encode(params.encode()).decode()
    
    # https://payme.uz/pay/{base64} ko'rinishida qaytaradi
    return f"{PAYME_APP_URL}/{encoded}"

# =============================================================
# AUTENTIFIKATSIYA VA XAVFSIZLIK
# =============================================================
def verify_auth(request) -> bool:
    """Payme autentifikatsiyasini tekshirish (Basic Auth)"""
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Basic "):
        return False
    try:
        decoded = base64.b64decode(auth_header[6:]).decode()
        login, password = decoded.split(":", 1)
        return login.lower() in ["paycom", "payme"] and password == PAYME_MERCHANT_KEY
    except Exception:
        return False

def error_response(rpc_id, code: int, message_uz: str):
    return {
        "jsonrpc": "2.0",
        "id": rpc_id,
        "error": {
            "code": code,
            "message": {"uz": message_uz, "ru": message_uz, "en": message_uz}
        }
    }

def success_response(rpc_id, result: dict):
    return {"jsonrpc": "2.0", "id": rpc_id, "result": result}

# =============================================================
# PAYME API ASOSIY LOGIKASI
# =============================================================
class PaymeAPI:
    @staticmethod
    async def handle_request(request: web.Request) -> web.Response:
        # 🛡 1-QALQON: IP Tekshiruvi
        client_ip = request.headers.get("X-Forwarded-For", request.remote).split(',')[0].strip()
        
        if client_ip not in PAYME_IPS:
            logger.warning(f"🚫 SHUBHALI SO'ROV: IP {client_ip} tizimga kirishga urindi!")
            return web.json_response({"error": "Forbidden IP"}, status=403)

        # 🛡 2-QALQON: Auth Tekshiruvi
        if not verify_auth(request):
            return web.json_response(error_response(None, -32504, "Auth xatosi"), status=200)

        try:
            body = await request.json()
        except Exception:
            return web.json_response(error_response(None, -32700, "JSON xatosi"), status=200)

        method = body.get("method", "")
        params = body.get("params", {})
        rpc_id = body.get("id")

        handlers = {
            "CheckPerformTransaction": PaymeAPI.check_perform_transaction,
            "CreateTransaction": PaymeAPI.create_transaction,
            "PerformTransaction": PaymeAPI.perform_transaction,
            "CancelTransaction": PaymeAPI.cancel_transaction,
            "CheckTransaction": PaymeAPI.check_transaction,
            "GetStatement": PaymeAPI.get_statement,
        }

        handler = handlers.get(method)
        if not handler:
            return web.json_response(error_response(rpc_id, -32601, "Metod yo'q"), status=200)

        result = await handler(rpc_id, params)
        return web.json_response(result, status=200)

    @staticmethod
    async def check_perform_transaction(rpc_id, params: dict) -> dict:
        account = params.get("account", {})
        order_id = account.get("order_id")
        app = await db.get_application_by_code(order_id)
        if not app: return error_response(rpc_id, -31050, "Ariza topilmadi")
        if app['status'] == 'paid': return error_response(rpc_id, -31052, "To'langan")
        return success_response(rpc_id, {"allow": True})

    @staticmethod
    async def create_transaction(rpc_id, params: dict) -> dict:
        payme_id = params.get("id")
        account = params.get("account", {})
        order_id = account.get("order_id")
        
        existing = await db.get_transaction_by_payment_id(payme_id)
        if existing:
            state = 1 if existing['status'] == 'pending' else 2
            return success_response(rpc_id, {
                "create_time": int(existing['create_time']),
                "transaction": str(existing['id']),
                "state": state
            })

        app = await db.get_application_by_code(order_id)
        if not app: return error_response(rpc_id, -31050, "Ariza topilmadi")

        transaction = await db.create_transaction(
            user_id=app['user_id'], application_id=app['id'],
            amount=Decimal(str(params.get("amount"))) / 100,
            trans_type='card_payment', payment_provider='payme',
            payment_id=payme_id, create_time=int(params.get("time"))
        )
        return success_response(rpc_id, {
            "create_time": int(transaction['create_time']),
            "transaction": str(transaction['id']),
            "state": 1
        })

    @staticmethod
    async def perform_transaction(rpc_id, params: dict) -> dict:
        """To'lovni yakunlash va AVTOMATIK bot xabarlari"""
        try:
            from main import bot 
            payme_id = params.get("id")
            transaction = await db.get_transaction_by_payment_id(payme_id)
            if not transaction: return error_response(rpc_id, -31003, "Xato")

            if transaction['status'] == 'completed':
                return success_response(rpc_id, {
                    "perform_time": int(transaction['perform_time']),
                    "transaction": str(transaction['id']), "state": 2
                })

            now_ms = int(time.time() * 1000)
            updated = await db.update_transaction_status(transaction['id'], 'completed', payme_id, perform_time=now_ms)
            app = await db.get_application_by_id(transaction['application_id'])
            await db.update_application_status(app['app_code'], 'paid')

            # 🔥 FOYDALANUVCHIGA XABAR
            user_text = f"✅ **To'lov qabul qilindi!**\n\n🆔 Ariza: `{app['app_code']}`\n💰 Summa: {transaction['amount']} so'm\n📊 Holati: **To'langan**"
            try:
                await bot.send_message(chat_id=app['user_id'], text=user_text)
            except: pass

            # 🔥 ADMINGA XABAR
            if ADMIN_GROUP_ID:
                try:
                    await bot.send_message(chat_id=ADMIN_GROUP_ID, text=f"💰 **Yangi to'lov!**\nAriza: `{app['app_code']}`\nSumma: {transaction['amount']} so'm")
                except: pass

            return success_response(rpc_id, {"perform_time": now_ms, "transaction": str(updated['id']), "state": 2})
        except Exception as e:
            logger.error(f"Perform error: {e}")
            return error_response(rpc_id, -31099, "Server xatosi")

    @staticmethod
    async def cancel_transaction(rpc_id, params: dict) -> dict:
        payme_id = params.get("id")
        reason = params.get("reason")
        transaction = await db.get_transaction_by_payment_id(payme_id)
        if not transaction: return error_response(rpc_id, -31003, "Xato")

        now_ms = int(time.time() * 1000)
        updated = await db.update_transaction_status(transaction['id'], 'cancelled', payme_id, cancel_time=now_ms, cancel_reason=reason)
        state = -2 if transaction['status'] == 'completed' else -1
        return success_response(rpc_id, {"cancel_time": now_ms, "transaction": str(updated['id']), "state": state})

    @staticmethod
    async def check_transaction(rpc_id, params: dict) -> dict:
        payme_id = params.get("id")
        tr = await db.get_transaction_by_payment_id(payme_id)
        if not tr: return error_response(rpc_id, -31003, "Xato")
        state = 1 if tr['status'] == 'pending' else 2
        if tr['status'] == 'cancelled': state = -2 if tr['perform_time'] else -1
        return success_response(rpc_id, {
            "create_time": int(tr['create_time']), "perform_time": int(tr['perform_time'] or 0),
            "cancel_time": int(tr['cancel_time'] or 0), "transaction": str(tr['id']), "state": state, "reason": tr['cancel_reason']
        })

    @staticmethod
    async def get_statement(rpc_id, params: dict) -> dict:
        rows = await db.get_transactions_by_time_range(params.get("from"), params.get("to"))
        return success_response(rpc_id, {"transactions": [
            {
                "id": r['payment_id'], "time": int(r['create_time']), "amount": int(r['amount'] * 100),
                "account": {"order_id": r['app_code']}, "create_time": int(r['create_time']),
                "perform_time": int(r['perform_time'] or 0), "cancel_time": int(r['cancel_time'] or 0),
                "transaction": str(r['id']), "state": 2 if r['status'] == 'completed' else (1 if r['status'] == 'pending' else -1)
            } for r in rows
        ]})
