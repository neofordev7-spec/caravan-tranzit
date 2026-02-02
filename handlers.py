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

def _all_texts(key):
    """Get set of all translations for a key across all languages"""
    return {TEXTS[lang].get(key, '') for lang in TEXTS} - {''}

def _text_in_any(text, key):
    """Check if text contains any translation of key"""
    if not text:
        return False
    for lang_code in TEXTS:
        val = TEXTS[lang_code].get(key, '')
        if val and val in text:
            return True
    return False

def _menu_filter(*keys):
    """Create filter matching any of the given translation keys"""
    all_values = set()
    for key in keys:
        all_values.update(_all_texts(key))
    return F.text.func(lambda t: any(v in t for v in all_values) if t else False)

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
                    referrer_lang = (await db.get_user(referrer_id))['language'] if await db.get_user(referrer_id) else 'uz'
                    msg = TEXTS.get(referrer_lang, TEXTS['uz'])['referral_new_friend'].format(name=message.from_user.full_name)
                    await bot.send_message(referrer_id, msg, parse_mode="Markdown")
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

@router.message(_menu_filter('menu_epi'))
async def start_epi_kod(message: Message, state: FSMContext):
    """EPI KOD AT DEKLARATSIYA flow"""
    await state.clear()
    lang = (await db.get_user(message.from_user.id))['language'] if await db.get_user(message.from_user.id) else 'uz'
    await state.update_data(lang=lang, service_type='EPI')

    t = await get_text(state, 'epi_start')
    await message.answer(t, reply_markup=kb.get_posts_kb(lang))
    await state.set_state(EPIKodFlow.select_border_post)

@router.message(_menu_filter('menu_mb'))
async def start_mb_deklaratsiya(message: Message, state: FSMContext):
    """MB DEKLARATSIYA flow"""
    await state.clear()
    lang = (await db.get_user(message.from_user.id))['language'] if await db.get_user(message.from_user.id) else 'uz'
    await state.update_data(lang=lang, service_type='MB')

    t = await get_text(state, 'mb_start')
    await message.answer(t, reply_markup=kb.get_posts_kb(lang))
    await state.set_state(MBDeklaratsiyaFlow.select_border_post)

@router.message(_menu_filter('menu_contacts'))
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

    if _text_in_any(message.text, 'btn_back'):
        await state.clear()
        await message.answer(TEXTS.get(lang, TEXTS['uz'])['menu_text'], reply_markup=kb.get_main_menu(lang))
        return

    if _text_in_any(message.text, 'btn_change_phone'):
        # Raqamni o'zgartirish
        t = await get_text(state, 'change_phone_msg')
        await message.answer(t, reply_markup=kb.get_phone_kb(lang))
        await state.set_state(ContactInfoFlow.change_phone)

    elif _text_in_any(message.text, 'btn_change_lang'):
        # Tilni o'zgartirish
        t = await get_text(state, 'change_lang_msg')
        await message.answer(t, reply_markup=kb.get_lang_kb())
        await state.set_state(ContactInfoFlow.change_language)

    elif _text_in_any(message.text, 'btn_clear_cache'):
        # Xotirani tozalash
        await db.clear_user_cache(message.from_user.id)
        t = await get_text(state, 'cache_cleared_msg')
        await message.answer(t)
        await message.answer(TEXTS.get(lang, TEXTS['uz'])['menu_text'], reply_markup=kb.get_main_menu(lang))
        await state.clear()

    elif _text_in_any(message.text, 'btn_admin_contact'):
        # Admin bilan aloqa - 3 ta tugma
        t = await get_text(state, 'admin_contact_msg')
        await message.answer(
            "📞 **ADMIN BILAN ALOQA:**\n\n"
            "📱 **Telefon raqamlar:**\n"
            "• +998 91 702 00 99\n"
            "• +998 94 312 00 99\n\n"
            "💬 **Telegram:**\n"
            "• @CARAVAN_TRANZIT\n"
            "• @caravan_tranzit1\n\n"
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

    t = await get_text(state, 'phone_changed')
    await message.answer(t)
    lang = await get_user_lang(state)
    await message.answer(TEXTS.get(lang, TEXTS['uz'])['menu_text'], reply_markup=kb.get_main_menu(lang))
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
    await call.message.answer(TEXTS[new_lang]['lang_changed'])
    await call.message.answer(TEXTS.get(new_lang, TEXTS['uz'])['menu_text'], reply_markup=kb.get_main_menu(new_lang))
    await state.clear()
    await state.update_data(lang=new_lang)

@router.message(_menu_filter('menu_apps'))
async def my_applications(message: Message, state: FSMContext):
    """My applications menu"""
    await state.clear()
    lang = (await db.get_user(message.from_user.id))['language'] if await db.get_user(message.from_user.id) else 'uz'
    await state.update_data(lang=lang)

    t = await get_text(state, 'apps_menu')
    await message.answer(t, reply_markup=kb.get_applications_menu_kb(lang))
    await state.set_state(ApplicationsFlow.choose_option)

@router.message(_menu_filter('menu_settings'))
async def settings_menu(message: Message, state: FSMContext):
    """Settings menu"""
    await state.clear()
    lang = (await db.get_user(message.from_user.id))['language'] if await db.get_user(message.from_user.id) else 'uz'
    await state.update_data(lang=lang)

    t = await get_text(state, 'settings_menu')
    await message.answer(t, reply_markup=kb.get_settings_kb(lang))
    await state.set_state(SettingsFlow.menu)

@router.message(_menu_filter('menu_prices'))
async def show_prices(message: Message, state: FSMContext):
    """Show prices catalog"""
    t = await get_text(state, 'prices_catalog')
    await message.answer(t, parse_mode="HTML")

@router.message(_menu_filter('menu_app'))
async def app_download(message: Message, state: FSMContext):
    """App download menu"""
    lang = await get_user_lang(state)
    t = await get_text(state, 'app_download_msg')
    await message.answer(t, reply_markup=kb.get_app_download_kb(lang))

@router.message(_menu_filter('menu_kgd'))
async def kgd_menu(message: Message, state: FSMContext):
    """KGD viewing menu"""
    await state.clear()
    lang = (await db.get_user(message.from_user.id))['language'] if await db.get_user(message.from_user.id) else 'uz'
    await state.update_data(lang=lang)

    t = await get_text(state, 'kgd_menu_msg')
    await message.answer(t, reply_markup=kb.get_kgd_menu_kb(lang))
    await state.set_state(KGDFlow.choose_method)

@router.message(_menu_filter('menu_gabarit'))
async def gabarit_info(message: Message, state: FSMContext):
    """Gabarit permit info"""
    t = await get_text(state, 'gabarit_msg')
    await message.answer(t, parse_mode="Markdown")

@router.message(_menu_filter('menu_sugurta', 'menu_navbat', 'menu_yuklar'))
async def coming_soon(message: Message, state: FSMContext):
    """Placeholder for future services"""
    t = await get_text(state, 'coming_soon')
    await message.answer(t)

@router.message(_menu_filter('menu_bonus'))
async def bonus_menu(message: Message, state: FSMContext):
    """Bonus/referral menu"""
    await state.clear()
    lang = (await db.get_user(message.from_user.id))['language'] if await db.get_user(message.from_user.id) else 'uz'
    await state.update_data(lang=lang)

    t = await get_text(state, 'bonus_menu_msg')
    await message.answer(t, reply_markup=kb.get_bonus_menu_kb(lang))
    await state.set_state(BonusFlow.menu)

@router.message(_menu_filter('menu_balance'))
async def show_balance(message: Message, state: FSMContext):
    """Show coin balance"""
    balance = await db.get_user_balance(message.from_user.id)
    t = await get_text(state, 'balance_msg', balance=int(balance))
    await message.answer(t, parse_mode="Markdown")

@router.message(_menu_filter('menu_social'))
async def social_media(message: Message, state: FSMContext):
    """Show social media links"""
    t = await get_text(state, 'social_msg')
    await message.answer(t, reply_markup=kb.get_social_media_kb())

@router.message(_menu_filter('menu_chat'))
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
    if _text_in_any(message.text, 'btn_back'):
        lang = await get_user_lang(state)
        await state.clear()
        await message.answer(TEXTS.get(lang, TEXTS['uz'])['menu_text'], reply_markup=kb.get_main_menu(lang))
        return

    # "ANIQ EMAS" bosilsa - viloyatlar ro'yxatini ko'rsatamiz
    if _text_in_any(message.text, 'btn_unknown_post'):
        lang = await get_user_lang(state)
        t = await get_text(state, 'viloyat_select')
        await message.answer(
            t,
            reply_markup=kb.get_viloyatlar_kb(lang),
            parse_mode="Markdown"
        )
        await state.set_state(EPIKodFlow.select_viloyat_border)
        return

    await state.update_data(border_post=message.text)

    # To'g'ridan-to'g'ri TIF postlarini ko'rsatamiz
    lang = await get_user_lang(state)
    t = await get_text(state, 'select_dest_post')
    await message.answer(t, reply_markup=kb.get_dest_posts_kb(lang))
    await state.set_state(EPIKodFlow.select_dest_post)

@router.message(EPIKodFlow.select_viloyat_border)
async def epi_viloyat_border_selected(message: Message, state: FSMContext):
    """EPI: Viloyat selected for border post (ANIQ EMAS)"""
    if _text_in_any(message.text, 'btn_back'):
        lang = await get_user_lang(state)
        t = await get_text(state, 'epi_start')
        await message.answer(t, reply_markup=kb.get_posts_kb(lang))
        await state.set_state(EPIKodFlow.select_border_post)
        return

    # Viloyat nomini saqlash
    await state.update_data(border_post=f"ANIQ EMAS ({message.text})")

    # Manzil postini tanlashga o'tish
    lang = await get_user_lang(state)
    t = await get_text(state, 'select_dest_post')
    await message.answer(t, reply_markup=kb.get_dest_posts_kb(lang))
    await state.set_state(EPIKodFlow.select_dest_post)

@router.message(EPIKodFlow.select_dest_post)
async def epi_dest_post_selected(message: Message, state: FSMContext):
    """EPI: Destination post selected"""
    if _text_in_any(message.text, 'btn_back'):
        lang = await get_user_lang(state)
        t = await get_text(state, 'epi_start')
        await message.answer(t, reply_markup=kb.get_posts_kb(lang))
        await state.set_state(EPIKodFlow.select_border_post)
        return

    # "ANIQ EMAS" bosilsa - viloyatlar ro'yxatini ko'rsatamiz
    if _text_in_any(message.text, 'btn_unknown_post'):
        lang = await get_user_lang(state)
        t = await get_text(state, 'viloyat_select')
        await message.answer(
            t,
            reply_markup=kb.get_viloyatlar_kb(lang),
            parse_mode="Markdown"
        )
        await state.set_state(EPIKodFlow.select_viloyat_dest)
        return

    await state.update_data(dest_post=message.text)

    t = await get_text(state, 'enter_car_number')
    await message.answer(t, reply_markup=kb.get_cancel_kb(await get_user_lang(state)))
    await state.set_state(EPIKodFlow.enter_car_number)

@router.message(EPIKodFlow.select_viloyat_dest)
async def epi_viloyat_dest_selected(message: Message, state: FSMContext):
    """EPI: Viloyat selected for destination post (ANIQ EMAS)"""
    if _text_in_any(message.text, 'btn_back'):
        lang = await get_user_lang(state)
        t = await get_text(state, 'select_dest_post')
        await message.answer(t, reply_markup=kb.get_dest_posts_kb(lang))
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
        t = await get_text(state, 'error_not_text')
        await message.reply(t)
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
        t = await get_text(state, 'error_file_large')
        await message.reply(t)
        return

    if file_id:
        current_photos.append(file_id)
        await state.update_data(photos=current_photos)

@router.message(EPIKodFlow.collect_docs, F.text)
async def epi_docs_done(message: Message, state: FSMContext, bot: Bot):
    """EPI: Documents upload done"""
    if _text_in_any(message.text, 'btn_back'):
        t = await get_text(state, 'enter_car_number')
        await message.answer(t, reply_markup=kb.get_cancel_kb(await get_user_lang(state)))
        await state.set_state(EPIKodFlow.enter_car_number)
        return

    # Check if "Done" button pressed
    if _text_in_any(message.text, 'btn_done'):
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
    if _text_in_any(message.text, 'btn_back'):
        lang = await get_user_lang(state)
        await state.clear()
        await message.answer(TEXTS.get(lang, TEXTS['uz'])['menu_text'], reply_markup=kb.get_main_menu(lang))
        return

    # "ANIQ EMAS" bosilsa - viloyatlar ro'yxatini ko'rsatamiz
    if _text_in_any(message.text, 'btn_unknown_post'):
        lang = await get_user_lang(state)
        t = await get_text(state, 'viloyat_select')
        await message.answer(
            t,
            reply_markup=kb.get_viloyatlar_kb(lang),
            parse_mode="Markdown"
        )
        await state.set_state(MBDeklaratsiyaFlow.select_viloyat_border)
        return

    await state.update_data(border_post=message.text)

    # To'g'ridan-to'g'ri TIF postlarini ko'rsatamiz
    lang = await get_user_lang(state)
    t = await get_text(state, 'select_dest_post')
    await message.answer(t, reply_markup=kb.get_dest_posts_kb(lang))
    await state.set_state(MBDeklaratsiyaFlow.select_dest_post)

@router.message(MBDeklaratsiyaFlow.select_viloyat_border)
async def mb_viloyat_border_selected(message: Message, state: FSMContext):
    """MB: Viloyat selected for border post (ANIQ EMAS)"""
    if _text_in_any(message.text, 'btn_back'):
        lang = await get_user_lang(state)
        t = await get_text(state, 'mb_start')
        await message.answer(t, reply_markup=kb.get_posts_kb(lang))
        await state.set_state(MBDeklaratsiyaFlow.select_border_post)
        return

    # Viloyat nomini saqlash
    await state.update_data(border_post=f"ANIQ EMAS ({message.text})")

    # Manzil postini tanlashga o'tish
    lang = await get_user_lang(state)
    t = await get_text(state, 'select_dest_post')
    await message.answer(t, reply_markup=kb.get_dest_posts_kb(lang))
    await state.set_state(MBDeklaratsiyaFlow.select_dest_post)

@router.message(MBDeklaratsiyaFlow.select_dest_post)
async def mb_dest_post_selected(message: Message, state: FSMContext):
    """MB: Destination post selected"""
    if _text_in_any(message.text, 'btn_back'):
        lang = await get_user_lang(state)
        t = await get_text(state, 'mb_start')
        await message.answer(t, reply_markup=kb.get_posts_kb(lang))
        await state.set_state(MBDeklaratsiyaFlow.select_border_post)
        return

    # "ANIQ EMAS" bosilsa - viloyatlar ro'yxatini ko'rsatamiz
    if _text_in_any(message.text, 'btn_unknown_post'):
        lang = await get_user_lang(state)
        t = await get_text(state, 'viloyat_select')
        await message.answer(
            t,
            reply_markup=kb.get_viloyatlar_kb(lang),
            parse_mode="Markdown"
        )
        await state.set_state(MBDeklaratsiyaFlow.select_viloyat_dest)
        return

    await state.update_data(dest_post=message.text)

    t = await get_text(state, 'enter_car_number')
    await message.answer(t, reply_markup=kb.get_cancel_kb(await get_user_lang(state)))
    await state.set_state(MBDeklaratsiyaFlow.enter_car_number)

@router.message(MBDeklaratsiyaFlow.select_viloyat_dest)
async def mb_viloyat_dest_selected(message: Message, state: FSMContext):
    """MB: Viloyat selected for destination post (ANIQ EMAS)"""
    if _text_in_any(message.text, 'btn_back'):
        lang = await get_user_lang(state)
        t = await get_text(state, 'select_dest_post')
        await message.answer(t, reply_markup=kb.get_dest_posts_kb(lang))
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
        t = await get_text(state, 'error_not_text')
        await message.reply(t)
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
        t = await get_text(state, 'error_file_large')
        await message.reply(t)
        return

    if file_id:
        current_photos.append(file_id)
        await state.update_data(photos=current_photos)

@router.message(MBDeklaratsiyaFlow.collect_docs, F.text)
async def mb_docs_done(message: Message, state: FSMContext, bot: Bot):
    """MB: Documents upload done"""
    if _text_in_any(message.text, 'btn_back'):
        t = await get_text(state, 'enter_car_number')
        await message.answer(t, reply_markup=kb.get_cancel_kb(await get_user_lang(state)))
        await state.set_state(MBDeklaratsiyaFlow.enter_car_number)
        return

    if _text_in_any(message.text, 'btn_done'):
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
    if _text_in_any(message.text, 'btn_back'):
        lang = await get_user_lang(state)
        await state.clear()
        await message.answer(TEXTS.get(lang, TEXTS['uz'])['menu_text'], reply_markup=kb.get_main_menu(lang))
        return

    if _text_in_any(message.text, 'btn_search_app'):
        t = await get_text(state, 'search_app_car')
        await message.answer(t, reply_markup=kb.get_cancel_kb(await get_user_lang(state)))
        await state.set_state(ApplicationsFlow.enter_car_for_search)
    elif _text_in_any(message.text, 'btn_my_apps'):
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
    if _text_in_any(message.text, 'btn_back'):
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

    if _text_in_any(message.text, 'btn_back'):
        await state.clear()
        await message.answer(TEXTS.get(lang, TEXTS['uz'])['menu_text'], reply_markup=kb.get_main_menu(lang))
        return

    if _text_in_any(message.text, 'btn_change_phone'):
        t = await get_text(state, 'change_phone_msg')
        await message.answer(t, reply_markup=kb.get_phone_kb(lang))
        await state.set_state(SettingsFlow.change_phone)

    elif _text_in_any(message.text, 'btn_change_lang'):
        t = await get_text(state, 'change_lang_msg')
        await message.answer(t, reply_markup=kb.get_lang_kb())
        await state.set_state(SettingsFlow.change_language)

    elif _text_in_any(message.text, 'btn_clear_cache'):
        await db.clear_user_cache(message.from_user.id)
        t = await get_text(state, 'cache_cleared_msg')
        await message.answer(t)
        await message.answer(TEXTS.get(lang, TEXTS['uz'])['menu_text'], reply_markup=kb.get_main_menu(lang))
        await state.clear()

    elif _text_in_any(message.text, 'btn_admin_contact'):
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

    t = await get_text(state, 'phone_changed')
    await message.answer(t)
    lang = await get_user_lang(state)
    await message.answer(TEXTS.get(lang, TEXTS['uz'])['menu_text'], reply_markup=kb.get_main_menu(lang))
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
    await call.message.answer(TEXTS[new_lang]['lang_changed'])
    await call.message.answer(TEXTS.get(new_lang, TEXTS['uz'])['menu_text'], reply_markup=kb.get_main_menu(new_lang))
    await state.clear()
    await state.update_data(lang=new_lang)

# ==========================================================
# 8. KGD FLOW
# ==========================================================

@router.message(KGDFlow.choose_method)
async def kgd_method_chosen(message: Message, state: FSMContext):
    """KGD: Method chosen"""
    lang = await get_user_lang(state)

    if _text_in_any(message.text, 'btn_back'):
        await state.clear()
        await message.answer(TEXTS.get(lang, TEXTS['uz'])['menu_text'], reply_markup=kb.get_main_menu(lang))
        return

    if _text_in_any(message.text, 'btn_kgd_app'):
        t = await get_text(state, 'kgd_app_msg')
        await message.answer(t, reply_markup=kb.get_kgd_app_submenu_kb(lang), parse_mode="Markdown")

    elif _text_in_any(message.text, 'btn_kgd_staff'):
        t = await get_text(state, 'kgd_staff_car')
        await message.answer(t, reply_markup=kb.get_cancel_kb(lang))
        await state.set_state(KGDFlow.enter_car_number)

@router.message(KGDFlow.enter_car_number)
async def kgd_car_entered(message: Message, state: FSMContext, bot: Bot):
    """KGD: Car number entered for staff check"""
    if _text_in_any(message.text, 'btn_back'):
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
    t = await get_text(state, 'request_sent')
    await message.answer(t, reply_markup=kb.get_main_menu(lang))
    await state.clear()

# ==========================================================
# 9. BONUS FLOW
# ==========================================================

@router.message(BonusFlow.menu)
async def bonus_option_chosen(message: Message, state: FSMContext):
    """Bonus: Option chosen"""
    lang = await get_user_lang(state)

    if _text_in_any(message.text, 'btn_back'):
        await state.clear()
        await message.answer(TEXTS.get(lang, TEXTS['uz'])['menu_text'], reply_markup=kb.get_main_menu(lang))
        return

    if _text_in_any(message.text, 'btn_get_link'):
        bot_username = (await message.bot.me()).username
        referral_link = f"https://t.me/{bot_username}?start={message.from_user.id}"
        t = await get_text(state, 'get_referral_link', link=referral_link)
        await message.answer(t, parse_mode="Markdown")

    elif _text_in_any(message.text, 'btn_bonus_info'):
        t = await get_text(state, 'bonus_info')
        await message.answer(t, parse_mode="Markdown")

    elif _text_in_any(message.text, 'btn_my_coins'):
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

    # Agar "Chatni tugatish" yoki "Ortga" yoki "Bekor" bosilsa - chatni tugatish
    if _text_in_any(text, 'btn_end_chat') or _text_in_any(text, 'btn_back') or _text_in_any(text, 'btn_cancel'):
        lang = await get_user_lang(state)
        await state.clear()
        t = await get_text(state, 'chat_ended')
        fallback_t = TEXTS.get(lang, TEXTS['uz']).get('chat_ended', '✅')
        await message.answer(t if t != "..." else fallback_t, reply_markup=kb.get_main_menu(lang))
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
    fallback_t = TEXTS.get(lang, TEXTS['uz']).get('chat_continue', '✅')
    await message.answer(t if t != "..." else fallback_t, reply_markup=kb.get_chat_kb(lang))
    # State saqlanadi - chat davom etadi
    await state.set_state(ChatFlow.waiting_message)

# ==========================================================
# 11. ADMIN HANDLERS
# ==========================================================

@router.callback_query(F.data.startswith("claim_"))
async def admin_claim(call: CallbackQuery, bot: Bot):
    """Admin claims application"""
    code = call.data.split("_")[1]
    if await db.claim_application(code, call.from_user.id):
        await call.message.edit_text(
            f"✅ **QABUL QILINDI**\n\n"
            f"🆔 Kod: `{code}`\n"
            f"👤 Admin: {call.from_user.full_name}\n\n"
            f"💰 Narx belgilang:",
            parse_mode="Markdown",
            reply_markup=kb.get_pricing_kb(code)
        )
        # Foydalanuvchiga xabar
        app = await db.get_application_by_code(code)
        if app:
            try:
                user_lang = (await db.get_user(app['user_id']))['language'] if await db.get_user(app['user_id']) else 'uz'
                msg = TEXTS.get(user_lang, TEXTS['uz'])['app_accepted_user'].format(code=code)
                await bot.send_message(app['user_id'], msg, parse_mode="Markdown")
            except:
                pass
        await call.answer("✅ Qabul qilindi!")
    else:
        await call.answer("❌ Bu ariza allaqachon olingan!", show_alert=True)

@router.callback_query(F.data.startswith("reject_"))
async def admin_reject(call: CallbackQuery, bot: Bot):
    """Admin rejects application"""
    code = call.data.split("_")[1]
    app = await db.get_application_by_code(code)

    if not app:
        await call.answer("❌ Ariza topilmadi!", show_alert=True)
        return

    # Statusni yangilash
    await db.update_application_status(code, 'rejected')

    # Admin guruhda xabarni yangilash
    await call.message.edit_text(
        f"❌ **RAD ETILDI**\n\n"
        f"🆔 Kod: `{code}`\n"
        f"👤 Admin: {call.from_user.full_name}",
        parse_mode="Markdown"
    )

    # Foydalanuvchiga xabar
    try:
        user_lang = (await db.get_user(app['user_id']))['language'] if await db.get_user(app['user_id']) else 'uz'
        msg = TEXTS.get(user_lang, TEXTS['uz'])['app_rejected_user'].format(code=code)
        await bot.send_message(app['user_id'], msg, parse_mode="Markdown")
    except:
        pass

    await call.answer("❌ Ariza rad etildi!")

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
    """Handle admin group messages - deklaratsiya va javoblarni userga yuborish"""
    txt = message.text or message.caption or ""

    # 1. Reply to message bo'lsa - original xabardagi userga javob yuborish
    if message.reply_to_message:
        orig = message.reply_to_message.text or message.reply_to_message.caption or ""
        match = re.search(r"(?:ID|🆔|Telegram ID):\s*`?(\d+)`?", orig)
        if match:
            try:
                user_id = int(match.group(1))
                user_lang = (await db.get_user(user_id))['language'] if await db.get_user(user_id) else 'uz'
                decl_text = TEXTS.get(user_lang, TEXTS['uz'])['declaration_ready']
                admin_reply = TEXTS.get(user_lang, TEXTS['uz'])['admin_reply_prefix']
                # Rasm/fayl bo'lsa uni ham yuborish
                if message.photo:
                    await bot.send_photo(
                        user_id,
                        message.photo[-1].file_id,
                        caption=f"{decl_text}\n\n{txt}" if txt else decl_text,
                        parse_mode="Markdown"
                    )
                elif message.document:
                    await bot.send_document(
                        user_id,
                        message.document.file_id,
                        caption=f"{decl_text}\n\n{txt}" if txt else decl_text,
                        parse_mode="Markdown"
                    )
                else:
                    await bot.send_message(
                        user_id,
                        f"{admin_reply}\n\n{txt}",
                        parse_mode="Markdown"
                    )
                await message.reply("✅ Foydalanuvchiga yuborildi!")
            except Exception as e:
                await message.reply(f"❌ Yuborib bo'lmadi: {e}")
            return

    # 2. EPI kod yoki MB kod bo'yicha qidirish (EPI-12345 yoki MB-12345)
    epi_match = re.search(r"\b(EPI|MB)-(\d{5})\b", txt.upper())
    if epi_match:
        app_code = f"{epi_match.group(1)}-{epi_match.group(2)}"
        app = await db.get_application_by_code(app_code)
        if app:
            try:
                user_lang = (await db.get_user(app['user_id']))['language'] if await db.get_user(app['user_id']) else 'uz'
                decl_ready = TEXTS.get(user_lang, TEXTS['uz']).get('declaration_ready_code', '📋 **DEKLARATSIYA TAYYOR!**\n\n🆔 Kod: `{code}`').format(code=app_code)
                admin_reply = TEXTS.get(user_lang, TEXTS['uz'])['admin_reply_prefix']
                # Rasm/fayl bo'lsa uni ham yuborish
                if message.photo:
                    await bot.send_photo(
                        app['user_id'],
                        message.photo[-1].file_id,
                        caption=f"{decl_ready}\n\n{txt}",
                        parse_mode="Markdown"
                    )
                elif message.document:
                    await bot.send_document(
                        app['user_id'],
                        message.document.file_id,
                        caption=f"{decl_ready}\n\n{txt}",
                        parse_mode="Markdown"
                    )
                else:
                    await bot.send_message(
                        app['user_id'],
                        f"{decl_ready}\n\n{admin_reply} {txt}",
                        parse_mode="Markdown"
                    )
                await message.reply(f"✅ {app_code} - foydalanuvchiga yuborildi!")
                # Statusni yangilash
                await db.update_application_status(app_code, 'completed')
            except Exception as e:
                await message.reply(f"❌ Yuborib bo'lmadi: {e}")
            return

    # 3. Mashina raqami bo'yicha qidirish (01A777AA yoki 12345AAA)
    car_match = re.search(r"\b(\d{2}[A-Z]\d{3}[A-Z]{2})\b|\b(\d{5}[A-Z]{3})\b", txt.upper())
    if car_match:
        vehicle_number = car_match.group(1) or car_match.group(2)
        app = await db.get_app_by_car_number(vehicle_number)
        if app:
            try:
                user_lang = (await db.get_user(app['user_id']))['language'] if await db.get_user(app['user_id']) else 'uz'
                decl_text = TEXTS.get(user_lang, TEXTS['uz'])['declaration_ready']
                admin_reply = TEXTS.get(user_lang, TEXTS['uz'])['admin_reply_prefix']
                # Rasm/fayl bo'lsa uni ham yuborish
                if message.photo:
                    await bot.send_photo(
                        app['user_id'],
                        message.photo[-1].file_id,
                        caption=f"{decl_text}\n\n{txt}",
                        parse_mode="Markdown"
                    )
                elif message.document:
                    await bot.send_document(
                        app['user_id'],
                        message.document.file_id,
                        caption=f"{decl_text}\n\n{txt}",
                        parse_mode="Markdown"
                    )
                else:
                    await bot.send_message(
                        app['user_id'],
                        f"{decl_text}\n\n{admin_reply} {txt}",
                        parse_mode="Markdown"
                    )
                await message.reply(f"✅ {vehicle_number} - foydalanuvchiga yuborildi!")
                # Statusni yangilash
                await db.update_application_status(app['app_code'], 'completed')
            except Exception as e:
                await message.reply(f"❌ Yuborib bo'lmadi: {e}")

# ==========================================================
# 12. GLOBAL HANDLERS
# ==========================================================

@router.message(F.text.func(lambda t: _text_in_any(t, 'btn_back') if t else False))
async def global_back_button(message: Message, state: FSMContext):
    """Global back button handler"""
    current_state = await state.get_state()

    if current_state is None:
        return  # Already at main menu

    lang = await get_user_lang(state)
    await state.clear()
    await state.update_data(lang=lang)
    await message.answer(TEXTS.get(lang, TEXTS['uz'])['menu_text'], reply_markup=kb.get_main_menu(lang))

@router.message(F.text.func(lambda t: _text_in_any(t, 'btn_cancel') if t else False))
async def global_cancel_button(message: Message, state: FSMContext):
    """Global cancel button handler"""
    lang = await get_user_lang(state)
    await state.clear()
    await state.update_data(lang=lang)
    await message.answer(TEXTS.get(lang, TEXTS['uz'])['menu_text'], reply_markup=kb.get_main_menu(lang))

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
            TEXTS.get(lang, TEXTS['uz'])['main_menu_text'],
            reply_markup=kb.get_main_menu(lang)
        )
    except:
        # Fallback to default language
        await message.answer(
            TEXTS['uz']['main_menu_text'],
            reply_markup=kb.get_main_menu('uz')
        )
