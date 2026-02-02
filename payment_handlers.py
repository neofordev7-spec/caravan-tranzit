"""
PAYMENT HANDLERS
To'lovlarni qayta ishlash:
- Payme orqali to'lash (checkout URL)
- Click orqali to'lash (checkout URL)
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
from payme_api import generate_checkout_url
from click_api import ClickAPI
from strings import TEXTS

router = Router()


def t(lang: str, key: str) -> str:
    """Helper to get translated text with fallback to Uzbek."""
    return TEXTS.get(lang, TEXTS['uz']).get(key, TEXTS['uz'].get(key, ''))


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

        # Get user language
        user = await db.get_user(call.from_user.id)
        lang = user.get('language', 'uz') if user else 'uz'

        # Payme checkout URL yaratamiz
        checkout_url = generate_checkout_url(app_code, Decimal(str(price)))

        # Foydalanuvchiga to'lov havolasini yuboramiz
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"💳 Payme ({price:,.0f} UZS)", url=checkout_url)],
            [InlineKeyboardButton(text=t(lang, 'payment_cancelled'), callback_data=f"cancel_payment_{app_code}")]
        ])

        await call.message.edit_text(
            t(lang, 'payme_title').format(code=app_code, amount=f"{price:,.0f}"),
            reply_markup=kb,
            parse_mode="Markdown"
        )

        await call.answer(t(lang, 'payment_page_ready'))

    except Exception as e:
        print(f"Pay payme error: {e}")
        user = await db.get_user(call.from_user.id)
        lang = user.get('language', 'uz') if user else 'uz'
        await call.answer(t(lang, 'error_general'), show_alert=True)


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

        # Get user language
        user = await db.get_user(call.from_user.id)
        lang = user.get('language', 'uz') if user else 'uz'

        # Click checkout URL yaratamiz
        click_url = ClickAPI.generate_payment_url(app_code, Decimal(str(price)))

        # Foydalanuvchiga to'lov havolasini yuboramiz
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"💳 Click ({price:,.0f} UZS)", url=click_url)],
            [InlineKeyboardButton(text=t(lang, 'payment_cancelled'), callback_data=f"cancel_payment_{app_code}")]
        ])

        await call.message.edit_text(
            t(lang, 'click_title').format(code=app_code, amount=f"{price:,.0f}"),
            reply_markup=kb,
            parse_mode="Markdown"
        )

        await call.answer(t(lang, 'payment_page_ready'))

    except Exception as e:
        print(f"Pay click error: {e}")
        user = await db.get_user(call.from_user.id)
        lang = user.get('language', 'uz') if user else 'uz'
        await call.answer(t(lang, 'error_general'), show_alert=True)


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
        lang = user.get('language', 'uz') if user else 'uz'
        balance = user['balance']

        if balance < 35000:
            await call.answer(
                t(lang, 'not_enough_coins_msg').format(balance=f"{balance:,.0f}"),
                show_alert=True
            )
            return

        # Tasdiqni so'raymiz
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=t(lang, 'btn_confirm'), callback_data=f"confirm_coins_{app_code}")],
            [InlineKeyboardButton(text=t(lang, 'payment_cancelled'), callback_data=f"cancel_payment_{app_code}")]
        ])

        await call.message.edit_text(
            t(lang, 'coins_payment_confirm').format(code=app_code, remaining=f"{balance - 35000:,.0f}"),
            reply_markup=kb,
            parse_mode="Markdown"
        )

    except Exception as e:
        print(f"Pay coins error: {e}")
        user = await db.get_user(call.from_user.id)
        lang = user.get('language', 'uz') if user else 'uz'
        await call.answer(t(lang, 'error_general'), show_alert=True)


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
        lang = user.get('language', 'uz') if user else 'uz'
        balance = user['balance']

        if balance < 35000:
            await call.answer(
                t(lang, 'not_enough_coins_msg').format(balance=f"{balance:,.0f}"),
                show_alert=True
            )
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
            t(lang, 'payment_success_title').format(code=app_code, amount="35,000 tanga"),
            parse_mode="Markdown"
        )

        # Admin guruhga xabar (stays in Uzbek)
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
            # Get referrer's language
            referrer = await db.get_user(referrer_id)
            ref_lang = referrer.get('language', 'uz') if referrer else 'uz'
            await bot.send_message(
                referrer_id,
                t(ref_lang, 'referral_reward'),
                parse_mode="Markdown"
            )

    except Exception as e:
        print(f"Confirm coins error: {e}")
        user = await db.get_user(call.from_user.id)
        lang = user.get('language', 'uz') if user else 'uz'
        await call.answer(t(lang, 'error_general'), show_alert=True)


@router.callback_query(F.data.startswith("cancel_payment_"))
async def handle_cancel_payment(call: CallbackQuery):
    """
    To'lovni bekor qilish
    """
    user = await db.get_user(call.from_user.id)
    lang = user.get('language', 'uz') if user else 'uz'
    await call.message.delete()
    await call.answer(t(lang, 'payment_cancelled'))


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
            await message.answer(t('uz', 'press_start'))
            return

        lang = user.get('language', 'uz')

        # Eng so'nggi "priced" statusidagi arizani topamiz
        apps = await db.get_user_apps(message.from_user.id)
        priced_app = None
        for app in apps:
            if app['status'] == 'priced' and app['price']:
                priced_app = app
                break

        if not priced_app:
            await message.answer(t(lang, 'no_pending_app'))
            return

        app_code = priced_app['app_code']
        price = priced_app['price']

        # Payme checkout URL
        checkout_url = generate_checkout_url(app_code, Decimal(str(price)))

        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"💳 Payme ({price:,.0f} UZS)", url=checkout_url)],
            [InlineKeyboardButton(text=t(lang, 'payment_cancelled'), callback_data=f"cancel_payment_{app_code}")]
        ])

        await message.answer(
            t(lang, 'payme_title').format(code=app_code, amount=f"{price:,.0f}"),
            reply_markup=kb,
            parse_mode="Markdown"
        )

    except Exception as e:
        print(f"Payme text button error: {e}")
        user = await db.get_user(message.from_user.id)
        lang = user.get('language', 'uz') if user else 'uz'
        await message.answer(t(lang, 'error_general'))


@router.message(F.text.contains("Click"))
async def handle_click_text_button(message: Message, bot: Bot):
    """
    Foydalanuvchi "Click" tugmasini bosganida
    """
    try:
        user = await db.get_user(message.from_user.id)
        if not user:
            await message.answer(t('uz', 'press_start'))
            return

        lang = user.get('language', 'uz')

        # Eng so'nggi "priced" statusidagi arizani topamiz
        apps = await db.get_user_apps(message.from_user.id)
        priced_app = None
        for app in apps:
            if app['status'] == 'priced' and app['price']:
                priced_app = app
                break

        if not priced_app:
            await message.answer(t(lang, 'no_pending_app'))
            return

        app_code = priced_app['app_code']
        price = priced_app['price']

        # Click checkout URL
        click_url = ClickAPI.generate_payment_url(app_code, Decimal(str(price)))

        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"💳 Click ({price:,.0f} UZS)", url=click_url)],
            [InlineKeyboardButton(text=t(lang, 'payment_cancelled'), callback_data=f"cancel_payment_{app_code}")]
        ])

        await message.answer(
            t(lang, 'click_title').format(code=app_code, amount=f"{price:,.0f}"),
            reply_markup=kb,
            parse_mode="Markdown"
        )

    except Exception as e:
        print(f"Click text button error: {e}")
        user = await db.get_user(message.from_user.id)
        lang = user.get('language', 'uz') if user else 'uz'
        await message.answer(t(lang, 'error_general'))


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

        lang = user.get('language', 'uz')
        provider_name = "Payme" if provider == 'payme' else "Click"

        # Foydalanuvchiga xabar
        await bot.send_message(
            app['user_id'],
            t(lang, 'payment_success_title').format(code=app_code, amount=f"{amount:,.0f} UZS ({provider_name})"),
            parse_mode="Markdown"
        )

        # Admin guruhga xabar (stays in Uzbek)
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
            # Get referrer's language
            referrer = await db.get_user(referrer_id)
            ref_lang = referrer.get('language', 'uz') if referrer else 'uz'
            await bot.send_message(
                referrer_id,
                t(ref_lang, 'referral_reward'),
                parse_mode="Markdown"
            )

    except Exception as e:
        print(f"Notify payment success error: {e}")
