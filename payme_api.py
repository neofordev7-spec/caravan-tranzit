import os
import base64
import time
import logging
from decimal import Decimal
from aiohttp import web
from database import db

# Loglarni sozlash
logger = logging.getLogger(__name__)

# 1. KONFIGURATSIYA (Railway Variables'dan olinadi)
PAYME_MERCHANT_KEY = os.getenv("PAYME_MERCHANT_KEY", "")
ADMIN_GROUP_ID = os.getenv("ADMIN_GROUP_ID") # Admin guruh ID raqami

def verify_auth(request) -> bool:
    """Payme autentifikatsiyasini tekshirish (Basic Auth)"""
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Basic "):
        return False
    try:
        decoded = base64.b64decode(auth_header[6:]).decode()
        login, password = decoded.split(":", 1)
        # Payme 'paycom' loginini ishlatadi
        return login.lower() in ["paycom", "payme"] and password == PAYME_MERCHANT_KEY
    except Exception:
        return False

def error_response(rpc_id, code: int, message_uz: str):
    """Xato javobi formati"""
    return {
        "jsonrpc": "2.0",
        "id": rpc_id,
        "error": {
            "code": code,
            "message": {"uz": message_uz, "ru": message_uz, "en": message_uz}
        }
    }

def success_response(rpc_id, result: dict):
    """Muvaffaqiyatli javob formati"""
    return {"jsonrpc": "2.0", "id": rpc_id, "result": result}

class PaymeAPI:
    @staticmethod
    async def handle_request(request: web.Request) -> web.Response:
        """Payme'dan kelgan so'rovlarni qabul qilish"""
        if not verify_auth(request):
            return web.json_response(error_response(None, -32504, "Autentifikatsiya xatosi"), status=200)

        try:
            body = await request.json()
        except Exception:
            return web.json_response(error_response(None, -32700, "JSON parse xatosi"), status=200)

        rpc_id = body.get("id")
        method = body.get("method", "")
        params = body.get("params", {})

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
        """To'lov qilish mumkinligini tekshirish"""
        account = params.get("account", {})
        order_id = account.get("order_id")
        amount = params.get("amount")

        app = await db.get_application_by_code(order_id)
        if not app:
            return error_response(rpc_id, -31050, "Ariza topilmadi")
        
        if app['status'] == 'paid':
            return error_response(rpc_id, -31052, "Ariza allaqachon to'langan")

        # Summani solishtirish (tiyinlarda)
        expected_amount = int(Decimal(str(app['price'])) * 100)
        if amount != expected_amount:
            return error_response(rpc_id, -31001, "Noto'g'ri summa")

        return success_response(rpc_id, {"allow": True})

    @staticmethod
    async def create_transaction(rpc_id, params: dict) -> dict:
        """Yangi tranzaksiya yaratish"""
        payme_id = params.get("id")
        payme_time = int(params.get("time"))
        account = params.get("account", {})
        order_id = account.get("order_id")
        amount = params.get("amount")

        existing = await db.get_transaction_by_payment_id(payme_id)
        if existing:
            state = 1 if existing['status'] == 'pending' else 2
            return success_response(rpc_id, {
                "create_time": int(existing['create_time']),
                "transaction": str(existing['id']),
                "state": state
            })

        app = await db.get_application_by_code(order_id)
        if not app:
            return error_response(rpc_id, -31050, "Ariza topilmadi")

        transaction = await db.create_transaction(
            user_id=app['user_id'],
            application_id=app['id'],
            amount=Decimal(str(amount)) / 100,
            trans_type='card_payment',
            payment_provider='payme',
            payment_id=payme_id,
            create_time=payme_time
        )

        return success_response(rpc_id, {
            "create_time": int(transaction['create_time']),
            "transaction": str(transaction['id']),
            "state": 1
        })

    @staticmethod
    async def perform_transaction(rpc_id, params: dict) -> dict:
        """To'lovni yakunlash va BOTDA AVTOMATIK XABAR BERISH"""
        try:
            # Botni main faylidan import qilamiz
            from main import bot 

            payme_id = params.get("id")
            transaction = await db.get_transaction_by_payment_id(payme_id)

            if not transaction:
                return error_response(rpc_id, -31003, "Tranzaksiya topilmadi")

            if transaction['status'] == 'completed':
                return success_response(rpc_id, {
                    "perform_time": int(transaction['perform_time']),
                    "transaction": str(transaction['id']),
                    "state": 2
                })

            # 1. Bazani yangilash
            now_ms = int(time.time() * 1000)
            updated = await db.update_transaction_status(
                transaction['id'], 'completed', payme_id, perform_time=now_ms
            )
            app = await db.get_application_by_id(transaction['application_id'])
            await db.update_application_status(app['app_code'], 'paid')

            # 2. 🔥 FOYDALANUVCHIGA AVTOMATIK XABAR
            user_msg = (
                f"✅ **To'lov muvaffaqiyatli qabul qilindi!**\n\n"
                f"📝 Ariza raqami: `{app['app_code']}`\n"
                f"💰 To'langan summa: {transaction['amount']} so'm\n"
                f"📊 Holati: **To'langan**"
            )
            try:
                await bot.send_message(chat_id=app['user_id'], text=user_msg)
            except Exception as e:
                logger.error(f"Userga xabar ketmadi: {e}")

            # 3. 🔥 ADMINGA AVTOMATIK XABAR
            if ADMIN_GROUP_ID:
                admin_msg = (
                    f"💰 **Yangi to'lov kelib tushdi!**\n\n"
                    f"📌 Ariza: `{app['app_code']}`\n"
                    f"💵 Summa: {transaction['amount']} so'm\n"
                    f"👤 Foydalanuvchi ID: `{app['user_id']}`"
                )
                try:
                    await bot.send_message(chat_id=ADMIN_GROUP_ID, text=admin_msg)
                except Exception as e:
                    logger.error(f"Adminga xabar ketmadi: {e}")

            return success_response(rpc_id, {
                "perform_time": int(updated['perform_time']),
                "transaction": str(updated['id']),
                "state": 2
            })
        except Exception as e:
            logger.error(f"Perform error: {e}")
            return error_response(rpc_id, -31099, "Serverda xatolik")

    @staticmethod
    async def cancel_transaction(rpc_id, params: dict) -> dict:
        """Tranzaksiyani bekor qilish"""
        payme_id = params.get("id")
        reason = params.get("reason")
        transaction = await db.get_transaction_by_payment_id(payme_id)

        if not transaction:
            return error_response(rpc_id, -31003, "Tranzaksiya topilmadi")

        if transaction['status'] == 'cancelled':
            state = -2 if transaction['perform_time'] else -1
            return success_response(rpc_id, {
                "cancel_time": int(transaction['cancel_time']),
                "transaction": str(transaction['id']),
                "state": state
            })

        now_ms = int(time.time() * 1000)
        updated = await db.update_transaction_status(
            transaction['id'], 'cancelled', payme_id, 
            cancel_time=now_ms, cancel_reason=reason
        )

        state = -2 if transaction['status'] == 'completed' else -1
        return success_response(rpc_id, {
            "cancel_time": int(updated['cancel_time']),
            "transaction": str(updated['id']),
            "state": state
        })

    @staticmethod
    async def check_transaction(rpc_id, params: dict) -> dict:
        """Tranzaksiya holatini tekshirish"""
        payme_id = params.get("id")
        tr = await db.get_transaction_by_payment_id(payme_id)

        if not tr:
            return error_response(rpc_id, -31003, "Tranzaksiya topilmadi")

        state_map = {'pending': 1, 'completed': 2, 'cancelled': -1}
        state = state_map.get(tr['status'], 1)
        if state == -1 and tr['perform_time']: state = -2

        return success_response(rpc_id, {
            "create_time": int(tr['create_time']),
            "perform_time": int(tr['perform_time'] or 0),
            "cancel_time": int(tr['cancel_time'] or 0),
            "transaction": str(tr['id']),
            "state": state,
            "reason": tr['cancel_reason']
        })

    @staticmethod
    async def get_statement(rpc_id, params: dict) -> dict:
        """Vaqt oralig'i bo'yicha hisobot"""
        rows = await db.get_transactions_by_time_range(params.get("from"), params.get("to"))
        transactions = []
        for r in rows:
            state = 1 if r['status'] == 'pending' else 2
            if r['status'] == 'cancelled': state = -2 if r['perform_time'] else -1
            
            transactions.append({
                "id": r['payment_id'],
                "time": int(r['create_time']),
                "amount": int(r['amount'] * 100),
                "account": {"order_id": r['app_code']},
                "create_time": int(r['create_time']),
                "perform_time": int(r['perform_time'] or 0),
                "cancel_time": int(r['cancel_time'] or 0),
                "transaction": str(r['id']),
                "state": state,
                "reason": r['cancel_reason'],
            })
        return success_response(rpc_id, {"transactions": transactions})
