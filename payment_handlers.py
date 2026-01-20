"""
PAYMENT HANDLERS
To'lovlarni qayta ishlash:
- Telegram Payments API (Click/Payme)
- Tangalar bilan to'lash
- To'lov tarixini saqlash
"""
from decimal import Decimal
from aiogram import Router, F, Bot
from aiogram.types import (
    CallbackQuery, Message, LabeledPrice,
    PreCheckoutQuery, InlineKeyboardMarkup, InlineKeyboardButton
)
from database import db

router = Router()

# Payment provider token (Click/Payme uchun)
# MUHIM: O'z provideringizning tokenini kiriting!
PAYMENT_PROVIDER_TOKEN = ""  # TODO: Add your payment provider token

# =========================================================================
# PAYMENT SELECTION
# =========================================================================

@router.callback_query(F.data.startswith("pay_click_"))
async def handle_pay_click(call: CallbackQuery, bot: Bot):
    """
    Click/Payme orqali to'lash
    """
    try:
        app_code = call.data.split("_")[2]

        # Arizani olamiz
        app = await db.get_application_by_code(app_code)
        if not app:
            await call.answer("❌ Ariza topilmadi!", show_alert=True)
            return

        price = app['price']
        if not price:
            await call.answer("❌ Narx belgilanmagan!", show_alert=True)
            return

        # Telegram Invoice yaratamiz
        await send_telegram_invoice(bot, call.from_user.id, app_code, price)

        await call.answer("✅ To'lov sahifasi yuborildi!")

    except Exception as e:
        print(f"❌ Pay click error: {e}")
        await call.answer("❌ Xatolik!", show_alert=True)


@router.callback_query(F.data.startswith("pay_coins_"))
async def handle_pay_coins(call: CallbackQuery, bot: Bot):
    """
    Tangalar bilan to'lash (35,000 tangalar = 1 xizmat)
    """
    try:
        app_code = call.data.split("_")[2]

        # Arizani olamiz
        app = await db.get_application_by_code(app_code)
        if not app:
            await call.answer("❌ Ariza topilmadi!", show_alert=True)
            return

        # Foydalanuvchi balansini tekshiramiz
        user = await db.get_user(call.from_user.id)
        balance = user['balance']

        if balance < 35000:
            await call.answer(
                f"❌ Yetarli tangalar yo'q!\n\n"
                f"Sizda: {balance:,.0f} tanga\n"
                f"Kerak: 35,000 tanga",
                show_alert=True
            )
            return

        # Tasdiqni so'raymiz
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"confirm_coins_{app_code}")],
            [InlineKeyboardButton(text="❌ Bekor qilish", callback_data=f"cancel_payment_{app_code}")]
        ])

        await call.message.edit_text(
            f"💰 **Tangalar bilan to'lash**\n\n"
            f"🆔 Ariza: `{app_code}`\n"
            f"💎 Olinadi: **35,000 tanga**\n"
            f"💰 Qoladi: **{balance - 35000:,.0f} tanga**\n\n"
            f"Tasdiqlaysizmi?",
            reply_markup=kb,
            parse_mode="Markdown"
        )

    except Exception as e:
        print(f"❌ Pay coins error: {e}")
        await call.answer("❌ Xatolik!", show_alert=True)


@router.callback_query(F.data.startswith("confirm_coins_"))
async def handle_confirm_coins(call: CallbackQuery, bot: Bot):
    """
    Tangalar bilan to'lashni tasdiqlash
    """
    try:
        app_code = call.data.split("_")[2]

        # Arizani olamiz
        app = await db.get_application_by_code(app_code)
        if not app:
            await call.answer("❌ Ariza topilmadi!", show_alert=True)
            return

        # Balansni tekshiramiz va kamaytiramiz
        user = await db.get_user(call.from_user.id)
        balance = user['balance']

        if balance < 35000:
            await call.answer("❌ Yetarli tangalar yo'q!", show_alert=True)
            return

        # Tangalarni kamaytiramiz
        await db.update_user_balance(call.from_user.id, Decimal('-35000.00'))

        # Ariza statusini yangilaymiz
        await db.update_application_status(app_code, 'paid')

        # Tranzaksiyani saqlaymiz
        await db.create_transaction(
            user_id=call.from_user.id,
            application_id=app['id'],
            amount=35000,
            trans_type='coins_payment',
            payment_provider='internal'
        )

        # Foydalanuvchiga xabar
        await call.message.edit_text(
            f"✅ **TO'LOV MUVAFFAQIYATLI!**\n\n"
            f"🆔 Ariza: `{app_code}`\n"
            f"💰 To'landi: **35,000 tanga**\n"
            f"💎 Qoldiq: **{balance - 35000:,.0f} tanga**\n\n"
            f"📦 Tez orada hujjatlaringizni olasiz!",
            parse_mode="Markdown"
        )

        # Admin guruhga xabar
        from admin_handlers import ADMIN_GROUP_ID
        await bot.send_message(
            ADMIN_GROUP_ID,
            f"✅ **TO'LOV QABUL QILINDI (TANGALAR)**\n\n"
            f"🆔 Ariza: `{app_code}`\n"
            f"👤 User: {user['full_name']}\n"
            f"💰 Summa: 35,000 tanga",
            parse_mode="Markdown"
        )

        # Referral reward tekshiramiz
        referrer_id = await db.mark_referral_reward(call.from_user.id)
        if referrer_id:
            await bot.send_message(
                referrer_id,
                f"🎁 **MUKOFOT!**\n\n"
                f"Do'stingiz xizmatdan foydalandi!\n"
                f"💰 +17,500 tanga qo'shildi!",
                parse_mode="Markdown"
            )

    except Exception as e:
        print(f"❌ Confirm coins error: {e}")
        await call.answer("❌ Xatolik!", show_alert=True)


@router.callback_query(F.data.startswith("cancel_payment_"))
async def handle_cancel_payment(call: CallbackQuery):
    """
    To'lovni bekor qilish
    """
    await call.message.delete()
    await call.answer("Bekor qilindi.")


# =========================================================================
# TELEGRAM PAYMENTS API
# =========================================================================

async def send_telegram_invoice(bot: Bot, user_id: int, app_code: str, amount: Decimal):
    """
    Telegram Invoice yuborish (Click/Payme integratsiyasi)
    """
    try:
        # Invoice ma'lumotlarini tayyorlaymiz
        prices = [LabeledPrice(label=f"Deklaratsiya ({app_code})", amount=int(amount * 100))]

        await bot.send_invoice(
            chat_id=user_id,
            title="Bojxona deklaratsiyasi",
            description=f"Ariza kodi: {app_code}",
            payload=f"app_{app_code}",
            provider_token=PAYMENT_PROVIDER_TOKEN,
            currency="UZS",
            prices=prices,
            start_parameter=f"pay_{app_code}",
            photo_url="https://via.placeholder.com/400x200.png?text=MYBOJXONA",
            photo_size=400,
            photo_width=400,
            photo_height=200,
            need_name=False,
            need_phone_number=False,
            need_email=False,
            need_shipping_address=False,
            is_flexible=False
        )

    except Exception as e:
        print(f"❌ Send invoice error: {e}")


@router.pre_checkout_query()
async def pre_checkout_handler(pre_checkout: PreCheckoutQuery):
    """
    To'lovni tasdiqlash (Pre-checkout)
    """
    # Har doim tasdiqlaymiz (Qo'shimcha tekshiruvlar shu yerda bo'lishi mumkin)
    await pre_checkout.answer(ok=True)


@router.message(F.successful_payment)
async def successful_payment_handler(message: Message, bot: Bot):
    """
    Muvaffaqiyatli to'lov qayta ishlash
    """
    try:
        payment = message.successful_payment

        # Payload dan app_code ni olamiz
        payload = payment.invoice_payload  # Format: "app_<code>"
        app_code = payload.split("_")[1]

        # Arizani olamiz
        app = await db.get_application_by_code(app_code)
        if not app:
            await message.answer("❌ Ariza topilmadi!")
            return

        # Ariza statusini yangilaymiz
        await db.update_application_status(app_code, 'paid')

        # Tranzaksiyani saqlaymiz
        await db.create_transaction(
            user_id=message.from_user.id,
            application_id=app['id'],
            amount=Decimal(payment.total_amount) / 100,
            trans_type='card_payment',
            payment_provider=payment.provider_payment_charge_id
        )

        # Foydalanuvchiga xabar
        await message.answer(
            f"✅ **TO'LOV MUVAFFAQIYATLI!**\n\n"
            f"🆔 Ariza: `{app_code}`\n"
            f"💰 To'langan: {payment.total_amount / 100:,.0f} {payment.currency}\n"
            f"📦 Tez orada hujjatlaringizni olasiz!",
            parse_mode="Markdown"
        )

        # Admin guruhga xabar
        from admin_handlers import ADMIN_GROUP_ID
        await bot.send_message(
            ADMIN_GROUP_ID,
            f"✅ **TO'LOV QABUL QILINDI**\n\n"
            f"🆔 Ariza: `{app_code}`\n"
            f"👤 User: {message.from_user.full_name}\n"
            f"💰 Summa: {payment.total_amount / 100:,.0f} {payment.currency}\n"
            f"🔗 Provider: {payment.provider_payment_charge_id}",
            parse_mode="Markdown"
        )

        # Referral reward tekshiramiz
        referrer_id = await db.mark_referral_reward(message.from_user.id)
        if referrer_id:
            await bot.send_message(
                referrer_id,
                f"🎁 **MUKOFOT!**\n\n"
                f"Do'stingiz xizmatdan foydalandi!\n"
                f"💰 +17,500 tanga qo'shildi!",
                parse_mode="Markdown"
            )

    except Exception as e:
        print(f"❌ Successful payment error: {e}")
