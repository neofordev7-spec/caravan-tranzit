import random
import re
import json
import asyncio
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, InputMediaDocument, ReplyKeyboardRemove
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
        # Add user to database (direction default: IMPORT)
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

    # Go directly to main menu (skip direction selection)
    t = await get_text(state, 'registered')
    await message.answer(t, reply_markup=kb.get_main_menu(lang))
    await state.clear()
    await state.update_data(lang=lang)

# ==========================================================
# 2. MAIN MENU HANDLERS (17 XIZMAT)
# ==========================================================

@router.message(F.text.startswith("📄"))
async def start_epi_kod(message: Message, state: FSMContext):
    """EPI KOD AT DEKLARATSIYA flow"""
    await state.clear()
    lang = (await db.get_user(message.from_user.id))['language'] if await db.get_user(message.from_user.id) else 'uz'
    await state.update_data(lang=lang, service_type='EPI')

    t = await get_text(state, 'epi_start')
    await message.answer(t, reply_markup=kb.get_posts_kb())
    await state.set_state(EPIKodFlow.select_border_post)

@router.message(F.text.startswith("📋"))
async def start_mb_deklaratsiya(message: Message, state: FSMContext):
    """MB DEKLARATSIYA flow"""
    await state.clear()
    lang = (await db.get_user(message.from_user.id))['language'] if await db.get_user(message.from_user.id) else 'uz'
    await state.update_data(lang=lang, service_type='MB')

    t = await get_text(state, 'mb_start')
    await message.answer(t, reply_markup=kb.get_posts_kb())
    await state.set_state(MBDeklaratsiyaFlow.select_border_post)

@router.message(F.text.startswith("📞"))
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

    if message.text.startswith("⬅️"):
        await state.clear()
        await message.answer("🏠 Menu", reply_markup=kb.get_main_menu(lang))
        return

    if message.text.startswith("📱"):
        # Raqamni o'zgartirish
        t = await get_text(state, 'change_phone_msg')
        await message.answer(t, reply_markup=kb.get_phone_kb(lang))
        await state.set_state(ContactInfoFlow.change_phone)

    elif message.text.startswith("🌐"):
        # Tilni o'zgartirish
        t = await get_text(state, 'change_lang_msg')
        await message.answer(t, reply_markup=kb.get_lang_kb())
        await state.set_state(ContactInfoFlow.change_language)

    elif message.text.startswith("🗑"):
        # Xotirani tozalash
        await db.clear_user_cache(message.from_user.id)
        t = await get_text(state, 'cache_cleared_msg')
        await message.answer(t)
        await message.answer("🏠 Menu", reply_markup=kb.get_main_menu(lang))
        await state.clear()

    elif message.text.startswith("👨‍💼"):
        # Admin bilan aloqa
        t = await get_text(state, 'admin_contact_msg')
        await message.answer(t,
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

@router.message(F.text.startswith("🎫"))
async def my_applications(message: Message, state: FSMContext):
    """My applications menu"""
    await state.clear()
    lang = (await db.get_user(message.from_user.id))['language'] if await db.get_user(message.from_user.id) else 'uz'
    await state.update_data(lang=lang)

    t = await get_text(state, 'apps_menu')
    await message.answer(t, reply_markup=kb.get_applications_menu_kb(lang))
    await state.set_state(ApplicationsFlow.choose_option)

@router.message(F.text.startswith("⚙️"))
async def settings_menu(message: Message, state: FSMContext):
    """Settings menu"""
    await state.clear()
    lang = (await db.get_user(message.from_user.id))['language'] if await db.get_user(message.from_user.id) else 'uz'
    await state.update_data(lang=lang)

    t = await get_text(state, 'settings_menu')
    await message.answer(t, reply_markup=kb.get_settings_kb(lang))
    await state.set_state(SettingsFlow.menu)

@router.message(F.text.startswith("💰"))
async def show_prices(message: Message, state: FSMContext):
    """Show prices catalog"""
    t = await get_text(state, 'prices_catalog')
    await message.answer(t, parse_mode="HTML")

@router.message(F.text.startswith("📱"))
async def app_download_or_social(message: Message, state: FSMContext):
    """App download OR Social media menu (both use 📱 emoji)"""
    # Tekshiramiz: Social media yoki App download?
    is_social = any(t in message.text for t in
        {v.get('menu_social', '') for v in TEXTS.values() if v.get('menu_social')})
    if is_social:
        t = await get_text(state, 'social_msg')
        await message.answer(t, reply_markup=kb.get_social_media_kb())
    else:
        lang = await get_user_lang(state)
        t = await get_text(state, 'app_download_msg')
        await message.answer(t, reply_markup=kb.get_app_download_kb(lang))

@router.message(F.text.startswith("🚚"))
async def kgd_menu(message: Message, state: FSMContext):
    """KGD viewing menu"""
    await state.clear()
    lang = (await db.get_user(message.from_user.id))['language'] if await db.get_user(message.from_user.id) else 'uz'
    await state.update_data(lang=lang)

    t = await get_text(state, 'kgd_menu_msg')
    await message.answer(t, reply_markup=kb.get_kgd_menu_kb(lang))
    await state.set_state(KGDFlow.choose_method)

@router.message(F.text.startswith("📜"))
async def gabarit_info(message: Message, state: FSMContext):
    """Gabarit permit info"""
    t = await get_text(state, 'gabarit_msg')
    await message.answer(t, parse_mode="Markdown")

@router.message(
    F.text.startswith("🛡") | F.text.startswith("🎯") |
    F.text.contains("ISHONCHLI YUKLAR") | F.text.contains("ИШОНЧЛИ ЮКЛАР") |
    F.text.contains("НАДЕЖНЫЕ ГРУЗЫ") | F.text.contains("TRUSTED CARGO") |
    F.text.contains("СЕНІМДІ ЖҮКТЕР") | F.text.contains("ИШЕНИМДҮҮ ЖҮКТӨР") |
    F.text.contains("БОЭЪТИМОД") | F.text.contains("GÜVENİLİR YÜKLER") |
    F.text.contains("YGTYBARLY") | F.text.contains("可靠货物"))
async def coming_soon(message: Message, state: FSMContext):
    """Placeholder for future services"""
    t = await get_text(state, 'coming_soon')
    await message.answer(t)

@router.message(F.text.startswith("🎁"))
async def bonus_menu(message: Message, state: FSMContext):
    """Bonus/referral menu"""
    await state.clear()
    lang = (await db.get_user(message.from_user.id))['language'] if await db.get_user(message.from_user.id) else 'uz'
    await state.update_data(lang=lang)

    t = await get_text(state, 'bonus_menu_msg')
    await message.answer(t, reply_markup=kb.get_bonus_menu_kb(lang))
    await state.set_state(BonusFlow.menu)

@router.message(F.text.startswith("💎"))
async def show_balance(message: Message, state: FSMContext):
    """Show coin balance"""
    balance = await db.get_user_balance(message.from_user.id)
    t = await get_text(state, 'balance_msg', balance=int(balance))
    await message.answer(t, parse_mode="Markdown")

@router.message(F.text.startswith("💬"))
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
    if message.text.startswith("⬅️"):
        lang = await get_user_lang(state)
        await state.clear()
        await message.answer("🏠 Menu", reply_markup=kb.get_main_menu(lang))
        return

    # "ANIQ EMAS" bosilsa - viloyatlar ro'yxatini ko'rsatamiz
    if "ANIQ EMAS" in message.text:
        t = await get_text(state, 'select_viloyat')
        await message.answer(t, reply_markup=kb.get_viloyatlar_kb(), parse_mode="Markdown")
        await state.set_state(EPIKodFlow.select_viloyat_border)
        return

    await state.update_data(border_post=message.text)

    # To'g'ridan-to'g'ri TIF postlarini ko'rsatamiz
    t = await get_text(state, 'select_dest_post')
    await message.answer(t, reply_markup=kb.get_dest_posts_kb())
    await state.set_state(EPIKodFlow.select_dest_post)

@router.message(EPIKodFlow.select_viloyat_border)
async def epi_viloyat_border_selected(message: Message, state: FSMContext):
    """EPI: Viloyat selected for border post (ANIQ EMAS)"""
    if message.text.startswith("⬅️"):
        t = await get_text(state, 'epi_start')
        await message.answer(t, reply_markup=kb.get_posts_kb())
        await state.set_state(EPIKodFlow.select_border_post)
        return

    # Viloyat nomini saqlash
    await state.update_data(border_post=f"ANIQ EMAS ({message.text})")

    # Manzil postini tanlashga o'tish
    t = await get_text(state, 'select_dest_post')
    await message.answer(t, reply_markup=kb.get_dest_posts_kb())
    await state.set_state(EPIKodFlow.select_dest_post)

@router.message(EPIKodFlow.select_dest_post)
async def epi_dest_post_selected(message: Message, state: FSMContext):
    """EPI: Destination post selected"""
    if message.text.startswith("⬅️"):
        t = await get_text(state, 'epi_start')
        await message.answer(t, reply_markup=kb.get_posts_kb())
        await state.set_state(EPIKodFlow.select_border_post)
        return

    # "ANIQ EMAS" bosilsa - viloyatlar ro'yxatini ko'rsatamiz
    if "ANIQ EMAS" in message.text:
        t = await get_text(state, 'select_viloyat')
        await message.answer(t, reply_markup=kb.get_viloyatlar_kb(), parse_mode="Markdown")
        await state.set_state(EPIKodFlow.select_viloyat_dest)
        return

    await state.update_data(dest_post=message.text)

    t = await get_text(state, 'enter_car_number')
    await message.answer(t, reply_markup=kb.get_cancel_kb(await get_user_lang(state)))
    await state.set_state(EPIKodFlow.enter_car_number)

@router.message(EPIKodFlow.select_viloyat_dest)
async def epi_viloyat_dest_selected(message: Message, state: FSMContext):
    """EPI: Viloyat selected for destination post (ANIQ EMAS)"""
    if message.text.startswith("⬅️"):
        t = await get_text(state, 'select_dest_post')
        await message.answer(t, reply_markup=kb.get_dest_posts_kb())
        await state.set_state(EPIKodFlow.select_dest_post)
        return

    # Viloyat nomini saqlash
    await state.update_data(dest_post=f"ANIQ EMAS ({message.text})")

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
    file_type = 'photo'

    if message.photo:
        file_id = message.photo[-1].file_id
        file_size = message.photo[-1].file_size or 0
        file_type = 'photo'
    elif message.document:
        file_id = message.document.file_id
        file_size = message.document.file_size or 0
        file_type = 'document'

    if file_size > MAX_FILE_SIZE:
        await message.reply("⚠️ Fayl juda katta (10MB dan ko'p). Kichikroq fayl yuklang.")
        return

    if file_id:
        current_photos.append({'file_id': file_id, 'type': file_type})
        await state.update_data(photos=current_photos)
        count = len(current_photos)
        await message.reply(f"✅ {count}-fayl qabul qilindi!")

@router.message(EPIKodFlow.collect_docs, F.text)
async def epi_docs_done(message: Message, state: FSMContext, bot: Bot):
    """EPI: Documents upload done"""
    if message.text.startswith("⬅️"):
        t = await get_text(state, 'enter_car_number')
        await message.answer(t, reply_markup=kb.get_cancel_kb(await get_user_lang(state)))
        await state.set_state(EPIKodFlow.enter_car_number)
        return

    # Check if "Done" button pressed (✅ prefix works in all languages)
    if message.text.startswith("✅"):
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
    if message.text.startswith("⬅️"):
        lang = await get_user_lang(state)
        await state.clear()
        await message.answer("🏠 Menu", reply_markup=kb.get_main_menu(lang))
        return

    # "ANIQ EMAS" bosilsa - viloyatlar ro'yxatini ko'rsatamiz
    if "ANIQ EMAS" in message.text:
        t = await get_text(state, 'select_viloyat')
        await message.answer(t, reply_markup=kb.get_viloyatlar_kb(), parse_mode="Markdown")
        await state.set_state(MBDeklaratsiyaFlow.select_viloyat_border)
        return

    await state.update_data(border_post=message.text)

    # To'g'ridan-to'g'ri TIF postlarini ko'rsatamiz
    t = await get_text(state, 'select_dest_post')
    await message.answer(t, reply_markup=kb.get_dest_posts_kb())
    await state.set_state(MBDeklaratsiyaFlow.select_dest_post)

@router.message(MBDeklaratsiyaFlow.select_viloyat_border)
async def mb_viloyat_border_selected(message: Message, state: FSMContext):
    """MB: Viloyat selected for border post (ANIQ EMAS)"""
    if message.text.startswith("⬅️"):
        t = await get_text(state, 'mb_start')
        await message.answer(t, reply_markup=kb.get_posts_kb())
        await state.set_state(MBDeklaratsiyaFlow.select_border_post)
        return

    # Viloyat nomini saqlash
    await state.update_data(border_post=f"ANIQ EMAS ({message.text})")

    # Manzil postini tanlashga o'tish
    t = await get_text(state, 'select_dest_post')
    await message.answer(t, reply_markup=kb.get_dest_posts_kb())
    await state.set_state(MBDeklaratsiyaFlow.select_dest_post)

@router.message(MBDeklaratsiyaFlow.select_dest_post)
async def mb_dest_post_selected(message: Message, state: FSMContext):
    """MB: Destination post selected"""
    if message.text.startswith("⬅️"):
        t = await get_text(state, 'mb_start')
        await message.answer(t, reply_markup=kb.get_posts_kb())
        await state.set_state(MBDeklaratsiyaFlow.select_border_post)
        return

    # "ANIQ EMAS" bosilsa - viloyatlar ro'yxatini ko'rsatamiz
    if "ANIQ EMAS" in message.text:
        t = await get_text(state, 'select_viloyat')
        await message.answer(t, reply_markup=kb.get_viloyatlar_kb(), parse_mode="Markdown")
        await state.set_state(MBDeklaratsiyaFlow.select_viloyat_dest)
        return

    await state.update_data(dest_post=message.text)

    t = await get_text(state, 'enter_car_number')
    await message.answer(t, reply_markup=kb.get_cancel_kb(await get_user_lang(state)))
    await state.set_state(MBDeklaratsiyaFlow.enter_car_number)

@router.message(MBDeklaratsiyaFlow.select_viloyat_dest)
async def mb_viloyat_dest_selected(message: Message, state: FSMContext):
    """MB: Viloyat selected for destination post (ANIQ EMAS)"""
    if message.text.startswith("⬅️"):
        t = await get_text(state, 'select_dest_post')
        await message.answer(t, reply_markup=kb.get_dest_posts_kb())
        await state.set_state(MBDeklaratsiyaFlow.select_dest_post)
        return

    # Viloyat nomini saqlash
    await state.update_data(dest_post=f"ANIQ EMAS ({message.text})")

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
    file_type = 'photo'

    if message.photo:
        file_id = message.photo[-1].file_id
        file_size = message.photo[-1].file_size or 0
        file_type = 'photo'
    elif message.document:
        file_id = message.document.file_id
        file_size = message.document.file_size or 0
        file_type = 'document'

    if file_size > MAX_FILE_SIZE:
        await message.reply("⚠️ Fayl juda katta (10MB dan ko'p). Kichikroq fayl yuklang.")
        return

    if file_id:
        current_photos.append({'file_id': file_id, 'type': file_type})
        await state.update_data(photos=current_photos)
        count = len(current_photos)
        await message.reply(f"✅ {count}-fayl qabul qilindi!")

@router.message(MBDeklaratsiyaFlow.collect_docs, F.text)
async def mb_docs_done(message: Message, state: FSMContext, bot: Bot):
    """MB: Documents upload done"""
    if message.text.startswith("⬅️"):
        t = await get_text(state, 'enter_car_number')
        await message.answer(t, reply_markup=kb.get_cancel_kb(await get_user_lang(state)))
        await state.set_state(MBDeklaratsiyaFlow.enter_car_number)
        return

    if message.text.startswith("✅"):
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
            f"🆕 **YANGI {app_type} ARIZA!**\n\n"
            f"🆔 Kod: `{code}`\n"
            f"🚛 Mashina: `{car_number}`\n"
            f"👤 Foydalanuvchi: [{message.from_user.full_name}](tg://user?id={message.from_user.id})\n"
            f"🆔 Telegram ID: `{message.from_user.id}`\n"
            f"📱 Telefon: {user['phone_number'] if user else 'N/A'}\n"
            f"🌍 Yo'nalish: {direction}\n"
            f"🗣 Til: {data.get('lang', 'uz').upper()}\n\n"
            f"{route}"
        )

        files = data.get('photos', [])

        # Separate photos and documents
        photo_ids = []
        doc_ids = []
        for f in files:
            if isinstance(f, dict):
                if f.get('type') == 'document':
                    doc_ids.append(f['file_id'])
                else:
                    photo_ids.append(f['file_id'])
            else:
                # Backward compatibility: plain file_id string treated as photo
                photo_ids.append(f)

        if not photo_ids and not doc_ids:
            await bot.send_message(ADMIN_GROUP_ID, cap, parse_mode="Markdown")
        else:
            # Send caption as text message first
            await bot.send_message(ADMIN_GROUP_ID, cap, parse_mode="Markdown")

            # Send photos
            if len(photo_ids) == 1:
                await bot.send_photo(ADMIN_GROUP_ID, photo_ids[0])
            elif len(photo_ids) > 1:
                for i in range(0, len(photo_ids), 10):
                    chunk = photo_ids[i:i+10]
                    media = [InputMediaPhoto(media=pid) for pid in chunk]
                    await bot.send_media_group(ADMIN_GROUP_ID, media=media)

            # Send documents (PDFs, Word, Excel, etc.)
            if len(doc_ids) == 1:
                await bot.send_document(ADMIN_GROUP_ID, doc_ids[0])
            elif len(doc_ids) > 1:
                for i in range(0, len(doc_ids), 10):
                    chunk = doc_ids[i:i+10]
                    media = [InputMediaDocument(media=did) for did in chunk]
                    await bot.send_media_group(ADMIN_GROUP_ID, media=media)

        await bot.send_message(ADMIN_GROUP_ID, f"🆔 `{code}` boshqarish:",
                              reply_markup=kb.get_admin_claim_kb(code), parse_mode="Markdown")
        print(f"✅ Admin guruhga yuborildi: {code}")
    except Exception as e:
        print(f"❌ Admin send error [{code}]: {e}")
        import traceback
        traceback.print_exc()
        try:
            await bot.send_message(ADMIN_GROUP_ID, f"🆕 Ariza: {code} (Xatolik: {e})")
        except Exception as e2:
            print(f"❌ Admin fallback send also failed: {e2}")
        # Foydalanuvchiga ham xabar beramiz
        try:
            await message.answer(f"⚠️ Texnik xatolik yuz berdi. Iltimos admin bilan bog'laning: @CARAVAN_TRANZIT")
        except:
            pass

# ==========================================================
# 6. APPLICATIONS FLOW
# ==========================================================

@router.message(ApplicationsFlow.choose_option)
async def apps_option_chosen(message: Message, state: FSMContext):
    """Applications: Option chosen"""
    if message.text.startswith("⬅️"):
        lang = await get_user_lang(state)
        await state.clear()
        await message.answer("🏠 Menu", reply_markup=kb.get_main_menu(lang))
        return

    if message.text.startswith("🔍"):
        t = await get_text(state, 'search_app_car')
        await message.answer(t, reply_markup=kb.get_cancel_kb(await get_user_lang(state)))
        await state.set_state(ApplicationsFlow.enter_car_for_search)
    elif message.text.startswith("📂"):
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
    if message.text.startswith("⬅️"):
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

    if message.text.startswith("⬅️"):
        await state.clear()
        await message.answer("🏠 Menu", reply_markup=kb.get_main_menu(lang))
        return

    if message.text.startswith("📱"):
        t = await get_text(state, 'change_phone_msg')
        await message.answer(t, reply_markup=kb.get_phone_kb(lang))
        await state.set_state(SettingsFlow.change_phone)

    elif message.text.startswith("🌐"):
        t = await get_text(state, 'change_lang_msg')
        await message.answer(t, reply_markup=kb.get_lang_kb())
        await state.set_state(SettingsFlow.change_language)

    elif message.text.startswith("🗑"):
        await db.clear_user_cache(message.from_user.id)
        t = await get_text(state, 'cache_cleared_msg')
        await message.answer(t)
        await message.answer("🏠 Menu", reply_markup=kb.get_main_menu(lang))
        await state.clear()

    elif message.text.startswith("👨‍💼"):
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

    if message.text.startswith("⬅️"):
        await state.clear()
        await message.answer("🏠 Menu", reply_markup=kb.get_main_menu(lang))
        return

    if message.text.startswith("📱"):
        t = await get_text(state, 'kgd_app_msg')
        await message.answer(t, reply_markup=kb.get_kgd_app_submenu_kb(lang), parse_mode="Markdown")

    elif message.text.startswith("👥"):
        t = await get_text(state, 'kgd_staff_car')
        await message.answer(t, reply_markup=kb.get_cancel_kb(lang))
        await state.set_state(KGDFlow.enter_car_number)

@router.message(KGDFlow.enter_car_number)
async def kgd_car_entered(message: Message, state: FSMContext, bot: Bot):
    """KGD: Car number entered for staff check"""
    if message.text.startswith("⬅️"):
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

    if message.text.startswith("⬅️"):
        await state.clear()
        await message.answer("🏠 Menu", reply_markup=kb.get_main_menu(lang))
        return

    if message.text.startswith("🔗"):
        bot_username = (await message.bot.me()).username
        referral_link = f"https://t.me/{bot_username}?start={message.from_user.id}"
        t = await get_text(state, 'get_referral_link', link=referral_link)
        await message.answer(t, parse_mode="Markdown")

    elif message.text.startswith("ℹ️"):
        t = await get_text(state, 'bonus_info')
        await message.answer(t, parse_mode="Markdown")

    elif message.text.startswith("💎"):
        balance = await db.get_user_balance(message.from_user.id)
        t = await get_text(state, 'balance_msg', balance=int(balance))
        await message.answer(t, parse_mode="Markdown")

# ==========================================================
# 10. CHAT FLOW
# ==========================================================

@router.message(ChatFlow.waiting_message)
async def chat_message_received(message: Message, state: FSMContext, bot: Bot):
    """Chat: Message received - davom etadigan chat"""
    text = message.text or ""

    # Agar "Chatni tugatish" (🏁) yoki "Ortga" (⬅️) yoki "Bekor" (❌) bosilsa
    if text.startswith("🏁") or text.startswith("⬅️") or text.startswith("❌"):
        lang = await get_user_lang(state)
        await state.clear()
        t = await get_text(state, 'chat_ended')
        await message.answer(t if t else "✅ Chat tugadi. Asosiy menyu:", reply_markup=kb.get_main_menu(lang))
        return

    # Send to admin group
    try:
        await bot.send_message(
            ADMIN_GROUP_ID,
            f"💬 **XABAR (GAPLASHISH)**\n\n"
            f"👤: [{message.from_user.full_name}](tg://user?id={message.from_user.id})\n"
            f"🆔: `{message.from_user.id}`\n"
            f"📝: {text}",
            parse_mode="Markdown"
        )
    except Exception as e:
        print(f"Error sending chat message: {e}")

    # Chat davom etadi - state tozalanmaydi!
    t = await get_text(state, 'chat_continue')
    lang = await get_user_lang(state)
    await message.answer(t if t else "✅ Xabar yuborildi! Yana yozing yoki chatni tugating.", reply_markup=kb.get_chat_kb(lang))
    # State saqlanadi - chat davom etadi
    await state.set_state(ChatFlow.waiting_message)

# ==========================================================
# 11. ADMIN HANDLERS
# ==========================================================

# NOTE: Admin callback handlers (claim_, reject_, setprice_) and admin_group_handler
# are in admin_handlers.py which is registered first in main.py

# ==========================================================
# 12. GLOBAL HANDLERS
# ==========================================================

@router.message(F.text.startswith("⬅️"))
async def global_back_button(message: Message, state: FSMContext):
    """Global back button handler"""
    current_state = await state.get_state()

    if current_state is None:
        return  # Already at main menu

    lang = await get_user_lang(state)
    await state.clear()
    await state.update_data(lang=lang)
    await message.answer("🏠 Menu", reply_markup=kb.get_main_menu(lang))

@router.message(F.text.startswith("❌"))
async def global_cancel_button(message: Message, state: FSMContext):
    """Global cancel button handler"""
    lang = await get_user_lang(state)
    await state.clear()
    await state.update_data(lang=lang)
    await message.answer("🏠 Menu", reply_markup=kb.get_main_menu(lang))

# ==========================================================
# 13. CATCH-ALL HANDLERS (prevent "Update is not handled" logs)
# ==========================================================

@router.callback_query()
async def unhandled_callback_query(call: CallbackQuery):
    """Catch-all handler for unhandled callback queries"""
    # Just answer to prevent timeout and suppress logs
    await call.answer()

@router.message()
async def unhandled_message(message: Message, state: FSMContext):
    """Catch-all handler for unhandled messages - redirect to main menu"""
    # Skip messages from admin group that are not commands
    if message.chat.id == ADMIN_GROUP_ID:
        return

    # Get user language and show main menu
    try:
        user = await db.get_user(message.from_user.id)
        lang = user['language'] if user else 'uz'
        await state.update_data(lang=lang)
        await message.answer(
            "🏠 Asosiy menyu:\n\nQuyidagi tugmalardan birini tanlang:",
            reply_markup=kb.get_main_menu(lang)
        )
    except:
        # Fallback to default language
        await message.answer(
            "🏠 Asosiy menyu:\n\nQuyidagi tugmalardan birini tanlang:",
            reply_markup=kb.get_main_menu('uz')
        )
