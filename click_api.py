"""
Click.uz Payment API Integration
"""
import os
import hashlib
import logging
from decimal import Decimal
from database import db

logger = logging.getLogger(__name__)

# Click API credentials (from environment variables)
CLICK_SERVICE_ID = int(os.getenv("CLICK_SERVICE_ID", "0"))
CLICK_MERCHANT_ID = int(os.getenv("CLICK_MERCHANT_ID", "0"))
CLICK_MERCHANT_USER_ID = int(os.getenv("CLICK_MERCHANT_USER_ID", "0"))
CLICK_SECRET_KEY = os.getenv("CLICK_SECRET_KEY", "")


class ClickAPI:
    """Click.uz payment API handler"""

    # Bot referensi - web server tomonidan o'rnatiladi
    bot = None

    @classmethod
    def set_bot(cls, bot_instance):
        """Bot referensini saqlash"""
        cls.bot = bot_instance

    @staticmethod
    def generate_signature(
        click_trans_id: int,
        service_id: int,
        secret_key: str,
        merchant_trans_id: str,
        amount: float,
        action: int,
        sign_time: str
    ) -> str:
        """
        Generate signature for Click API

        SHA1(click_trans_id + service_id + secret_key + merchant_trans_id + amount + action + sign_time)
        """
        signature_string = f"{click_trans_id}{service_id}{secret_key}{merchant_trans_id}{amount}{action}{sign_time}"
        return hashlib.sha1(signature_string.encode()).hexdigest()

    @staticmethod
    async def prepare_payment(
        click_trans_id: int,
        merchant_trans_id: str,
        amount: float,
        sign_time: str,
        sign_string: str
    ) -> dict:
        """
        Prepare payment (verify transaction)

        Returns: dict with status code and message
        """
        # Verify signature
        expected_signature = ClickAPI.generate_signature(
            click_trans_id,
            CLICK_SERVICE_ID,
            CLICK_SECRET_KEY,
            merchant_trans_id,
            amount,
            0,  # prepare action
            sign_time
        )

        if sign_string != expected_signature:
            return {
                "error": -1,
                "error_note": "SIGN CHECK FAILED!"
            }

        # Arizani bazadan tekshiramiz
        app = await db.get_application_by_code(merchant_trans_id)
        if not app:
            return {
                "error": -5,
                "error_note": "Order not found"
            }

        # Ariza allaqachon to'langanmi?
        if app['status'] == 'paid':
            return {
                "error": -4,
                "error_note": "Already paid"
            }

        # Narxni tekshiramiz
        if app['price']:
            expected_amount = float(app['price'])
            if abs(amount - expected_amount) > 1:  # 1 UZS tolerans
                return {
                    "error": -2,
                    "error_note": f"Incorrect amount. Expected: {expected_amount}"
                }

        # Tranzaksiya yaratamiz
        try:
            transaction = await db.create_transaction(
                user_id=app['user_id'],
                application_id=app['id'],
                amount=Decimal(str(amount)),
                trans_type='card_payment',
                payment_provider='click'
            )

            if transaction:
                await db.update_transaction_status(
                    transaction['id'],
                    'pending',
                    str(click_trans_id)
                )
        except Exception as e:
            logger.error(f"Click prepare DB error: {e}")

        return {
            "click_trans_id": click_trans_id,
            "merchant_trans_id": merchant_trans_id,
            "merchant_prepare_id": merchant_trans_id,
            "error": 0,
            "error_note": "Success"
        }

    @staticmethod
    async def complete_payment(
        click_trans_id: int,
        merchant_trans_id: str,
        merchant_prepare_id: str,
        amount: float,
        sign_time: str,
        sign_string: str,
        error: int
    ) -> dict:
        """
        Complete payment (confirm transaction)

        Returns: dict with status code and message
        """
        # Verify signature
        expected_signature = ClickAPI.generate_signature(
            click_trans_id,
            CLICK_SERVICE_ID,
            CLICK_SECRET_KEY,
            merchant_trans_id,
            amount,
            1,  # complete action
            sign_time
        )

        if sign_string != expected_signature:
            return {
                "error": -1,
                "error_note": "SIGN CHECK FAILED!"
            }

        if error < 0:
            # Click tomonidan to'lov bekor qilindi
            try:
                transaction = await db.get_transaction_by_payment_id(str(click_trans_id))
                if transaction:
                    await db.update_transaction_status(transaction['id'], 'cancelled', str(click_trans_id))
            except Exception as e:
                logger.error(f"Click cancel DB error: {e}")

            return {
                "error": error,
                "error_note": "Payment cancelled"
            }

        # Tranzaksiyani completed ga o'tkazamiz
        try:
            transaction = await db.get_transaction_by_payment_id(str(click_trans_id))
            if transaction:
                await db.update_transaction_status(transaction['id'], 'completed', str(click_trans_id))

                # Ariza statusini paid ga o'tkazamiz
                if transaction['application_id']:
                    app = await db.get_application_by_id(transaction['application_id'])
                    if app:
                        await db.update_application_status(app['app_code'], 'paid')

                        # Referral reward tekshiramiz
                        await db.mark_referral_reward(transaction['user_id'])

                        # Bot orqali xabar yuboramiz
                        if ClickAPI.bot:
                            try:
                                from payment_handlers import notify_payment_success
                                amount_uzs = Decimal(str(transaction['amount']))
                                await notify_payment_success(ClickAPI.bot, app['app_code'], amount_uzs, 'click')
                            except Exception as notify_err:
                                logger.error(f"Click payment notification error: {notify_err}")
        except Exception as e:
            logger.error(f"Click complete DB error: {e}")

        return {
            "click_trans_id": click_trans_id,
            "merchant_trans_id": merchant_trans_id,
            "merchant_confirm_id": merchant_trans_id,
            "error": 0,
            "error_note": "Success"
        }

    @staticmethod
    def generate_payment_url(
        app_code: str,
        amount: Decimal,
        return_url: str = "https://t.me/caravan_tranzit_bot"
    ) -> str:
        """
        Generate Click payment URL for user

        Args:
            app_code: Application code (merchant_trans_id)
            amount: Payment amount in UZS
            return_url: URL to return after payment

        Returns: Click payment URL
        """
        base_url = "https://my.click.uz/services/pay"
        params = {
            "service_id": CLICK_SERVICE_ID,
            "merchant_id": CLICK_MERCHANT_ID,
            "amount": float(amount),
            "transaction_param": app_code,
            "return_url": return_url
        }

        # Build query string
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"{base_url}?{query_string}"


# Click error codes
CLICK_ERROR_CODES = {
    -1: "SIGN CHECK FAILED!",
    -2: "Incorrect parameter amount",
    -3: "Action not found",
    -4: "Already paid",
    -5: "User does not exist",
    -6: "Transaction does not exist",
    -7: "Failed to update user",
    -8: "Error in request from click",
    -9: "Transaction cancelled"
}
