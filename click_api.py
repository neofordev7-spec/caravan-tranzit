"""
Click.uz Payment API Integration
"""
import os
import hashlib
import aiohttp
from decimal import Decimal

# Click API credentials (from environment variables)
CLICK_SERVICE_ID = int(os.getenv("CLICK_SERVICE_ID", "0"))
CLICK_MERCHANT_ID = int(os.getenv("CLICK_MERCHANT_ID", "0"))
CLICK_MERCHANT_USER_ID = int(os.getenv("CLICK_MERCHANT_USER_ID", "0"))
CLICK_SECRET_KEY = os.getenv("CLICK_SECRET_KEY", "")

# Click API URLs
CLICK_API_URL = "https://api.click.uz/v2/merchant"
CLICK_PREPARE_URL = f"{CLICK_API_URL}/prepare"
CLICK_COMPLETE_URL = f"{CLICK_API_URL}/complete"


class ClickAPI:
    """Click.uz payment API handler"""

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

        # TODO: Check if transaction already exists in database
        # TODO: Verify merchant_trans_id (application code) exists
        # TODO: Verify amount matches

        return {
            "click_trans_id": click_trans_id,
            "merchant_trans_id": merchant_trans_id,
            "merchant_prepare_id": merchant_trans_id,  # Your internal transaction ID
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
            # Payment failed on Click side
            return {
                "error": error,
                "error_note": "Payment cancelled"
            }

        # TODO: Mark transaction as completed in database
        # TODO: Update application status
        # TODO: Send notification to user

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
        # Click payment URL format:
        # https://my.click.uz/services/pay?service_id=SERVICE_ID&merchant_id=MERCHANT_ID&amount=AMOUNT&transaction_param=APP_CODE&return_url=RETURN_URL

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
