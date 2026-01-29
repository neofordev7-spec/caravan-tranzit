"""
ADMIN GROUP HANDLERS
Admin guruhida ishlatiladigan handlerlar:
- Arizalarni qabul qilish/rad etish
- Narx belgilash
- Statusni yangilash
"""
import re
from decimal import Decimal
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import db
from payme_api import generate_checkout_url
from click_api import ClickAPI

router = Router()

# Admin guruh ID
ADMIN_GROUP_ID = -1003463212374

# FSM States for admin actions
class AdminPricingState(StatesGroup):
    waiting_for_custom_price = State()


# =========================================================================
# CALLBACK HANDLERS
# =========================================================================

@router.callback_query(F.data.startswith("claim_"))
async def handle_accept(call: CallbackQuery, bot: Bot):
    """
    Arizani qabul qilish (accept)
    """
    app_code = call.data.split("_")[1]

    try:
        # Arizani bazadan olamiz
        app = await db.get_application_by_code(app_code)
        if not app:
            await call.answer("❌ Ariza topilmadi!", show_alert=True)
            return

        # Arizani claim qilamiz
        success = await db.claim_application(app_code, call.from_user.id)
        if not success:
            await call.answer("❌ Bu ariza allaqachon olingan!", show_alert=True)
            return

        # Xabarni yangilaymiz
        await call.message.edit_text(
            f"✅ **ARIZA QABUL QILINDI**\n\n"
            f"🆔 Kod: `{app_code}`\n"
            f"👤 Admin: {call.from_user.full_name}\n\n"
            f"💰 Endi narx belgilashingiz mumkin:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="💰 Narx belgilash", callback_data=f"setprice_{app_code}")],
                [InlineKeyboardButton(text="❌ Rad etish", callback_data=f"reject_{app_code}")]
            ])
        )

        await call.answer("✅ Ariza qabul qilindi!")

    except Exception as e:
        print(f"❌ Accept error: {e}")
        await call.answer("❌ Xatolik yuz berdi!", show_alert=True)


@router.callback_query(F.data.startswith("reject_"))
async def handle_reject(call: CallbackQuery, bot: Bot):
    """
    Arizani rad etish
    """
    app_code = call.data.split("_")[1]

    try:
        # Arizani bazadan olamiz
        app = await db.get_application_by_code(app_code)
        if not app:
            await call.answer("❌ Ariza topilmadi!", show_alert=True)
            return

        # Statusni yangilaymiz
        await db.update_application_status(app_code, 'rejected')

        # Xabarni yangilaymiz
        await call.message.edit_text(
            f"❌ **ARIZA RAD ETILDI**\n\n"
            f"🆔 Kod: `{app_code}`\n"
            f"👤 Admin: {call.from_user.full_name}",
            parse_mode="Markdown"
        )

        # Foydalanuvchiga xabar yuboramiz
        await bot.send_message(
            app['user_id'],
            f"❌ **Arizangiz rad etildi**\n\n"
            f"🆔 Kod: `{app_code}`\n"
            f"📞 Qo'shimcha ma'lumot uchun admin bilan bog'laning.",
            parse_mode="Markdown"
        )

        await call.answer("✅ Ariza rad etildi va foydalanuvchiga xabar yuborildi.")

    except Exception as e:
        print(f"❌ Reject error: {e}")
        await call.answer("❌ Xatolik yuz berdi!", show_alert=True)


@router.callback_query(F.data.startswith("setprice_"))
async def handle_set_price(call: CallbackQuery, bot: Bot):
    """
    Narx belgilash - tanlangan narxlar yoki custom
    """
    try:
        parts = call.data.split("_")

        # Agar 3 ta qism bo'lsa: setprice_<code> - narxlar ro'yxatini ko'rsatamiz
        if len(parts) == 2:
            app_code = parts[1]

            # Narx variantlarini ko'rsatamiz
            kb = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📦 1-2 Partiya (35,000 UZS)", callback_data=f"price_35000_{app_code}")],
                [InlineKeyboardButton(text="📦 3 Partiya (45,000 UZS)", callback_data=f"price_45000_{app_code}")],
                [InlineKeyboardButton(text="📦 4+ Partiya (60,000 UZS)", callback_data=f"price_60000_{app_code}")],
                [InlineKeyboardButton(text="✏️ Boshqa narx", callback_data=f"custom_price_{app_code}")],
                [InlineKeyboardButton(text="❌ Bekor qilish", callback_data=f"cancel_price_{app_code}")]
            ])

            await call.message.answer(
                f"💰 **Narx belgilang:**\n\n🆔 Ariza: `{app_code}`",
                reply_markup=kb,
                parse_mode="Markdown"
            )
            await call.answer()

    except Exception as e:
        print(f"❌ Set price error: {e}")
        await call.answer("❌ Xatolik!", show_alert=True)


@router.callback_query(F.data.startswith("price_"))
async def handle_price_selected(call: CallbackQuery, bot: Bot):
    """
    Tanlangan narxni qo'llash
    """
    try:
        parts = call.data.split("_")
        amount = Decimal(parts[1])
        app_code = parts[2]

        # Arizani olamiz
        app = await db.get_application_by_code(app_code)
        if not app:
            await call.answer("❌ Ariza topilmadi!", show_alert=True)
            return

        # Narxni bazaga saqlaymiz
        await db.update_application_price(app_code, amount)

        # Admin guruhda tasdiqlaymiz
        await call.message.edit_text(
            f"✅ **NARX BELGILANDI**\n\n"
            f"🆔 Ariza: `{app_code}`\n"
            f"💰 Narx: **{amount:,.0f} UZS**\n"
            f"👤 Admin: {call.from_user.full_name}",
            parse_mode="Markdown"
        )

        # Foydalanuvchiga invoice yuboramiz
        await send_invoice_to_user(bot, app, amount)

        await call.answer("✅ Narx belgilandi va foydalanuvchiga yuborildi!")

    except Exception as e:
        print(f"❌ Price selected error: {e}")
        await call.answer("❌ Xatolik!", show_alert=True)


@router.callback_query(F.data.startswith("custom_price_"))
async def handle_custom_price(call: CallbackQuery, state: FSMContext):
    """
    Qo'lda narx kiritish
    """
    app_code = call.data.split("_")[2]

    await state.set_state(AdminPricingState.waiting_for_custom_price)
    await state.update_data(app_code=app_code)

    await call.message.answer(
        f"✏️ **Narxni kiriting (UZS):**\n\n"
        f"🆔 Ariza: `{app_code}`\n\n"
        f"Misol: 50000",
        parse_mode="Markdown"
    )
    await call.answer()


@router.message(AdminPricingState.waiting_for_custom_price)
async def process_custom_price(message: Message, state: FSMContext, bot: Bot):
    """
    Qo'lda kiritilgan narxni qayta ishlash
    """
    try:
        # Narxni parse qilamiz
        price_text = message.text.replace(" ", "").replace(",", "")
        amount = Decimal(price_text)

        if amount <= 0:
            await message.answer("❌ Narx 0 dan katta bo'lishi kerak!")
            return

        # State dan app_code ni olamiz
        data = await state.get_data()
        app_code = data.get('app_code')

        # Arizani olamiz
        app = await db.get_application_by_code(app_code)
        if not app:
            await message.answer("❌ Ariza topilmadi!")
            await state.clear()
            return

        # Narxni saqlaymiz
        await db.update_application_price(app_code, amount)

        # Tasdiqlaymiz
        await message.answer(
            f"✅ **NARX BELGILANDI**\n\n"
            f"🆔 Ariza: `{app_code}`\n"
            f"💰 Narx: **{amount:,.0f} UZS**\n"
            f"👤 Admin: {message.from_user.full_name}",
            parse_mode="Markdown"
        )

        # Foydalanuvchiga yuboramiz
        await send_invoice_to_user(bot, app, amount)

        await state.clear()

    except ValueError:
        await message.answer("❌ Noto'g'ri format! Faqat raqam kiriting (masalan: 50000)")
    except Exception as e:
        print(f"❌ Custom price error: {e}")
        await message.answer("❌ Xatolik yuz berdi!")
        await state.clear()


@router.callback_query(F.data.startswith("cancel_price_"))
async def handle_cancel_price(call: CallbackQuery):
    """
    Narx belgilashni bekor qilish
    """
    await call.message.delete()
    await call.answer("Bekor qilindi.")


# =========================================================================
# HELPER FUNCTIONS
# =========================================================================

async def send_invoice_to_user(bot: Bot, app, amount: Decimal):
    """
    Foydalanuvchiga to'lov invoicesini yuboradi
    """
    try:
        user_id = app['user_id']
        app_code = app['app_code']

        # Foydalanuvchi ma'lumotlarini olamiz
        user = await db.get_user(user_id)
        if not user:
            return

        # Payme va Click checkout URL larini yaratamiz
        payme_url = generate_checkout_url(app_code, amount)
        click_url = ClickAPI.generate_payment_url(app_code, amount)

        # To'lov usullarini ko'rsatamiz
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"💳 Payme ({amount:,.0f} UZS)", url=payme_url)],
            [InlineKeyboardButton(text=f"💳 Click ({amount:,.0f} UZS)", url=click_url)],
            [InlineKeyboardButton(text="🪙 Tangalardan to'lash", callback_data=f"pay_coins_{app_code}")],
            [InlineKeyboardButton(text="❌ Bekor qilish", callback_data=f"cancel_payment_{app_code}")]
        ])

        # Balance tekshiramiz
        balance = user['balance']
        can_pay_with_coins = balance >= 35000

        coins_msg = ""
        if can_pay_with_coins:
            free_services = int(balance / 35000)
            coins_msg = f"\n\n💰 Sizda **{balance:,.0f}** tanga mavjud!\n🎁 Bepul xizmatlar: {free_services}"

        msg = f"""
✅ **Arizangiz tasdiqlandi!**

🆔 Ariza: `{app_code}`
💰 To'lov summasi: **{amount:,.0f} UZS**
{coins_msg}

📌 To'lov usulini tanlang:
"""

        await bot.send_message(
            user_id,
            msg,
            reply_markup=kb,
            parse_mode="Markdown"
        )

    except Exception as e:
        print(f"❌ Send invoice error: {e}")


# =========================================================================
# ADMIN GROUP MESSAGE HANDLER
# =========================================================================

@router.message(F.chat.id == ADMIN_GROUP_ID)
async def admin_group_messages(message: Message, bot: Bot):
    """
    Admin grupidagi xabarlarni qayta ishlash
    - Reply to message: Foydalanuvchiga javob yuborish
    - Mashina raqami: Foydalanuvchiga xabar yuborish
    """
    # Reply to message bo'lsa
    if message.reply_to_message:
        orig_text = message.reply_to_message.text or message.reply_to_message.caption or ""

        # User ID ni topamiz
        match = re.search(r'(?:ID|🆔|Telegram ID):\s*`?(\d+)`?', orig_text)
        if match:
            user_id = int(match.group(1))
            try:
                await bot.send_message(
                    user_id,
                    f"👮‍♂️ **Admin javob:**\n\n{message.text}",
                    parse_mode="Markdown"
                )
                await message.reply("✅ Yuborildi!")
            except Exception as e:
                await message.reply(f"❌ Yuborib bo'lmadi: {e}")
            return

    # Mashina raqamini topib, foydalanuvchiga xabar yuborish
    text_upper = (message.text or "").upper()
    car_match = re.search(r'\b(\d{2}[A-Z]\d{3}[A-Z]{2})\b', text_upper)

    if car_match:
        vehicle_number = car_match.group(1)

        # Bazadan arizani topamiz
        # TODO: Add method to find application by vehicle number
        # app = await db.get_application_by_vehicle(vehicle_number)
        # if app:
        #     await bot.send_message(app['user_id'], f"🔔 Admin: {message.text}")
        pass
