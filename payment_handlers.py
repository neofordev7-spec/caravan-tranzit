"""
PAYMENT HANDLERS
To'lovlarni qayta ishlash:
- Payme orqali to'lash (checkout URL)
- Click orqali to'lash (checkout URL)
- Tangalar bilan to'lash
- To'lov tarixini saqlash
"""
import os
from decimal import Decimal
from aiogram import Router, F, Bot
from aiogram.types import (
    CallbackQuery, Message, LabeledPrice,
    PreCheckoutQuery, InlineKeyboardMarkup, InlineKeyboardButton
)
from database import db
from payme_api import generate_checkout_url
from click_api import ClickAPI

router = Router()

# Click Provider Token for Telegram Payments
CLICK_PROVIDER_TOKEN = os.getenv("CLICK_PROVIDER_TOKEN", "")

# =========================================================================
# PAYMENT SELECTION - PAYME
# =========================================================================

@router.callback_query(F.data.startswith("pay_payme_"))
async def handle_pay_payme(call: CallbackQuery, bot: Bot):
    """
    Payme orqali to'lash - checkout URL yuboradi
    """
    try:
        app_code = call.data.split("pay_payme_")[1]

        # Arizani olamiz
        app = await db.get_application_by_code(app_code)
        if not app:
            await call.answer("Ariza topilmadi!", show_alert=True)
            return

        price = app['price']
        if not price:
            await call.answer("Narx belgilanmagan!", show_alert=True)
            return

        # Payme checkout URL yaratamiz
        checkout_url = generate_checkout_url(app_code, Decimal(str(price)))

        # Foydalanuvchiga to'lov havolasini yuboramiz
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"💳 Payme orqali to'lash ({price:,.0f} UZS)", url=checkout_url)],
            [InlineKeyboardButton(text="Bekor qilish", callback_data=f"cancel_payment_{app_code}")]
        ])

        await call.message.edit_text(
            f"💳 **PAYME ORQALI TO'LOV**\n\n"
            f"🆔 Ariza: `{app_code}`\n"
            f"💰 Summa: **{price:,.0f} UZS**\n\n"
            f"Quyidagi tugmani bosib to'lovni amalga oshiring.\n"
            f"To'lov muvaffaqiyatli bo'lgandan so'ng, "
            f"arizangiz avtomatik tasdiqlanadi.",
            reply_markup=kb,
            parse_mode="Markdown"
        )

        await call.answer("To'lov sahifasi tayyor!")

    except Exception as e:
        print(f"Pay payme error: {e}")
        await call.answer("Xatolik!", show_alert=True)


# =========================================================================
# PAYMENT SELECTION - CLICK
# =========================================================================

@router.callback_query(F.data.startswith("pay_click_"))
async def handle_pay_click(call: CallbackQuery, bot: Bot):
    """
    Click orqali to'lash - checkout URL yuboradi
    """
    try:
        app_code = call.data.split("pay_click_")[1]

        # Arizani olamiz
        app = await db.get_application_by_code(app_code)
        if not app:
            await call.answer("Ariza topilmadi!", show_alert=True)
            return

        price = app['price']
        if not price:
            await call.answer("Narx belgilanmagan!", show_alert=True)
            return

        # Click checkout URL yaratamiz
        click_url = ClickAPI.generate_payment_url(app_code, Decimal(str(price)))

        # Foydalanuvchiga to'lov havolasini yuboramiz
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"💳 Click orqali to'lash ({price:,.0f} UZS)", url=click_url)],
            [InlineKeyboardButton(text="Bekor qilish", callback_data=f"cancel_payment_{app_code}")]
        ])

        await call.message.edit_text(
            f"💳 **CLICK ORQALI TO'LOV**\n\n"
            f"🆔 Ariza: `{app_code}`\n"
            f"💰 Summa: **{price:,.0f} UZS**\n\n"
            f"Quyidagi tugmani bosib to'lovni amalga oshiring.",
            reply_markup=kb,
            parse_mode="Markdown"
        )

        await call.answer("To'lov sahifasi tayyor!")

    except Exception as e:
        print(f"Pay click error: {e}")
        await call.answer("Xatolik!", show_alert=True)


# =========================================================================
# PAYMENT SELECTION - COINS
# =========================================================================

@router.callback_query(F.data.startswith("pay_coins_"))
async def handle_pay_coins(call: CallbackQuery, bot: Bot):
    """
    Tangalar bilan to'lash (35,000 tangalar = 1 xizmat)
    """
    try:
        app_code = call.data.split("pay_coins_")[1]

        # Arizani olamiz
        app = await db.get_application_by_code(app_code)
        if not app:
            await call.answer("Ariza topilmadi!", show_alert=True)
            return

        # Foydalanuvchi balansini tekshiramiz
        user = await db.get_user(call.from_user.id)
        balance = user['balance']

        if balance < 35000:
            await call.answer(
                f"Yetarli tangalar yo'q!\n\n"
                f"Sizda: {balance:,.0f} tanga\n"
                f"Kerak: 35,000 tanga",
                show_alert=True
            )
            return

        # Tasdiqni so'raymiz
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Tasdiqlash", callback_data=f"confirm_coins_{app_code}")],
            [InlineKeyboardButton(text="Bekor qilish", callback_data=f"cancel_payment_{app_code}")]
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
        print(f"Pay coins error: {e}")
        await call.answer("Xatolik!", show_alert=True)


@router.callback_query(F.data.startswith("confirm_coins_"))
async def handle_confirm_coins(call: CallbackQuery, bot: Bot):
    """
    Tangalar bilan to'lashni tasdiqlash
    """
    try:
        app_code = call.data.split("confirm_coins_")[1]

        # Arizani olamiz
        app = await db.get_application_by_code(app_code)
        if not app:
            await call.answer("Ariza topilmadi!", show_alert=True)
            return

        # Balansni tekshiramiz va kamaytiramiz
        user = await db.get_user(call.from_user.id)
        balance = user['balance']

        if balance < 35000:
            await call.answer("Yetarli tangalar yo'q!", show_alert=True)
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
            f"**TO'LOV MUVAFFAQIYATLI!**\n\n"
            f"🆔 Ariza: `{app_code}`\n"
            f"💰 To'landi: **35,000 tanga**\n"
            f"💎 Qoldiq: **{balance - 35000:,.0f} tanga**\n\n"
            f"Tez orada hujjatlaringizni olasiz!",
            parse_mode="Markdown"
        )

        # Admin guruhga xabar
        from admin_handlers import ADMIN_GROUP_ID
        await bot.send_message(
            ADMIN_GROUP_ID,
            f"**TO'LOV QABUL QILINDI (TANGALAR)**\n\n"
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
        print(f"Confirm coins error: {e}")
        await call.answer("Xatolik!", show_alert=True)


@router.callback_query(F.data.startswith("cancel_payment_"))
async def handle_cancel_payment(call: CallbackQuery):
    """
    To'lovni bekor qilish
    """
    await call.message.delete()
    await call.answer("Bekor qilindi.")


# =========================================================================
# PAYMENT METHOD SELECTION FROM KEYBOARD (Text buttons)
# =========================================================================

@router.message(F.text.contains("Payme"))
async def handle_payme_text_button(message: Message, bot: Bot):
    """
    Foydalanuvchi "Payme" tugmasini bosganida
    """
    try:
        user = await db.get_user(message.from_user.id)
        if not user:
            await message.answer("Iltimos, avval /start bosing.")
            return

        # Eng so'nggi "priced" statusidagi arizani topamiz
        apps = await db.get_user_apps(message.from_user.id)
        priced_app = None
        for app in apps:
            if app['status'] == 'priced' and app['price']:
                priced_app = app
                break

        if not priced_app:
            await message.answer(
                "Hozirda to'lov kutayotgan ariza yo'q.\n"
                "Avval ariza yuboring va admin narx belgilasin."
            )
            return

        app_code = priced_app['app_code']
        price = priced_app['price']

        # Payme checkout URL
        checkout_url = generate_checkout_url(app_code, Decimal(str(price)))

        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"💳 Payme ({price:,.0f} UZS)", url=checkout_url)],
            [InlineKeyboardButton(text="Bekor qilish", callback_data=f"cancel_payment_{app_code}")]
        ])

        await message.answer(
            f"💳 **PAYME ORQALI TO'LOV**\n\n"
            f"🆔 Ariza: `{app_code}`\n"
            f"💰 Summa: **{price:,.0f} UZS**\n\n"
            f"Quyidagi tugmani bosib to'lovni amalga oshiring:",
            reply_markup=kb,
            parse_mode="Markdown"
        )

    except Exception as e:
        print(f"Payme text button error: {e}")
        await message.answer("Xatolik yuz berdi. Qaytadan urinib ko'ring.")


@router.message(F.text.contains("Click"))
async def handle_click_text_button(message: Message, bot: Bot):
    """
    Foydalanuvchi "Click" tugmasini bosganida
    """
    try:
        user = await db.get_user(message.from_user.id)
        if not user:
            await message.answer("Iltimos, avval /start bosing.")
            return

        # Eng so'nggi "priced" statusidagi arizani topamiz
        apps = await db.get_user_apps(message.from_user.id)
        priced_app = None
        for app in apps:
            if app['status'] == 'priced' and app['price']:
                priced_app = app
                break

        if not priced_app:
            await message.answer(
                "Hozirda to'lov kutayotgan ariza yo'q.\n"
                "Avval ariza yuboring va admin narx belgilasin."
            )
            return

        app_code = priced_app['app_code']
        price = priced_app['price']

        # Click checkout URL
        click_url = ClickAPI.generate_payment_url(app_code, Decimal(str(price)))

        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"💳 Click ({price:,.0f} UZS)", url=click_url)],
            [InlineKeyboardButton(text="Bekor qilish", callback_data=f"cancel_payment_{app_code}")]
        ])

        await message.answer(
            f"💳 **CLICK ORQALI TO'LOV**\n\n"
            f"🆔 Ariza: `{app_code}`\n"
            f"💰 Summa: **{price:,.0f} UZS**\n\n"
            f"Quyidagi tugmani bosib to'lovni amalga oshiring:",
            reply_markup=kb,
            parse_mode="Markdown"
        )

    except Exception as e:
        print(f"Click text button error: {e}")
        await message.answer("Xatolik yuz berdi. Qaytadan urinib ko'ring.")


# =========================================================================
# PAYME PAYMENT NOTIFICATION (Bot notifies user after Payme callback)
# =========================================================================

async def notify_payment_success(bot: Bot, app_code: str, amount: Decimal, provider: str = 'payme'):
    """
    To'lov muvaffaqiyatli bo'lganda foydalanuvchiga xabar yuborish.
    Bu funksiya payme_api.py dan chaqiriladi (PerformTransaction)
    """
    try:
        app = await db.get_application_by_code(app_code)
        if not app:
            return

        user = await db.get_user(app['user_id'])
        if not user:
            return

        provider_name = "Payme" if provider == 'payme' else "Click"

        # Foydalanuvchiga xabar
        await bot.send_message(
            app['user_id'],
            f"**TO'LOV MUVAFFAQIYATLI!**\n\n"
            f"🆔 Ariza: `{app_code}`\n"
            f"💰 To'langan: **{amount:,.0f} UZS**\n"
            f"💳 Usul: {provider_name}\n\n"
            f"Tez orada hujjatlaringizni olasiz!",
            parse_mode="Markdown"
        )

        # Admin guruhga xabar
        from admin_handlers import ADMIN_GROUP_ID
        await bot.send_message(
            ADMIN_GROUP_ID,
            f"**TO'LOV QABUL QILINDI ({provider_name.upper()})**\n\n"
            f"🆔 Ariza: `{app_code}`\n"
            f"👤 User: {user['full_name']}\n"
            f"💰 Summa: **{amount:,.0f} UZS**",
            parse_mode="Markdown"
        )

        # Referral reward
        referrer_id = await db.mark_referral_reward(app['user_id'])
        if referrer_id:
            await bot.send_message(
                referrer_id,
                f"🎁 **MUKOFOT!**\n\n"
                f"Do'stingiz xizmatdan foydalandi!\n"
                f"💰 +17,500 tanga qo'shildi!",
                parse_mode="Markdown"
            )

    except Exception as e:
        print(f"Notify payment success error: {e}")
