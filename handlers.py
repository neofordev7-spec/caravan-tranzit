import random
import re
import json
import asyncio
import logging
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, InputMediaDocument
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from database import db
from states import (
    Registration, EPIKodFlow, MBDeklaratsiyaFlow, ApplicationsFlow,
    SettingsFlow, ContactInfoFlow, KGDFlow, BonusFlow, ChatFlow
)
import keyboards as kb
from strings import TEXTS

logger = logging.getLogger(__name__)
router = Router()
ADMIN_GROUP_ID = -1003463212374
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

# --- YORDAMCHI FUNKSIYALAR ---
async def get_text(state: FSMContext, key: str, **kwargs):
    data = await state.get_data()
    lang = data.get('lang', 'uz')
    return TEXTS.get(lang, TEXTS['uz']).get(key, "...").format(**kwargs)

async def get_user_lang(state: FSMContext):
    data = await state.get_data()
    return data.get('lang', 'uz')

# ==========================================================
# 1. RO'YXATDAN O'TISH (REGISTRATION)
# ==========================================================
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(TEXTS['uz']['start'], reply_markup=kb.get_lang_kb())
    await state.set_state(Registration.lang)

@router.callback_query(Registration.lang)
async def lang_chosen(call: CallbackQuery, state: FSMContext):
    lang = call.data.split("_")[1]
    await state.update_data(lang=lang)
    await call.message.delete()
    await call.message.answer(TEXTS[lang]['agreement'], reply_markup=kb.get_agreement_kb(lang))
    await state.set_state(Registration.agreement)

@router.callback_query(Registration.agreement)
async def agree(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await call.message.delete()
    await call.message.answer(TEXTS[data['lang']]['ask_phone'], reply_markup=kb.get_phone_kb(data['lang']))
    await state.set_state(Registration.phone)

@router.message(Registration.phone)
async def phone_received(message: Message, state: FSMContext):
    data = await state.get_data()
    ph = message.contact.phone_number if message.contact else message.text
    await db.add_user(message.from_user.id, message.from_user.full_name, ph, data['lang'])
    await message.answer("✅ Muvaffaqiyatli ro'yxatdan o'tdingiz!", reply_markup=kb.get_main_menu(data['lang']))
    await state.clear()
    await state.update_data(lang=data['lang'])

# ==========================================================
# 2. AT DEKLARATSIYA (EPI) FLOW ✅
# ==========================================================
@router.message(F.text.startswith("📄"))
async def start_at(message: Message, state: FSMContext):
    await state.clear()
    await state.update_data(lang='uz', app_type='AT')
    await message.answer("Kirish chegara postini tanlang:", reply_markup=kb.get_posts_kb())
    await state.set_state(EPIKodFlow.select_border_post)

@router.message(EPIKodFlow.select_border_post)
async def at_border(message: Message, state: FSMContext):
    if "ANIQ EMAS" in message.text:
        await message.answer("Viloyatni tanlang:", reply_markup=kb.get_viloyatlar_kb())
        await state.set_state(EPIKodFlow.select_viloyat_border)
        return
    await state.update_data(border_post=message.text)
    await message.answer("Manzil (TIF) bojxona postini tanlang:", reply_markup=kb.get_dest_posts_kb())
    await state.set_state(EPIKodFlow.select_dest_post)

@router.message(EPIKodFlow.select_dest_post)
async def at_dest(message: Message, state: FSMContext):
    await state.update_data(dest_post=message.text)
    await message.answer("Mashina raqamini yozing:", reply_markup=kb.get_cancel_kb())
    await state.set_state(EPIKodFlow.enter_car_number)

@router.message(EPIKodFlow.enter_car_number)
async def at_car(message: Message, state: FSMContext):
    await state.update_data(car_number=message.text.upper(), photos=[])
    await message.answer("Hujjatlarni yuboring (Rasm yoki PDF):", reply_markup=kb.get_done_kb())
    await state.set_state(EPIKodFlow.collect_docs)

# ==========================================================
# 3. MB DEKLARATSIYA FLOW (MAXSUS MANTIQ) ✅
# ==========================================================
@router.message(F.text.startswith("📋"))
async def start_mb(message: Message, state: FSMContext):
    await state.clear()
    await state.update_data(lang='uz', app_type='MB')
    await message.answer("Kirish chegara postini tanlang:", reply_markup=kb.get_posts_kb())
    await state.set_state(MBDeklaratsiyaFlow.select_border_post)

@router.message(MBDeklaratsiyaFlow.select_border_post)
async def mb_border(message: Message, state: FSMContext):
    if "ANIQ EMAS" in message.text:
        await message.answer("Viloyatni tanlang:", reply_markup=kb.get_viloyatlar_kb())
        await state.set_state(MBDeklaratsiyaFlow.select_viloyat_border)
        return
    await state.update_data(border_post=message.text)
    # MB uchun: Yo'q / Aniq emas / Chegara postlari tugmalari
    await message.answer("Manzil postini tanlang (MB uchun):", reply_markup=kb.get_mb_dest_posts_kb())
    await state.set_state(MBDeklaratsiyaFlow.select_dest_post)

@router.message(MBDeklaratsiyaFlow.select_dest_post)
async def mb_dest(message: Message, state: FSMContext):
    await state.update_data(dest_post=message.text)
    await message.answer("Mashina raqamini yozing:", reply_markup=kb.get_cancel_kb())
    await state.set_state(MBDeklaratsiyaFlow.enter_car_number)

@router.message(MBDeklaratsiyaFlow.enter_car_number)
async def mb_car(message: Message, state: FSMContext):
    await state.update_data(car_number=message.text.upper(), photos=[])
    await message.answer("Hujjatlarni yuboring (Rasm yoki PDF):", reply_markup=kb.get_done_kb())
    await state.set_state(MBDeklaratsiyaFlow.collect_docs)

# ==========================================================
# 4. HUJJATLARNI QABUL QILISH (SHARED) 📸
# ==========================================================
@router.message(EPIKodFlow.collect_docs, F.photo | F.document)
@router.message(MBDeklaratsiyaFlow.collect_docs, F.photo | F.document)
async def handle_docs(message: Message, state: FSMContext):
    data = await state.get_data()
    photos = data.get('photos', [])
    
    file_id = message.photo[-1].file_id if message.photo else message.document.file_id
    file_type = 'photo' if message.photo else 'document'
    
    photos.append({'file_id': file_id, 'type': file_type})
    await state.update_data(photos=photos)
    await message.reply(f"✅ {len(photos)}-fayl qabul qilindi!")

@router.message(EPIKodFlow.collect_docs, F.text.startswith("✅"))
@router.message(MBDeklaratsiyaFlow.collect_docs, F.text.startswith("✅"))
async def process_finish(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    if not data.get('photos'):
        await message.answer("⚠️ Kamida bitta rasm yuklang!")
        return

    atype = data['app_type']
    code = f"{atype}-{random.randint(10000, 99999)}"
    await db.create_application(code, message.from_user.id, atype, data['car_number'], data)
    
    # Admin xabari
    cap = f"🆕 **YANGI {atype} ARIZA!**\n🆔 `{code}`\n🚛 {data['car_number']}\n📍 {data['border_post']} -> {data['dest_post']}"
    await bot.send_message(ADMIN_GROUP_ID, cap, reply_markup=kb.get_admin_claim_kb(code))
    
    await message.answer(f"🚀 Ariza qabul qilindi! Kod: `{code}`", reply_markup=kb.get_main_menu())
    await state.clear()

# ==========================================================
# 5. GLOBAL HANDLERS (BACK/CANCEL)
# ==========================================================
@router.message(F.text.in_(["❌ Bekor qilish", "⬅️ Ortga"]))
async def global_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("🏠 Asosiy menyu", reply_markup=kb.get_main_menu())
