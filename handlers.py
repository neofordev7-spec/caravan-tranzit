import random
import re
import json
import asyncio
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, ReplyKeyboardRemove
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from database import db
from states import (
    Registration, EPIKodFlow, MBDeklaratsiyaFlow, ApplicationsFlow,
    SettingsFlow, ContactInfoFlow, KGDFlow, BonusFlow, ChatFlow, AdminState
)
import keyboards as kb
from strings import TEXTS

router = Router()
SUPER_ADMIN_ID = 2027194005
ADMIN_GROUP_ID = -1003463212374
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

async def get_text(state: FSMContext, key: str, **kwargs):
    """Get localized text from TEXTS dictionary"""
    data = await state.get_data()
    lang = data.get('lang', 'uz')
    return TEXTS.get(lang, TEXTS['uz']).get(key, "...").format(**kwargs)

async def get_user_lang(state: FSMContext):
    """Get user's language"""
    data = await state.get_data()
    return data.get('lang', 'uz')

# ==========================================================
# 1. ONBOARDING FLOW
# ==========================================================

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    """Start command - begin registration"""
    await state.clear()

    # Check for referral link: /start 123456789
    referrer_id = None
    if message.text and len(message.text.split()) > 1:
        try:
            referrer_id = int(message.text.split()[1])
            if referrer_id == message.from_user.id:
                referrer_id = None
            else:
                await state.update_data(referrer_id=referrer_id)
        except:
            pass

    await message.answer(TEXTS['uz']['start'], reply_markup=kb.get_lang_kb())
    await state.set_state(Registration.lang)

@router.callback_query(Registration.lang)
async def lang_chosen(call: CallbackQuery, state: FSMContext):
    """Language selected"""
    lang = call.data.split("_")[1]
    await state.update_data(lang=lang)
    await call.message.delete()

    t = TEXTS.get(lang, TEXTS['uz'])['agreement']
    await call.message.answer(t, reply_markup=kb.get_agreement_kb(lang))
    await state.set_state(Registration.agreement)

@router.callback_query(Registration.agreement)
async def agreement_accepted(call: CallbackQuery, state: FSMContext):
    """Agreement accepted"""
    await call.message.delete()
    data = await state.get_data()
    lang = data['lang']

    t = await get_text(state, 'ask_phone')
    await call.message.answer(t, reply_markup=kb.get_phone_kb(lang))
    await state.set_state(Registration.phone)

@router.message(Registration.phone)
async def phone_received(message: Message, state: FSMContext):
    """Phone number received"""
    data = await state.get_data()
    lang = data.get('lang', 'uz')
    referrer_id = data.get('referrer_id')

    ph = message.contact.phone_number if message.contact else message.text

    try:
        # Add user to database
        await db.add_user(message.from_user.id, message.from_user.full_name, ph, lang, 'IMPORT', referrer_id)

        # Handle referral bonus
        if referrer_id:
            success = await db.create_referral(referrer_id, message.from_user.id)
            if success:
                try:
                    bot = message.bot
                    await bot.send_message(
                        referrer_id,
                        f"🎉 **Yangi do'st!**\n\n"
                        f"👤 {message.from_user.full_name} sizning havolangiz orqali botga qo'shildi!\n"
                        f"💰 +2,000 tanga qo'shildi!\n\n"
                        f"🎁 Do'stingiz birinchi xizmatdan foydalansa, yana +17,500 tanga olasiz!",
                        parse_mode="Markdown"
                    )
                except:
                    pass
    except Exception as e:
        print(f"❌ Add user error: {e}")

    # Ask for direction
    t = await get_text(state, 'ask_direction')
    await message.answer(t, reply_markup=kb.get_direction_kb(lang))
    await state.set_state(Registration.direction)

@router.message(Registration.direction)
async def direction_selected(message: Message, state: FSMContext):
    """Direction selected (IMPORT/EKSPORT/TRANZIT)"""
    direction = message.text.replace("🚛", "").replace("📦", "").replace("🔄", "").strip()
    await state.update_data(direction=direction)

    # Update user direction in database
    try:
        user = await db.get_user(message.from_user.id)
        if user:
            await db.add_user(
                message.from_user.id,
                message.from_user.full_name,
                user['phone_number'],
                user['language'],
                direction
            )
    except Exception as e:
        print(f"❌ Update direction error: {e}")

    lang = await get_user_lang(state)
    t = await get_text(state, 'registered')
    await message.answer(t, reply_markup=kb.get_main_menu(lang))
    await state.clear()
    await state.update_data(lang=lang, direction=direction)

# ==========================================================
# 2. MAIN MENU HANDLERS (17 XIZMAT)
# ==========================================================

@router.message(F.text.contains("EPI KOD AT DEKLARATSIYA"))
async def start_epi_kod(message: Message, state: FSMContext):
    """EPI KOD AT DEKLARATSIYA flow"""
    await state.clear()
    lang = (await db.get_user(message.from_user.id))['language'] if await db.get_user(message.from_user.id) else 'uz'
    await state.update_data(lang=lang, service_type='EPI')

    t = await get_text(state, 'epi_start')
    await message.answer(t, reply_markup=kb.get_posts_kb())
    await state.set_state(EPIKodFlow.select_border_post)

@router.message(F.text.contains("MB DEKLARATSIYA"))
async def start_mb_deklaratsiya(message: Message, state: FSMContext):
    """MB DEKLARATSIYA flow"""
    await state.clear()
    lang = (await db.get_user(message.from_user.id))['language'] if await db.get_user(message.from_user.id) else 'uz'
    await state.update_data(lang=lang, service_type='MB')

    t = await get_text(state, 'mb_start')
    await message.answer(t, reply_markup=kb.get_posts_kb())
    await state.set_state(MBDeklaratsiyaFlow.select_border_post)

@router.message(F.text.contains("ISHONCH TELEFONLARI"))
async def show_contacts(message: Message, state: FSMContext):
    """Show contact information menu with 4 main functions"""
    await state.clear()
    lang = (await db.get_user(message.from_user.id))['language'] if await db.get_user(message.from_user.id) else 'uz'
    await state.update_data(lang=lang)

    t = await get_text(state, 'contacts_msg')
    await message.answer(t, reply_markup=kb.get_contact_info_kb(lang))
    await state.set_state(ContactInfoFlow.menu)

@router.message(ContactInfoFlow.menu)
async def contact_info_option_chosen(message: Message, state: FSMContext):
    """Contact Info: Option chosen"""
    lang = await get_user_lang(state)

    if "Ortga" in message.text or "Back" in message.text:
        await state.clear()
        await message.answer("🏠 Menu", reply_markup=kb.get_main_menu(lang))
        return

    if "RAQAMNI O'ZGARTIRISH" in message.text or "Change" in message.text and "phone" in message.text.lower():
        # Raqamni o'zgartirish
        t = await get_text(state, 'change_phone_msg')
        await message.answer(t, reply_markup=kb.get_phone_kb(lang))
        await state.set_state(ContactInfoFlow.change_phone)

    elif "TILNI O'ZGARTIRISH" in message.text or "Language" in message.text:
        # Tilni o'zgartirish
        t = await get_text(state, 'change_lang_msg')
        await message.answer(t, reply_markup=kb.get_lang_kb())
        await state.set_state(ContactInfoFlow.change_language)

    elif "XOTIRANI TOZALASH" in message.text or "Clear" in message.text:
        # Xotirani tozalash
        await db.clear_user_cache(message.from_user.id)
        t = await get_text(state, 'cache_cleared_msg')
        await message.answer(t)
        await message.answer("🏠 Menu", reply_markup=kb.get_main_menu(lang))
        await state.clear()

    elif "ADMIN BILAN ALOQA" in message.text or "Contact" in message.text:
        # Admin bilan aloqa - 3 ta tugma
        t = await get_text(state, 'admin_contact_msg')
        await message.answer(
            "📞 **ADMIN BILAN ALOQA:**\n\n"
            "📱 **Telefon raqamlar:**\n"
            "• +998 91 702 00 99\n"
            "• +998 94 312 00 99\n\n"
            "💬 **Telegram:**\n"
            "• @MYBOJXONA\n"
            "• @mybojxona1\n\n"
            "📲 **WhatsApp:**\n"
            "• +998 91 702 00 99\n"
            "• +998 94 312 00 99\n"
            "• [Guruhga qo'shilish](https://chat.whatsapp.com/Ka6XhUv2ueVFZPNuHo06BP)",
            reply_markup=kb.get_admin_contact_detailed_kb(),
            parse_mode="Markdown"
        )

@router.message(ContactInfoFlow.change_phone)
async def contact_info_phone_changed(message: Message, state: FSMContext):
    """Contact Info: Phone changed"""
    ph = message.contact.phone_number if message.contact else message.text
    user = await db.get_user(message.from_user.id)
    if user:
        await db.add_user(
            message.from_user.id,
            message.from_user.full_name,
            ph,
            user['language'],
            user.get('direction', 'IMPORT')
        )

    await message.answer("✅ Raqam o'zgartirildi!")
    lang = await get_user_lang(state)
    await message.answer("🏠 Menu", reply_markup=kb.get_main_menu(lang))
    await state.clear()

@router.callback_query(ContactInfoFlow.change_language)
async def contact_info_lang_changed(call: CallbackQuery, state: FSMContext):
    """Contact Info: Language changed"""
    new_lang = call.data.split("_")[1]
    user = await db.get_user(call.from_user.id)
    if user:
        await db.add_user(
            call.from_user.id,
            call.from_user.full_name,
            user['phone_number'],
            new_lang,
            user.get('direction', 'IMPORT')
        )

    await call.message.delete()
    await call.message.answer("✅ Til o'zgartirildi!")
    await call.message.answer("🏠 Menu", reply_markup=kb.get_main_menu(new_lang))
    await state.clear()
    await state.update_data(lang=new_lang)

@router.message(F.text.contains("ARIZALARIM"))
async def my_applications(message: Message, state: FSMContext):
    """My applications menu"""
    await state.clear()
    lang = (await db.get_user(message.from_user.id))['language'] if await db.get_user(message.from_user.id) else 'uz'
    await state.update_data(lang=lang)

    t = await get_text(state, 'apps_menu')
    await message.answer(t, reply_markup=kb.get_applications_menu_kb(lang))
    await state.set_state(ApplicationsFlow.choose_option)

@router.message(F.text.contains("SOZLAMALAR"))
async def settings_menu(message: Message, state: FSMContext):
    """Settings menu"""
    await state.clear()
    lang = (await db.get_user(message.from_user.id))['language'] if await db.get_user(message.from_user.id) else 'uz'
    await state.update_data(lang=lang)

    t = await get_text(state, 'settings_menu')
    await message.answer(t, reply_markup=kb.get_settings_kb(lang))
    await state.set_state(SettingsFlow.menu)

@router.message(F.text.contains("NARXLAR KATALOGI"))
async def show_prices(message: Message, state: FSMContext):
    """Show prices catalog with user balance"""
    lang = await get_user_lang(state)
    balance = await db.get_user_balance(message.from_user.id)
    t = await get_text(state, 'prices_catalog', balance=balance)
    await message.answer(t, parse_mode="Markdown")

@router.message(F.text.contains("DASTURNI YUKLAB OLING"))
async def app_download(message: Message, state: FSMContext):
    """App download menu"""
    lang = await get_user_lang(state)
    t = await get_text(state, 'app_download_msg')
    await message.answer(t, reply_markup=kb.get_app_download_kb(lang))

@router.message(F.text.contains("KGD") | F.text.contains("E-TRANZIT"))
async def kgd_menu(message: Message, state: FSMContext):
    """KGD viewing menu"""
    await state.clear()
    lang = (await db.get_user(message.from_user.id))['language'] if await db.get_user(message.from_user.id) else 'uz'
    await state.update_data(lang=lang)

    t = await get_text(state, 'kgd_menu_msg')
    await message.answer(t, reply_markup=kb.get_kgd_menu_kb(lang))
    await state.set_state(KGDFlow.choose_method)

@router.message(F.text.contains("GABARIT RUXSATNOMA"))
async def gabarit_info(message: Message, state: FSMContext):
    """Gabarit permit info"""
    t = await get_text(state, 'gabarit_msg')
    await message.answer(t, parse_mode="Markdown")

@router.message(F.text.contains("SUGURTA") | F.text.contains("ELEKTRON NAVBAT") | F.text.contains("ISHONCHLI YUKLAR"))
async def coming_soon(message: Message, state: FSMContext):
    """Placeholder for future services"""
    t = await get_text(state, 'coming_soon')
    await message.answer(t)

@router.message(F.text.contains("BOT ORQALI BONUS"))
async def bonus_menu(message: Message, state: FSMContext):
    """Bonus/referral menu"""
    await state.clear()
    lang = (await db.get_user(message.from_user.id))['language'] if await db.get_user(message.from_user.id) else 'uz'
    await state.update_data(lang=lang)

    t = await get_text(state, 'bonus_menu_msg')
    await message.answer(t, reply_markup=kb.get_bonus_menu_kb(lang))
    await state.set_state(BonusFlow.menu)

@router.message(F.text.contains("TANGALARIM HISOBI"))
async def show_balance(message: Message, state: FSMContext):
    """Show coin balance"""
    balance = await db.get_user_balance(message.from_user.id)
    t = await get_text(state, 'balance_msg', balance=int(balance))
    await message.answer(t, parse_mode="Markdown")

@router.message(F.text.contains("SOCIAL MEDIA"))
async def social_media(message: Message, state: FSMContext):
    """Show social media links"""
    t = await get_text(state, 'social_msg')
    await message.answer(t, reply_markup=kb.get_social_media_kb())

@router.message(F.text.contains("GAPLASHISH"))
async def start_chat(message: Message, state: FSMContext):
    """Start chat with support"""
    await state.clear()
    lang = (await db.get_user(message.from_user.id))['language'] if await db.get_user(message.from_user.id) else 'uz'
    await state.update_data(lang=lang)

    t = await get_text(state, 'chat_msg')
    await message.answer(t, reply_markup=kb.get_cancel_kb(lang))
    await state.set_state(ChatFlow.waiting_message)

# ==========================================================
# 3. EPI KOD FLOW
# ==========================================================

@router.message(EPIKodFlow.select_border_post)
async def epi_border_post_selected(message: Message, state: FSMContext):
    """EPI: Border post selected"""
    if "Ortga" in message.text or "Back" in message.text:
        lang = await get_user_lang(state)
        await state.clear()
        await message.answer("🏠 Menu", reply_markup=kb.get_main_menu(lang))
        return

    await state.update_data(border_post=message.text)

    # For now, skip agent selection (will implement later)
    # Ask for destination post based on direction
    data = await state.get_data()
    direction = data.get('direction', 'IMPORT')

    if direction == 'IMPORT':
        # IMPORT: manzil TIF postlaridan
        t = await get_text(state, 'select_dest_post')
        await message.answer(t, reply_markup=kb.get_dest_posts_kb())
        await state.set_state(EPIKodFlow.select_dest_post)
    elif direction == 'TRANZIT':
        # TRANZIT: manzil chegara postlaridan
        t = await get_text(state, 'select_dest_post')
        await message.answer(t, reply_markup=kb.get_dest_border_posts_kb())
        await state.set_state(EPIKodFlow.select_dest_post)
    else:
        # EKSPORT - no destination post
        t = await get_text(state, 'enter_car_number')
        await message.answer(t, reply_markup=kb.get_cancel_kb(await get_user_lang(state)))
        await state.set_state(EPIKodFlow.enter_car_number)

@router.message(EPIKodFlow.select_dest_post)
async def epi_dest_post_selected(message: Message, state: FSMContext):
    """EPI: Destination post selected"""
    if "Ortga" in message.text or "Back" in message.text:
        t = await get_text(state, 'epi_start')
        await message.answer(t, reply_markup=kb.get_posts_kb())
        await state.set_state(EPIKodFlow.select_border_post)
        return

    await state.update_data(dest_post=message.text)

    t = await get_text(state, 'enter_car_number')
    await message.answer(t, reply_markup=kb.get_cancel_kb(await get_user_lang(state)))
    await state.set_state(EPIKodFlow.enter_car_number)

@router.message(EPIKodFlow.enter_car_number)
async def epi_car_number_entered(message: Message, state: FSMContext):
    """EPI: Car number entered"""
    if not message.text:
        await message.reply("⚠️ Iltimos, mashina raqamini yozing (Rasm emas).")
        return

    car = message.text.replace(" ", "").upper()
    await state.update_data(car_number=car, photos=[])

    t = await get_text(state, 'docs_epi')
    await message.answer(t, reply_markup=kb.get_done_kb(await get_user_lang(state)), parse_mode="Markdown")
    await state.set_state(EPIKodFlow.collect_docs)

@router.message(EPIKodFlow.collect_docs, F.photo | F.document)
async def epi_photo_received(message: Message, state: FSMContext):
    """EPI: Photo/document received"""
    data = await state.get_data()
    current_photos = data.get('photos', [])

    file_id = None
    file_size = 0

    if message.photo:
        file_id = message.photo[-1].file_id
        file_size = message.photo[-1].file_size
    elif message.document:
        file_id = message.document.file_id
        file_size = message.document.file_size

    if file_size > MAX_FILE_SIZE:
        await message.reply("⚠️ Fayl juda katta (10MB dan ko'p). Kichikroq rasm yuklang.")
        return

    if file_id:
        current_photos.append(file_id)
        await state.update_data(photos=current_photos)

@router.message(EPIKodFlow.collect_docs, F.text)
async def epi_docs_done(message: Message, state: FSMContext, bot: Bot):
    """EPI: Documents upload done"""
    if "Ortga" in message.text or "Back" in message.text:
        t = await get_text(state, 'enter_car_number')
        await message.answer(t, reply_markup=kb.get_cancel_kb(await get_user_lang(state)))
        await state.set_state(EPIKodFlow.enter_car_number)
        return

    # Check if "Done" button pressed
    if any(k in message.text for k in ["Yuklab", "Done", "Болды", "完成"]):
        data = await state.get_data()
        if not data.get('photos') or len(data.get('photos', [])) == 0:
            t = await get_text(state, 'zero_photos')
            await message.answer(t)
            return

        # Create application
        code = f"EPI-{random.randint(10000, 99999)}"
        try:
            await db.create_application(code, message.from_user.id, 'EPI', data.get('car_number', ''), data)
        except Exception as e:
            print(f"Error creating application: {e}")

        # Send to admin group
        await send_to_admin_group(bot, message, code, data, 'EPI')

        # Notify user
        t = await get_text(state, 'waiting_admin', code=code)
        lang = await get_user_lang(state)
        await message.answer(t, reply_markup=kb.get_main_menu(lang), parse_mode="Markdown")
        await state.clear()
        await state.update_data(lang=lang)

# ==========================================================
# 4. MB DEKLARATSIYA FLOW (Similar to EPI KOD)
# ==========================================================

@router.message(MBDeklaratsiyaFlow.select_border_post)
async def mb_border_post_selected(message: Message, state: FSMContext):
    """MB: Border post selected"""
    if "Ortga" in message.text or "Back" in message.text:
        lang = await get_user_lang(state)
        await state.clear()
        await message.answer("🏠 Menu", reply_markup=kb.get_main_menu(lang))
        return

    await state.update_data(border_post=message.text)

    data = await state.get_data()
    direction = data.get('direction', 'IMPORT')

    if direction == 'IMPORT':
        # IMPORT: manzil TIF postlaridan
        t = await get_text(state, 'select_dest_post')
        await message.answer(t, reply_markup=kb.get_dest_posts_kb())
        await state.set_state(MBDeklaratsiyaFlow.select_dest_post)
    elif direction == 'TRANZIT':
        # TRANZIT: manzil chegara postlaridan
        t = await get_text(state, 'select_dest_post')
        await message.answer(t, reply_markup=kb.get_dest_border_posts_kb())
        await state.set_state(MBDeklaratsiyaFlow.select_dest_post)
    else:
        # EKSPORT - no destination post
        t = await get_text(state, 'enter_car_number')
        await message.answer(t, reply_markup=kb.get_cancel_kb(await get_user_lang(state)))
        await state.set_state(MBDeklaratsiyaFlow.enter_car_number)

@router.message(MBDeklaratsiyaFlow.select_dest_post)
async def mb_dest_post_selected(message: Message, state: FSMContext):
    """MB: Destination post selected"""
    if "Ortga" in message.text or "Back" in message.text:
        t = await get_text(state, 'mb_start')
        await message.answer(t, reply_markup=kb.get_posts_kb())
        await state.set_state(MBDeklaratsiyaFlow.select_border_post)
        return

    await state.update_data(dest_post=message.text)

    t = await get_text(state, 'enter_car_number')
    await message.answer(t, reply_markup=kb.get_cancel_kb(await get_user_lang(state)))
    await state.set_state(MBDeklaratsiyaFlow.enter_car_number)

@router.message(MBDeklaratsiyaFlow.enter_car_number)
async def mb_car_number_entered(message: Message, state: FSMContext):
    """MB: Car number entered"""
    if not message.text:
        await message.reply("⚠️ Iltimos, mashina raqamini yozing (Rasm emas).")
        return

    car = message.text.replace(" ", "").upper()
    await state.update_data(car_number=car, photos=[])

    t = await get_text(state, 'docs_mb')
    await message.answer(t, reply_markup=kb.get_done_kb(await get_user_lang(state)), parse_mode="Markdown")
    await state.set_state(MBDeklaratsiyaFlow.collect_docs)

@router.message(MBDeklaratsiyaFlow.collect_docs, F.photo | F.document)
async def mb_photo_received(message: Message, state: FSMContext):
    """MB: Photo/document received"""
    data = await state.get_data()
    current_photos = data.get('photos', [])

    file_id = None
    file_size = 0

    if message.photo:
        file_id = message.photo[-1].file_id
        file_size = message.photo[-1].file_size
    elif message.document:
        file_id = message.document.file_id
        file_size = message.document.file_size

    if file_size > MAX_FILE_SIZE:
        await message.reply("⚠️ Fayl juda katta (10MB dan ko'p). Kichikroq rasm yuklang.")
        return

    if file_id:
        current_photos.append(file_id)
        await state.update_data(photos=current_photos)

@router.message(MBDeklaratsiyaFlow.collect_docs, F.text)
async def mb_docs_done(message: Message, state: FSMContext, bot: Bot):
    """MB: Documents upload done"""
    if "Ortga" in message.text or "Back" in message.text:
        t = await get_text(state, 'enter_car_number')
        await message.answer(t, reply_markup=kb.get_cancel_kb(await get_user_lang(state)))
        await state.set_state(MBDeklaratsiyaFlow.enter_car_number)
        return

    if any(k in message.text for k in ["Yuklab", "Done", "Болды", "完成"]):
        data = await state.get_data()
        if not data.get('photos') or len(data.get('photos', [])) == 0:
            t = await get_text(state, 'zero_photos')
            await message.answer(t)
            return

        code = f"MB-{random.randint(10000, 99999)}"
        try:
            await db.create_application(code, message.from_user.id, 'MB', data.get('car_number', ''), data)
        except Exception as e:
            print(f"Error creating application: {e}")

        await send_to_admin_group(bot, message, code, data, 'MB')

        t = await get_text(state, 'waiting_admin', code=code)
        lang = await get_user_lang(state)
        await message.answer(t, reply_markup=kb.get_main_menu(lang), parse_mode="Markdown")
        await state.clear()
        await state.update_data(lang=lang)

# ==========================================================
# 5. HELPER FUNCTION - Send to Admin Group
# ==========================================================

async def send_to_admin_group(bot: Bot, message: Message, code: str, data: dict, app_type: str):
    """Send application to admin group"""
    try:
        user = await db.get_user(message.from_user.id)
        direction = data.get('direction', 'IMPORT')
        border_post = data.get('border_post', 'N/A')
        dest_post = data.get('dest_post', 'N/A')
        car_number = data.get('car_number', 'N/A')

        route = f"📍 Kirish: {border_post}"
        if dest_post != 'N/A':
            route += f"\n📍 Manzil: {dest_post}"

        cap = (
            f"🆕 **YANGI {app_type} ARIZA!**\n"
            f"🆔: `{code}`\n"
            f"🚛: {car_number}\n"
            f"👤: [{message.from_user.full_name}](tg://user?id={message.from_user.id})\n"
            f"📱: {user['phone_number'] if user else 'N/A'}\n"
            f"🌍: {direction}\n"
            f"🗣: {data.get('lang', 'uz').upper()}\n"
            f"{route}"
        )

        photos = data.get('photos', [])
        if not photos:
            await bot.send_message(ADMIN_GROUP_ID, cap, parse_mode="Markdown")
        else:
            chunked = [photos[i:i+10] for i in range(0, len(photos), 10)]

            for idx, chunk in enumerate(chunked):
                media = []
                for pidx, pid in enumerate(chunk):
                    caption = cap if (idx == 0 and pidx == 0) else None
                    media.append(InputMediaPhoto(media=pid, caption=caption, parse_mode="Markdown"))

                await bot.send_media_group(ADMIN_GROUP_ID, media=media)

        await bot.send_message(ADMIN_GROUP_ID, f"🆔 `{code}` boshqarish:",
                              reply_markup=kb.get_admin_claim_kb(code), parse_mode="Markdown")
    except Exception as e:
        print(f"Admin send error: {e}")
        try:
            await bot.send_message(ADMIN_GROUP_ID, f"🆕 Ariza: {code} (Xatolik: {e})")
        except:
            pass

# ==========================================================
# 6. APPLICATIONS FLOW
# ==========================================================

@router.message(ApplicationsFlow.choose_option)
async def apps_option_chosen(message: Message, state: FSMContext):
    """Applications: Option chosen"""
    if "Ortga" in message.text or "Back" in message.text:
        lang = await get_user_lang(state)
        await state.clear()
        await message.answer("🏠 Menu", reply_markup=kb.get_main_menu(lang))
        return

    if "ARIZA BOR" in message.text or "Search" in message.text:
        t = await get_text(state, 'search_app_car')
        await message.answer(t, reply_markup=kb.get_cancel_kb(await get_user_lang(state)))
        await state.set_state(ApplicationsFlow.enter_car_for_search)
    elif "ARIZALARIM" in message.text or "My" in message.text:
        apps = await db.get_user_apps(message.from_user.id)
        if not apps:
            t = await get_text(state, 'my_apps_empty')
            await message.answer(t)
        else:
            apps_text = ""
            for app in apps:
                apps_text += f"🔹 `{app['app_code']}`: {app['status']}\n"
            t = await get_text(state, 'my_apps_list', apps=apps_text)
            await message.answer(t, parse_mode="Markdown")

@router.message(ApplicationsFlow.enter_car_for_search)
async def apps_search_by_car(message: Message, state: FSMContext):
    """Applications: Search by car number"""
    if "Ortga" in message.text or "Back" in message.text:
        lang = await get_user_lang(state)
        t = await get_text(state, 'apps_menu')
        await message.answer(t, reply_markup=kb.get_applications_menu_kb(lang))
        await state.set_state(ApplicationsFlow.choose_option)
        return

    car_number = message.text.replace(" ", "").upper()
    app = await db.get_app_by_car_number(car_number)

    if not app:
        t = await get_text(state, 'app_not_found')
        await message.answer(t)
    else:
        t = await get_text(state, 'app_found',
                          code=app['app_code'],
                          car=app['vehicle_number'],
                          date=app['created_at'].strftime("%d.%m.%Y %H:%M"),
                          status=app['status'])
        await message.answer(t, parse_mode="Markdown")

# ==========================================================
# 7. SETTINGS FLOW
# ==========================================================

@router.message(SettingsFlow.menu)
async def settings_option_chosen(message: Message, state: FSMContext):
    """Settings: Option chosen"""
    lang = await get_user_lang(state)

    if "Ortga" in message.text or "Back" in message.text:
        await state.clear()
        await message.answer("🏠 Menu", reply_markup=kb.get_main_menu(lang))
        return

    if "RAQAMNI O'ZGARTIRISH" in message.text or "Change" in message.text and "phone" in message.text.lower():
        t = await get_text(state, 'change_phone_msg')
        await message.answer(t, reply_markup=kb.get_phone_kb(lang))
        await state.set_state(SettingsFlow.change_phone)

    elif "TILNI O'ZGARTIRISH" in message.text or "Language" in message.text:
        t = await get_text(state, 'change_lang_msg')
        await message.answer(t, reply_markup=kb.get_lang_kb())
        await state.set_state(SettingsFlow.change_language)

    elif "XOTIRANI TOZALASH" in message.text or "Clear" in message.text:
        await db.clear_user_cache(message.from_user.id)
        t = await get_text(state, 'cache_cleared_msg')
        await message.answer(t)
        await message.answer("🏠 Menu", reply_markup=kb.get_main_menu(lang))
        await state.clear()

    elif "ADMIN BILAN ALOQA" in message.text or "Contact" in message.text:
        t = await get_text(state, 'admin_contact_msg')
        await message.answer(t, reply_markup=kb.get_admin_contact_kb(), parse_mode="Markdown")

@router.message(SettingsFlow.change_phone)
async def settings_phone_changed(message: Message, state: FSMContext):
    """Settings: Phone changed"""
    ph = message.contact.phone_number if message.contact else message.text
    user = await db.get_user(message.from_user.id)
    if user:
        await db.add_user(
            message.from_user.id,
            message.from_user.full_name,
            ph,
            user['language'],
            user.get('direction', 'IMPORT')
        )

    await message.answer("✅ Raqam o'zgartirildi!")
    lang = await get_user_lang(state)
    await message.answer("🏠 Menu", reply_markup=kb.get_main_menu(lang))
    await state.clear()

@router.callback_query(SettingsFlow.change_language)
async def settings_lang_changed(call: CallbackQuery, state: FSMContext):
    """Settings: Language changed"""
    new_lang = call.data.split("_")[1]
    user = await db.get_user(call.from_user.id)
    if user:
        await db.add_user(
            call.from_user.id,
            call.from_user.full_name,
            user['phone_number'],
            new_lang,
            user.get('direction', 'IMPORT')
        )

    await call.message.delete()
    await call.message.answer("✅ Til o'zgartirildi!")
    await call.message.answer("🏠 Menu", reply_markup=kb.get_main_menu(new_lang))
    await state.clear()
    await state.update_data(lang=new_lang)

# ==========================================================
# 8. KGD FLOW
# ==========================================================

@router.message(KGDFlow.choose_method)
async def kgd_method_chosen(message: Message, state: FSMContext):
    """KGD: Method chosen"""
    lang = await get_user_lang(state)

    if "Ortga" in message.text or "Back" in message.text:
        await state.clear()
        await message.answer("🏠 Menu", reply_markup=kb.get_main_menu(lang))
        return

    if "DASTUR ORQALI" in message.text:
        t = await get_text(state, 'kgd_app_msg')
        await message.answer(t, reply_markup=kb.get_kgd_app_submenu_kb(lang), parse_mode="Markdown")

    elif "XODIMLAR ORQALI" in message.text:
        t = await get_text(state, 'kgd_staff_car')
        await message.answer(t, reply_markup=kb.get_cancel_kb(lang))
        await state.set_state(KGDFlow.enter_car_number)

@router.message(KGDFlow.enter_car_number)
async def kgd_car_entered(message: Message, state: FSMContext, bot: Bot):
    """KGD: Car number entered for staff check"""
    if "Ortga" in message.text or "Back" in message.text:
        lang = await get_user_lang(state)
        t = await get_text(state, 'kgd_menu_msg')
        await message.answer(t, reply_markup=kb.get_kgd_menu_kb(lang))
        await state.set_state(KGDFlow.choose_method)
        return

    car_number = message.text.replace(" ", "").upper()
    t = await get_text(state, 'kgd_checking')
    await message.answer(t)

    # Send to admin group for manual check
    try:
        await bot.send_message(
            ADMIN_GROUP_ID,
            f"🔍 **KGD KO'RISH SO'ROVI**\n\n"
            f"👤: [{message.from_user.full_name}](tg://user?id={message.from_user.id})\n"
            f"🚛: {car_number}\n\n"
            f"Xodimlar javob berishsin!",
            parse_mode="Markdown"
        )
    except Exception as e:
        print(f"Error sending KGD request: {e}")

    lang = await get_user_lang(state)
    await message.answer("✅ So'rovingiz yuborildi! Javobni kutib turing.", reply_markup=kb.get_main_menu(lang))
    await state.clear()

# ==========================================================
# 9. BONUS FLOW
# ==========================================================

@router.message(BonusFlow.menu)
async def bonus_option_chosen(message: Message, state: FSMContext):
    """Bonus: Option chosen"""
    lang = await get_user_lang(state)

    if "Ortga" in message.text or "Back" in message.text:
        await state.clear()
        await message.answer("🏠 Menu", reply_markup=kb.get_main_menu(lang))
        return

    if "HAVOLANGIZNI OLING" in message.text or "link" in message.text.lower():
        bot_username = (await message.bot.me()).username
        referral_link = f"https://t.me/{bot_username}?start={message.from_user.id}"
        t = await get_text(state, 'get_referral_link', link=referral_link)
        await message.answer(t, parse_mode="Markdown")

    elif "TUSHUNTIRISHNOMA" in message.text or "info" in message.text.lower():
        t = await get_text(state, 'bonus_info')
        await message.answer(t, parse_mode="Markdown")

    elif "TANGALARIM" in message.text or "coins" in message.text.lower():
        balance = await db.get_user_balance(message.from_user.id)
        t = await get_text(state, 'balance_msg', balance=int(balance))
        await message.answer(t, parse_mode="Markdown")

# ==========================================================
# 10. CHAT FLOW
# ==========================================================

@router.message(ChatFlow.waiting_message)
async def chat_message_received(message: Message, state: FSMContext, bot: Bot):
    """Chat: Message received"""
    if "Ortga" in message.text or "Back" in message.text or "Bekor" in message.text:
        lang = await get_user_lang(state)
        await state.clear()
        await message.answer("🏠 Menu", reply_markup=kb.get_main_menu(lang))
        return

    # Send to admin group
    try:
        await bot.send_message(
            ADMIN_GROUP_ID,
            f"💬 **XABAR (GAPLASHISH)**\n\n"
            f"👤: [{message.from_user.full_name}](tg://user?id={message.from_user.id})\n"
            f"🆔: `{message.from_user.id}`\n"
            f"📝: {message.text}",
            parse_mode="Markdown"
        )
    except Exception as e:
        print(f"Error sending chat message: {e}")

    t = await get_text(state, 'chat_sent')
    lang = await get_user_lang(state)
    await message.answer(t, reply_markup=kb.get_main_menu(lang))
    await state.clear()

# ==========================================================
# 11. ADMIN HANDLERS
# ==========================================================

@router.callback_query(F.data.startswith("claim_"))
async def admin_claim(call: CallbackQuery, bot: Bot):
    """Admin claims application"""
    code = call.data.split("_")[1]
    if await db.claim_application(code, call.from_user.id):
        await call.message.edit_text(f"✅ Qabul qilindi: {call.from_user.full_name}\n🆔 `{code}`", parse_mode="Markdown")
        try:
            await bot.send_message(call.from_user.id, f"Arizani oldingiz: {code}", reply_markup=kb.get_pricing_kb(code))
        except:
            await call.answer("Botga /start bosing!", show_alert=True)
    else:
        await call.answer("Band!", show_alert=True)

@router.callback_query(F.data.startswith("setprice_"))
async def admin_set_price(call: CallbackQuery, bot: Bot):
    """Admin sets price"""
    try:
        parts = call.data.split("_")
        amt = parts[1]
        code = parts[2]

        app = await db.get_app_by_code(code)
        if app:
            await db.update_application_price(code, float(amt))

            user_lang = (await db.get_user(app['user_id']))['language'] if await db.get_user(app['user_id']) else 'uz'
            t = TEXTS.get(user_lang, TEXTS['uz'])['price_set'].format(price=amt)

            await bot.send_message(app['user_id'], t,
                                  reply_markup=kb.get_payment_methods_kb(user_lang),
                                  parse_mode="Markdown")
            await call.message.edit_text(f"✅ Yuborildi: {amt} so'm")
    except Exception as e:
        print(f"Error setting price: {e}")
    await call.answer()

@router.callback_query(F.data == "cancel_pay")
async def cancel_payment(call: CallbackQuery):
    """Cancel payment"""
    await call.message.delete()

@router.message(F.chat.id == ADMIN_GROUP_ID)
async def admin_group_handler(message: Message, bot: Bot):
    """Handle admin group messages"""
    if message.reply_to_message:
        orig = message.reply_to_message.text or ""
        match = re.search(r"(?:ID|🆔):\s*`?(\d+)`?", orig)
        if match:
            try:
                await bot.send_message(int(match.group(1)), f"👮‍♂️ **Admin:**\n{message.text}", parse_mode="Markdown")
            except:
                pass

    # Check for car number broadcast
    txt = (message.text or "").upper()
    car_m = re.search(r"(\d{2}[A-Z]\d{3}[A-Z]{2})|(\d{5}[A-Z]{3})", txt)
    if car_m:
        app = await db.get_app_by_car_number(car_m.group(0))
        if app:
            try:
                await bot.send_message(app['user_id'], f"🔔 Admin: {message.text}")
            except:
                pass

# ==========================================================
# 12. GLOBAL HANDLERS
# ==========================================================

@router.message(F.text.in_(["⬅️ Ortga", "⬅️ Назад", "⬅️ Back"]))
async def global_back_button(message: Message, state: FSMContext):
    """Global back button handler"""
    current_state = await state.get_state()

    if current_state is None:
        return  # Already at main menu

    lang = await get_user_lang(state)
    await state.clear()
    await state.update_data(lang=lang)
    await message.answer("🏠 Menu", reply_markup=kb.get_main_menu(lang))

@router.message(F.text.in_(["❌ Bekor qilish", "❌ Cancel", "❌ Отмена"]))
async def global_cancel_button(message: Message, state: FSMContext):
    """Global cancel button handler"""
    lang = await get_user_lang(state)
    await state.clear()
    await state.update_data(lang=lang)
    await message.answer("🏠 Menu", reply_markup=kb.get_main_menu(lang))
