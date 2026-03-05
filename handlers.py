import random
import re
import json
import asyncio
import logging
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

logger = logging.getLogger(__name__)
router = Router()
SUPER_ADMIN_ID = 2027194005
ADMIN_GROUP_ID = -1003463212374
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

async def get_text(state: FSMContext, key: str, **kwargs):
    """Localized matnni olish"""
    data = await state.get_data()
    lang = data.get('lang', 'uz')
    return TEXTS.get(lang, TEXTS['uz']).get(key, "...").format(**kwargs)

async def get_user_lang(state: FSMContext):
    """Foydalanuvchi tilini aniqlash"""
    data = await state.get_data()
    return data.get('lang', 'uz')

# ==========================================================
# 1. START & REGISTRATION
# ==========================================================

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    referrer_id = None
    if message.text and len(message.text.split()) > 1:
        try:
            referrer_id = int(message.text.split()[1])
            if referrer_id != message.from_user.id:
                await state.update_data(referrer_id=referrer_id)
        except: pass

    await message.answer(TEXTS['uz']['start'], reply_markup=kb.get_lang_kb())
    await state.set_state(Registration.lang)

@router.callback_query(Registration.lang)
async def lang_chosen(call: CallbackQuery, state: FSMContext):
    lang = call.data.split("_")[1]
    await state.update_data(lang=lang)
    await call.message.delete()
    t = TEXTS.get(lang, TEXTS['uz'])['agreement']
    await call.message.answer(t, reply_markup=kb.get_agreement_kb(lang))
    await state.set_state(Registration.agreement)

@router.callback_query(Registration.agreement)
async def agreement_accepted(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    data = await state.get_data()
    t = await get_text(state, 'ask_phone')
    await call.message.answer(t, reply_markup=kb.get_phone_kb(data['lang']))
    await state.set_state(Registration.phone)

@router.message(Registration.phone)
async def phone_received(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get('lang', 'uz')
    referrer_id = data.get('referrer_id')
    ph = message.contact.phone_number if message.contact else message.text

    try:
        await db.add_user(message.from_user.id, message.from_user.full_name, ph, lang, 'IMPORT', referrer_id)
        if referrer_id:
            await db.create_referral(referrer_id, message.from_user.id)
            try:
                await message.bot.send_message(referrer_id, f"🎉 **Yangi do'st!** (+2,000 tanga)", parse_mode="Markdown")
            except: pass
    except Exception as e: logger.error(f"Add user error: {e}")

    t = await get_text(state, 'registered')
    await message.answer(t, reply_markup=kb.get_main_menu(lang))
    await state.clear()
    await state.update_data(lang=lang)

# ==========================================================
# 2. MB DEKLARATSIYA FLOW (MAXSUS MANTIQ) 🔥
# ==========================================================

@router.message(F.text.startswith("📋"))
async def start_mb_deklaratsiya(message: Message, state: FSMContext):
    """MB DEKLARATSIYA boshlanishi"""
    await state.clear()
    lang = (await db.get_user(message.from_user.id))['language'] if await db.get_user(message.from_user.id) else 'uz'
    await state.update_data(lang=lang, service_type='MB')

    t = await get_text(state, 'mb_start')
    await message.answer(t, reply_markup=kb.get_posts_kb()) # Chegara postlari
    await state.set_state(MBDeklaratsiyaFlow.select_border_post)

@router.message(MBDeklaratsiyaFlow.select_border_post)
async def mb_border_post_selected(message: Message, state: FSMContext):
    if message.text.startswith("⬅️"):
        await state.clear()
        await message.answer("🏠 Menu", reply_markup=kb.get_main_menu(await get_user_lang(state)))
        return

    if "ANIQ EMAS" in message.text:
        t = await get_text(state, 'select_viloyat')
        await message.answer(t, reply_markup=kb.get_viloyatlar_kb(), parse_mode="Markdown")
        await state.set_state(MBDeklaratsiyaFlow.select_viloyat_border)
        return

    await state.update_data(border_post=message.text)
    # MB uchun: Manzil postida YO'Q/ANIQ EMAS va Chegara postlari chiqadi
    t = await get_text(state, 'select_dest_post')
    await message.answer(t, reply_markup=kb.get_mb_dest_posts_kb()) 
    await state.set_state(MBDeklaratsiyaFlow.select_dest_post)

@router.message(MBDeklaratsiyaFlow.select_viloyat_border)
async def mb_viloyat_border_selected(message: Message, state: FSMContext):
    if message.text.startswith("⬅️"):
        await message.answer("Kirish postini tanlang:", reply_markup=kb.get_posts_kb())
        await state.set_state(MBDeklaratsiyaFlow.select_border_post)
        return
    await state.update_data(border_post=f"ANIQ EMAS ({message.text})")
    # MB uchun manzil posti tanlash
    t = await get_text(state, 'select_dest_post')
    await message.answer(t, reply_markup=kb.get_mb_dest_posts_kb())
    await state.set_state(MBDeklaratsiyaFlow.select_dest_post)

@router.message(MBDeklaratsiyaFlow.select_dest_post)
async def mb_dest_post_selected(message: Message, state: FSMContext):
    if message.text.startswith("⬅️"):
        await message.answer("Kirish postini tanlang:", reply_markup=kb.get_posts_kb())
        await state.set_state(MBDeklaratsiyaFlow.select_border_post)
        return

    if "ANIQ EMAS" in message.text and "YO'Q" not in message.text:
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
    if message.text.startswith("⬅️"):
        await message.answer("Manzil postini tanlang:", reply_markup=kb.get_mb_dest_posts_kb())
        await state.set_state(MBDeklaratsiyaFlow.select_dest_post)
        return
    await state.update_data(dest_post=f"ANIQ EMAS ({message.text})")
    t = await get_text(state, 'enter_car_number')
    await message.answer(t, reply_markup=kb.get_cancel_kb(await get_user_lang(state)))
    await state.set_state(MBDeklaratsiyaFlow.enter_car_number)

# (Qolgan barcha handlerlar: EPI Flow, Collect Docs, Admin Group va h.k. o'z o'rnida qoldi)
# ... [Bu yerda siz yuborgan faylning qolgan qismlari joylashadi]
