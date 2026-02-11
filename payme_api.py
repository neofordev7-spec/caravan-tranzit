"""
Payme.uz Payment API Integration

Payme Merchant API (JSON-RPC 2.0):
- CheckPerformTransaction
- CreateTransaction
- PerformTransaction
- CancelTransaction
- CheckTransaction
- GetStatement

Payme Checkout URL generation for user payments.
"""
import os
import base64
import time
import hashlib
import json
import logging
from decimal import Decimal
from aiohttp import web
from database import db

logger = logging.getLogger(__name__)

# Payme credentials (from environment variables)
PAYME_MERCHANT_ID = os.getenv("PAYME_MERCHANT_ID", "")
PAYME_MERCHANT_KEY = os.getenv("PAYME_MERCHANT_KEY", "")

# Payme URLs
PAYME_CHECKOUT_URL = "https://checkout.paycom.uz"

# Payme error codes
PAYME_ERRORS = {
    -31001: "Noto'g'ri summa",
    -31003: "Tranzaksiya topilmadi",
    -31004: "Noto'g'ri holatdagi tranzaksiya",
    -31005: "Tranzaksiyani bajarib bo'lmaydi",
    -31007: "Tranzaksiya bekor qilish mumkin emas",
    -31008: "Tranzaksiya bajarildi, bekor qilib bo'lmaydi",
    -31050: "Buyurtma topilmadi",
    -31051: "Buyurtma narxi noto'g'ri",
    -31052: "Buyurtma statusini o'zgartirish mumkin emas",
    -31099: "Serverda xatolik"
}


def generate_checkout_url(order_id: str, amount_uzs: Decimal) -> str:
    """
    Payme checkout URL yaratish

    Args:
        order_id: Ariza kodi (app_code)
        amount_uzs: To'lov summasi UZS da

    Returns:
        Payme checkout URL
    """
    # Payme summani tiyinda qabul qiladi (1 UZS = 100 tiyin)
    amount_tiyin = int(amount_uzs * 100)

    # Parametrlarni tayyorlaymiz
    params = f"m={PAYME_MERCHANT_ID};ac.order_id={order_id};a={amount_tiyin}"

    # Base64 encode
    encoded = base64.b64encode(params.encode()).decode()

    return f"{PAYME_CHECKOUT_URL}/{encoded}"


def verify_auth(request) -> bool:
    """
    Payme so'rovining autentikatsiyasini tekshirish
    Basic Auth: login=Paycom, password=MERCHANT_KEY
    """
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Basic "):
        return False

    try:
        decoded = base64.b64decode(auth_header[6:]).decode()
        login, password = decoded.split(":", 1)
        return login == "Paycom" and password == PAYME_MERCHANT_KEY
    except Exception:
        return False


def error_response(rpc_id, code: int, message_uz: str, message_ru: str = "", message_en: str = ""):
    """JSON-RPC error response"""
    return {
        "jsonrpc": "2.0",
        "id": rpc_id,
        "error": {
            "code": code,
            "message": {
                "uz": message_uz,
                "ru": message_ru or message_uz,
                "en": message_en or message_uz
            }
        }
    }


def success_response(rpc_id, result: dict):
    """JSON-RPC success response"""
    return {
        "jsonrpc": "2.0",
        "id": rpc_id,
        "result": result
    }


class PaymeAPI:
    """Payme Merchant API handler (JSON-RPC 2.0)"""

    @staticmethod
    async def handle_request(request: web.Request) -> web.Response:
        """
        Payme dan kelgan JSON-RPC so'rovlarni qayta ishlash
        """
        # Auth tekshirish
        if not verify_auth(request):
            return web.json_response(
                error_response(None, -32504, "Autentifikatsiya xatosi", "Ошибка аутентификации", "Authentication error"),
                status=200
            )

        try:
            body = await request.json()
        except Exception:
            return web.json_response(
                error_response(None, -32700, "JSON parse xatosi", "Ошибка парсинга JSON", "JSON parse error"),
                status=200
            )

        rpc_id = body.get("id")
        method = body.get("method", "")
        params = body.get("params", {})

        logger.info(f"Payme request: method={method}, params={params}")

        # Metodlarni yo'naltiramiz
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
            return web.json_response(
                error_response(rpc_id, -32601, "Metod topilmadi", "Метод не найден", "Method not found"),
                status=200
            )

        result = await handler(rpc_id, params)
        return web.json_response(result, status=200)

    @staticmethod
    async def check_perform_transaction(rpc_id, params: dict) -> dict:
        """
        Tranzaksiya bajarilishi mumkinligini tekshirish
        Payme to'lovni boshlashdan oldin chaqiradi
        """
        try:
            account = params.get("account", {})
            order_id = account.get("order_id")
            amount = params.get("amount")

            if not order_id:
                return error_response(rpc_id, -31050,
                    "Buyurtma topilmadi",
                    "Заказ не найден",
                    "Order not found")

            # Bazadan arizani topamiz
            app = await db.get_application_by_code(order_id)
            if not app:
                return error_response(rpc_id, -31050,
                    "Buyurtma topilmadi",
                    "Заказ не найден",
                    "Order not found")

            # Ariza statusini tekshiramiz
            if app['status'] == 'paid':
                return error_response(rpc_id, -31052,
                    "Buyurtma allaqachon to'langan",
                    "Заказ уже оплачен",
                    "Order already paid")

            if app['status'] not in ('new', 'priced', 'processing'):
                return error_response(rpc_id, -31052,
                    "Buyurtma statusini o'zgartirish mumkin emas",
                    "Невозможно изменить статус заказа",
                    "Cannot change order status")

            # Narxni tekshiramiz (tiyinda)
            if app['price']:
                expected_amount = int(Decimal(str(app['price'])) * 100)
                if amount != expected_amount:
                    return error_response(rpc_id, -31001,
                        f"Noto'g'ri summa. Kutilgan: {expected_amount}",
                        f"Неверная сумма. Ожидалось: {expected_amount}",
                        f"Invalid amount. Expected: {expected_amount}")

            return success_response(rpc_id, {"allow": True})

        except Exception as e:
            logger.error(f"CheckPerformTransaction error: {e}")
            return error_response(rpc_id, -31099,
                "Serverda xatolik",
                "Ошибка сервера",
                "Server error")

    @staticmethod
    async def create_transaction(rpc_id, params: dict) -> dict:
        """
        Yangi tranzaksiya yaratish
        """
        try:
            payme_id = params.get("id")
            account = params.get("account", {})
            order_id = account.get("order_id")
            amount = params.get("amount")
            create_time = params.get("time")

            if not order_id:
                return error_response(rpc_id, -31050,
                    "Buyurtma topilmadi",
                    "Заказ не найден",
                    "Order not found")

            # Arizani tekshiramiz
            app = await db.get_application_by_code(order_id)
            if not app:
                return error_response(rpc_id, -31050,
                    "Buyurtma topilmadi",
                    "Заказ не найден",
                    "Order not found")

            if app['status'] == 'paid':
                return error_response(rpc_id, -31052,
                    "Buyurtma allaqachon to'langan",
                    "Заказ уже оплачен",
                    "Order already paid")

            # Bazada tranzaksiya yaratamiz
            amount_uzs = Decimal(str(amount)) / 100
            transaction = await db.create_transaction(
                user_id=app['user_id'],
                application_id=app['id'],
                amount=amount_uzs,
                trans_type='card_payment',
                payment_provider='payme'
            )

            # Payme transaction ID ni saqlaymiz
            if transaction:
                await db.update_transaction_status(
                    transaction['id'],
                    'pending',
                    payme_id
                )

            now_ms = int(time.time() * 1000)

            return success_response(rpc_id, {
                "create_time": now_ms,
                "transaction": str(transaction['id'] if transaction else 0),
                "state": 1  # 1 = created
            })

        except Exception as e:
            logger.error(f"CreateTransaction error: {e}")
            return error_response(rpc_id, -31099,
                "Serverda xatolik",
                "Ошибка сервера",
                "Server error")

    @staticmethod
    async def perform_transaction(rpc_id, params: dict) -> dict:
        """
        Tranzaksiyani bajarish (to'lovni tasdiqlash)
        """
        try:
            payme_id = params.get("id")

            # Payme ID bo'yicha tranzaksiyani topamiz
            transaction = await db.get_transaction_by_payment_id(payme_id)
            if not transaction:
                return error_response(rpc_id, -31003,
                    "Tranzaksiya topilmadi",
                    "Транзакция не найдена",
                    "Transaction not found")

            if transaction['status'] == 'completed':
                return success_response(rpc_id, {
                    "perform_time": int(time.time() * 1000),
                    "transaction": str(transaction['id']),
                    "state": 2  # 2 = completed
                })

            if transaction['status'] != 'pending':
                return error_response(rpc_id, -31004,
                    "Noto'g'ri holatdagi tranzaksiya",
                    "Транзакция в неверном состоянии",
                    "Transaction in invalid state")

            # Tranzaksiyani "completed" ga o'tkazamiz
            await db.update_transaction_status(transaction['id'], 'completed', payme_id)

            # Ariza statusini "paid" ga o'tkazamiz
            if transaction['application_id']:
                app = await db.get_application_by_id(transaction['application_id'])
                if app:
                    await db.update_application_status(app['app_code'], 'paid')

                    # Referral reward tekshiramiz
                    referrer_id = await db.mark_referral_reward(transaction['user_id'])

            now_ms = int(time.time() * 1000)
            return success_response(rpc_id, {
                "perform_time": now_ms,
                "transaction": str(transaction['id']),
                "state": 2  # 2 = completed
            })

        except Exception as e:
            logger.error(f"PerformTransaction error: {e}")
            return error_response(rpc_id, -31099,
                "Serverda xatolik",
                "Ошибка сервера",
                "Server error")

    @staticmethod
    async def cancel_transaction(rpc_id, params: dict) -> dict:
        """
        Tranzaksiyani bekor qilish
        """
        try:
            payme_id = params.get("id")
            reason = params.get("reason")

            transaction = await db.get_transaction_by_payment_id(payme_id)
            if not transaction:
                return error_response(rpc_id, -31003,
                    "Tranzaksiya topilmadi",
                    "Транзакция не найдена",
                    "Transaction not found")

            if transaction['status'] == 'cancelled':
                return success_response(rpc_id, {
                    "cancel_time": int(time.time() * 1000),
                    "transaction": str(transaction['id']),
                    "state": -1  # -1 = cancelled before perform
                })

            if transaction['status'] == 'completed':
                # Bajarilgan tranzaksiyani bekor qilish
                await db.update_transaction_status(transaction['id'], 'cancelled', payme_id)

                if transaction['application_id']:
                    app = await db.get_application_by_id(transaction['application_id'])
                    if app:
                        await db.update_application_status(app['app_code'], 'new')

                return success_response(rpc_id, {
                    "cancel_time": int(time.time() * 1000),
                    "transaction": str(transaction['id']),
                    "state": -2  # -2 = cancelled after perform
                })

            # Pending tranzaksiyani bekor qilish
            await db.update_transaction_status(transaction['id'], 'cancelled', payme_id)

            return success_response(rpc_id, {
                "cancel_time": int(time.time() * 1000),
                "transaction": str(transaction['id']),
                "state": -1
            })

        except Exception as e:
            logger.error(f"CancelTransaction error: {e}")
            return error_response(rpc_id, -31099,
                "Serverda xatolik",
                "Ошибка сервера",
                "Server error")

    @staticmethod
    async def check_transaction(rpc_id, params: dict) -> dict:
        """
        Tranzaksiya holatini tekshirish
        """
        try:
            payme_id = params.get("id")

            transaction = await db.get_transaction_by_payment_id(payme_id)
            if not transaction:
                return error_response(rpc_id, -31003,
                    "Tranzaksiya topilmadi",
                    "Транзакция не найдена",
                    "Transaction not found")

            state_map = {
                'pending': 1,
                'completed': 2,
                'cancelled': -1,
                'failed': -1,
            }

            state = state_map.get(transaction['status'], 1)
            now_ms = int(time.time() * 1000)

            return success_response(rpc_id, {
                "create_time": now_ms,
                "perform_time": now_ms if state == 2 else 0,
                "cancel_time": now_ms if state < 0 else 0,
                "transaction": str(transaction['id']),
                "state": state,
                "reason": None
            })

        except Exception as e:
            logger.error(f"CheckTransaction error: {e}")
            return error_response(rpc_id, -31099,
                "Serverda xatolik",
                "Ошибка сервера",
                "Server error")

    @staticmethod
    async def get_statement(rpc_id, params: dict) -> dict:
        """
        Belgilangan vaqt oralig'idagi tranzaksiyalar ro'yxati
        """
        try:
            # Hozircha bo'sh ro'yxat qaytaramiz
            return success_response(rpc_id, {
                "transactions": []
            })
        except Exception as e:
            logger.error(f"GetStatement error: {e}")
            return error_response(rpc_id, -31099,
                "Serverda xatolik",
                "Ошибка сервера",
                "Server error")
