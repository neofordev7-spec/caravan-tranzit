import os
import base64
import time
import logging
from decimal import Decimal
from aiohttp import web
from database import db

# Loglarni sozlash
logger = logging.getLogger(__name__)

# 1. KONFIGURATSIYA (Railway Variables orqali olinadi)
PAYME_MERCHANT_ID = os.getenv("PAYME_MERCHANT_ID", "")
PAYME_MERCHANT_KEY = os.getenv("PAYME_MERCHANT_KEY", "")
ADMIN_GROUP_ID = os.getenv("ADMIN_GROUP_ID") 

# 🛡 KIBERXAVFSIZLIK: Payme rasmiy IP manzillari
PAYME_IPS = ["195.158.31.134", "195.158.31.135", "195.158.28.14"]

# =============================================================
# ⚡️ DEEP LINK GENERATOR (Ilovani bittada ochish uchun)
# =============================================================
def generate_checkout_url(app_code: str, amount_uzs: Decimal) -> str:
    """
    Payme Deep Link yaratish. 
    Summani tiyinga o'tkazish majburiy (Bank standarti).
    """
    # 1. Summani tiyinga o'tkazamiz (Payme talabi)
    amount_tiyin = int(Decimal(str(amount_uzs)) * 100)
    
    # 2. Parametrlarni yig'amiz
    params = f"m={PAYME_MERCHANT_ID};ac.app_code={app_code};a={amount_tiyin}"
    
    # 3. Base64 kodlash
    encoded = base64.b64encode(params.encode()).decode()
    
    # ✅ checkout.payme.uz har qanday qurilmada ishlaydi (mobil + desktop/laptop)
    return f"https://checkout.payme.uz/{encoded}"

# =============================================================
# AUTENTIFIKATSIYA VA YORDAMCHI FUNKSIYALAR
# =============================================================
def verify_auth(request) -> bool:
    """Payme merchant kaliti bilan autentifikatsiyani tekshirish"""
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Basic "):
        return False
    try:
        decoded = base64.b64decode(auth_header[6:]).decode()
        login, password = decoded.split(":", 1)
        # Payme har doim 'paycom' yoki 'payme' loginini ishlatadi
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
        # 1. IP Tekshiruvi (Kiberxavfsizlik uchun)
        client_ip = request.headers.get("X-Forwarded-For", request.remote).split(',')[0].strip()
        if client_ip not in PAYME_IPS:
            logger.warning(f"🚫 SHUBHALI SO'ROV: IP {client_ip} urinishi!")
            return web.json_response({"error": "Forbidden IP"}, status=403)

        # 2. Auth Tekshiruvi (Merchant Key orqali)
        if not verify_auth(request):
            return web.json_response(error_response(None, -32504, "Auth xatosi"), status=200)

        try:
            body = await request.json()
            method = body.get("method", "")
            params = body.get("params", {})
            rpc_id = body.get("id")
        except Exception:
            return web.json_response(error_response(None, -32700, "JSON xatosi"), status=200)

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
            return web.json_response(error_response(rpc_id, -32601, "Metod topilmadi"), status=200)

        result = await handler(rpc_id, params)
        return web.json_response(result, status=200)

    @staticmethod
    async def check_perform_transaction(rpc_id, params: dict) -> dict:
        account = params.get("account", {})
        app_code = account.get("app_code")
        app = await db.get_application_by_code(app_code)
        if not app: return error_response(rpc_id, -31050, "Ariza topilmadi")
        if app['status'] == 'paid': return error_response(rpc_id, -31052, "Ariza allaqachon to'langan")
        return success_response(rpc_id, {"allow": True})

    @staticmethod
    async def create_transaction(rpc_id, params: dict) -> dict:
        payme_id = params.get("id")
        account = params.get("account", {})
        app_code = account.get("app_code")

        # Mavjud tranzaksiyani tekshirish
        existing = await db.get_transaction_by_payment_id(payme_id)
        if existing:
            state = 1 if existing['status'] == 'pending' else 2
            return success_response(rpc_id, {
                "create_time": int(existing['create_time']),
                "transaction": str(existing['id']),
                "state": state
            })

        app = await db.get_application_by_code(app_code)
        if not app: return error_response(rpc_id, -31050, "Ariza topilmadi")

        # Yangi tranzaksiya yaratish
        transaction = await db.create_transaction(
            user_id=app['user_id'], application_id=app['id'],
            amount=Decimal(str(params.get("amount"))) / 100, # Tiyinni so'mga o'tkazamiz
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
        from main import bot 
        payme_id = params.get("id")
        tr = await db.get_transaction_by_payment_id(payme_id)
        if not tr: return error_response(rpc_id, -31003, "Tranzaksiya topilmadi")

        if tr['status'] == 'completed':
            return success_response(rpc_id, {"perform_time": int(tr['perform_time']), "transaction": str(tr['id']), "state": 2})

        now_ms = int(time.time() * 1000)
        await db.update_transaction_status(tr['id'], 'completed', payme_id, perform_time=now_ms)
        app = await db.get_application_by_id(tr['application_id'])
        await db.update_application_status(app['app_code'], 'paid')

        # ✅ FOYDALANUVCHIGA BOTDAN XABAR
        try:
            await bot.send_message(app['user_id'], f"✅ **To'lov qabul qilindi!**\n🆔 Ariza: `{app['app_code']}`\n💰 Summa: {tr['amount']} so'm")
        except: pass

        # ✅ ADMINGA XABAR
        if ADMIN_GROUP_ID:
            try:
                await bot.send_message(ADMIN_GROUP_ID, f"💰 **Payme To'lov!**\nAriza: `{app['app_code']}`\nSumma: {tr['amount']} so'm")
            except: pass

        return success_response(rpc_id, {"perform_time": now_ms, "transaction": str(tr['id']), "state": 2})

    @staticmethod
    async def cancel_transaction(rpc_id, params: dict) -> dict:
        payme_id = params.get("id")
        reason = params.get("reason")
        tr = await db.get_transaction_by_payment_id(payme_id)
        if not tr: return error_response(rpc_id, -31003, "Xato")

        now_ms = int(time.time() * 1000)
        await db.update_transaction_status(tr['id'], 'cancelled', payme_id, cancel_time=now_ms, cancel_reason=reason)
        state = -2 if tr['status'] == 'completed' else -1
        return success_response(rpc_id, {"cancel_time": now_ms, "transaction": str(tr['id']), "state": state})

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
                "account": {"app_code": r['app_code']}, "create_time": int(r['create_time']),
                "perform_time": int(r['perform_time'] or 0), "cancel_time": int(r['cancel_time'] or 0),
                "transaction": str(r['id']), "state": 2 if r['status'] == 'completed' else 1
            } for r in rows if r['payment_provider'] == 'payme'
        ]})
