import random
import re
import json
import asyncio
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, ReplyKeyboardRemove
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from database import db
from states import Registration, ApplicationWorkflow, AdminState, SupportState
import keyboards as kb
from strings import TEXTS

router = Router()
SUPER_ADMIN_ID = 2027194005
ADMIN_GROUP_ID = -1003463212374
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB limit (Hujjatlar uchun yetarli)

async def get_text(state: FSMContext, key: str, **kwargs):
    data = await state.get_data()
    lang = data.get('lang', 'uz')
    return TEXTS.get(lang, TEXTS['uz']).get(key, "...").format(**kwargs)

# ==========================================================
# 1. START & REGISTRATION
# ==========================================================
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()

    # Referral linkni tekshiramiz: /start 123456789
    referrer_id = None
    if message.text and len(message.text.split()) > 1:
        try:
            referrer_id = int(message.text.split()[1])
            # O'zini taklif qila olmaydi
            if referrer_id == message.from_user.id:
                referrer_id = None
            else:
                await state.update_data(referrer_id=referrer_id)
        except:
            pass

    await message.answer(TEXTS['uz']['start'], reply_markup=kb.get_lang_kb())
    await state.set_state(Registration.lang)

# GLOBAL BEKOR QILISH
@router.message(F.text.in_(["❌", "⬅️ Ortga", "⬅️ Назад", "⬅️ Back", "❌ Bekor qilish", "❌ Cancel", "⬅️ Орқага", "❌ Бекор қилиш", "⬅️ 返回", "❌ Бас тарту"]))
async def cancel_process(message: Message, state: FSMContext):
    await state.clear()
    data = await state.get_data()
    lang = data.get('lang', 'uz')
    await message.answer("🏠 Menu", reply_markup=kb.get_main_menu(lang))

@router.callback_query(Registration.lang)
async def lang_cho(call: CallbackQuery, state: FSMContext):
    lang = call.data.split("_")[1]
    await state.update_data(lang=lang)
    await call.message.delete()
    t = TEXTS.get(lang, TEXTS['uz'])['agreement']
    await call.message.answer(t, reply_markup=kb.get_agreement_kb(lang))
    await state.set_state(Registration.agreement)

@router.callback_query(Registration.agreement)
async def agree(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    data = await state.get_data()
    t = await get_text(state, 'ask_phone')
    await call.message.answer(t, reply_markup=kb.get_phone_kb(data['lang']))
    await state.set_state(Registration.phone)

@router.message(Registration.phone)
async def phone_h(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get('lang', 'uz')
    referrer_id = data.get('referrer_id')

    ph = message.contact.phone_number if message.contact else message.text

    try:
        # Foydalanuvchini qo'shamiz (referral bilan)
        await db.add_user(message.from_user.id, message.from_user.full_name, ph, lang, referrer_id)

        # Agar referral bo'lsa, referrallarni ham saqlaymiz
        if referrer_id:
            success = await db.create_referral(referrer_id, message.from_user.id)
            if success:
                # Referrer ga xabar yuboramiz
                try:
                    from aiogram import Bot
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

    t = await get_text(state, 'registered')
    await message.answer(t, reply_markup=kb.get_main_menu(lang))
    await state.clear()
    await state.update_data(lang=lang)

# ==========================================================
# 2. ARIZA JARAYONI (AT / MB) - CRASH TUZATILDI ✅
# ==========================================================
# MUHIM: F.text qo'shildi. Endi rasm kelsa bu yerga kirmaydi va crash bo'lmaydi.
@router.message(F.text, F.text.func(lambda text: ("AT" in text.upper() or "MB" in text.upper() or "АТ" in text.upper() or "МБ" in text.upper()) and "ALOQA" not in text.upper()))
async def start_app(message: Message, state: FSMContext):
    atype = "MB" if ("MB" in message.text.upper() or "МБ" in message.text.upper()) else "AT"
    await state.update_data(app_type=atype, photos=[])
    
    t = await get_text(state, 'enter_car')
    data = await state.get_data()
    await message.answer(f"{atype}: {t}", reply_markup=kb.get_step_control(data.get('lang', 'uz')))
    await state.set_state(ApplicationWorkflow.car_number)

@router.message(ApplicationWorkflow.car_number)
async def car_step(message: Message, state: FSMContext):
    # Agar rasm tashlab yuborsa, ogohlantiramiz
    if not message.text:
        await message.reply("⚠️ Iltimos, mashina raqamini yozing (Rasm emas).")
        return

    car = message.text.replace(" ", "").upper()
    await state.update_data(car_number=car)
    
    saved = await db.get_saved_docs(message.from_user.id, car)
    if saved:
        await state.update_data(temp_saved=saved)
        t = await get_text(state, 'autofill_found', car=car)
        data = await state.get_data()
        await message.answer(t, reply_markup=kb.get_autofill_kb(data['lang']))
        await state.set_state(ApplicationWorkflow.collect_docs)
    else:
        await ask_docs(message, state)

async def ask_docs(message: Message, state: FSMContext, is_auto=False):
    data = await state.get_data()
    lang = data.get('lang', 'uz')
    atype = data.get('app_type', 'AT')
    
    docs_key = 'docs_list_at' if atype == 'AT' else 'docs_list_mb'
    docs_text = TEXTS.get(lang, TEXTS['uz'])[docs_key]
    
    if is_auto:
        msg = TEXTS.get(lang, TEXTS['uz'])['autofill_used']
    else:
        h = TEXTS.get(lang, TEXTS['uz'])['docs_header']
        f = TEXTS.get(lang, TEXTS['uz'])['docs_footer']
        msg = f"{h}\n\n{docs_text}\n{f}"
        
    await message.answer(msg, reply_markup=kb.get_done_kb(lang))
    await state.set_state(ApplicationWorkflow.collect_docs)

# --- RASM QABUL QILISH (ALOHIDA HANDLER) 🔥 ---
# Bu handler faqat rasm yoki fayl kelsa ishlaydi
@router.message(ApplicationWorkflow.collect_docs, F.photo | F.document)
async def on_photo_sent(message: Message, state: FSMContext):
    data = await state.get_data()
    current_photos = data.get('photos', [])
    
    file_id = None
    file_size = 0
    
    if message.photo:
        file_id = message.photo[-1].file_id 
        file_size = message.photo[-1].file_size
    elif message.document:
        # Hujjat bo'lsa ham rasm ekanligini tekshiramiz (yoki PDF)
        file_id = message.document.file_id
        file_size = message.document.file_size

    # LIMIT (10 MB)
    if file_size > MAX_FILE_SIZE:
        await message.reply("⚠️ Fayl juda katta (10MB dan ko'p). Kichikroq rasm yuklang.")
        return

    if file_id:
        current_photos.append(file_id)
        await state.update_data(photos=current_photos)
        # Rasmni jim qabul qilamiz (Spam bo'lmasligi uchun)

# --- TUGMALARNI QABUL QILISH (ALOHIDA HANDLER) ---
@router.message(ApplicationWorkflow.collect_docs, F.text)
async def on_text_sent(message: Message, state: FSMContext):
    data = await state.get_data()
    
    # Auto-fill
    if any(x in message.text for x in ["✅ Ha", "✅ Да", "✅ Yes", "✅ Иә", "✅ Ҳа"]):
        saved = data.get('temp_saved', [])
        await state.update_data(photos=saved)
        await ask_docs(message, state, is_auto=True)
        return
        
    if any(x in message.text for x in ["🔄", "Yo'q", "Нет", "No", "Жоқ", "Йўқ"]):
        await state.update_data(photos=[])
        await ask_docs(message, state, is_auto=False)
        return
        
    # "YUKLAB BO'LDIM" (Barcha tillarda)
    # Turkiy tillar va boshqalar uchun kalit so'zlar
    keywords = ["Yuklab", "Загрузил", "Done", "Болды", "Юклаб", "Тайёр", "Boldu", "完成", "Tamam", "Бүттүм"]
    
    if any(k.lower() in message.text.lower() for k in keywords):
        if not data.get('photos') or len(data.get('photos', [])) == 0:
            t = await get_text(state, 'zero_photos')
            await message.answer(t)
            return
            
        t = await get_text(state, 'select_post')
        await message.answer(t, reply_markup=kb.get_posts_kb())
        await state.set_state(ApplicationWorkflow.select_post)
        return
    
    # Agar boshqa so'z yozsa
    await message.reply("⚠️ Iltimos, rasm yuklang yoki 'Yuklab bo'ldim' tugmasini bosing.")

@router.message(ApplicationWorkflow.select_post)
async def post_s(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(post=message.text)
    data = await state.get_data()
    if data['app_type'] == 'AT':
        t = await get_text(state, 'select_dest_post')
        await message.answer(t, reply_markup=kb.get_dest_posts_kb())
        await state.set_state(ApplicationWorkflow.select_dest_post)
    else:
        await finish(message, state, bot)

@router.message(ApplicationWorkflow.select_dest_post)
async def dest_s(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(dest_post=message.text)
    await finish(message, state, bot)

async def finish(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    atype = data.get('app_type', 'AT')
    car = data['car_number']
    code = f"{atype}-{random.randint(10000, 99999)}"
    
    try: await db.save_car_docs(message.from_user.id, car, data.get('photos', []))
    except: pass
    await db.create_application(code, message.from_user.id, atype, car, data)
    
    t = await get_text(state, 'finish', code=code, count=len(data.get('photos', [])))
    await message.answer(t, reply_markup=kb.get_main_menu(data.get('lang', 'uz')))
    
    # Admin Broadcast (Albom qilib yuborish)
    try:
        route = f"📍: {data.get('post')}"
        if atype == 'AT': route += f" -> {data.get('dest_post')}"
        cap = f"🆕 **YANGI {atype} ARIZA!**\n🆔: `{code}`\n🚛: {car}\n👤: {message.from_user.full_name}\n{route}"
        
        photos = data.get('photos', [])
        chunked = [photos[i:i+10] for i in range(0, len(photos), 10)]
        
        for chunk in chunked:
            media = []
            for idx, pid in enumerate(chunk):
                # Faqat birinchi rasmga caption qo'shamiz
                caption = cap if (idx == 0 and chunk == chunked[0]) else None
                media.append(InputMediaPhoto(media=pid, caption=caption, parse_mode="Markdown"))
            
            await bot.send_media_group(ADMIN_GROUP_ID, media=media)
            
        await bot.send_message(ADMIN_GROUP_ID, f"🆔 `{code}` boshqarish:", reply_markup=kb.get_admin_claim_kb(code))
    except Exception as e: 
        print(f"Admin send error: {e}")
        # Agar rasm bilan muammo bo'lsa, kamida tekst boradi
        await bot.send_message(ADMIN_GROUP_ID, f"🆕 Ariza: {code} (Rasmlarni yuklashda xatolik: {e})")
        
    await state.clear()
    await state.update_data(lang=data.get('lang', 'uz'))

# ==========================================================
# 3. ADMIN & TO'LOV
# ==========================================================
@router.callback_query(F.data.startswith("claim_"))
async def claim(call: CallbackQuery, bot: Bot):
    code = call.data.split("_")[1]
    if await db.claim_application(code, call.from_user.id):
        await call.message.edit_text(f"✅ Qabul qilindi: {call.from_user.full_name}\n🆔 `{code}`")
        try: await bot.send_message(call.from_user.id, f"Arizani oldingiz: {code}", reply_markup=kb.get_pricing_kb(code))
        except: await call.answer("Botga start bosing!", show_alert=True)
    else: await call.answer("Band!", show_alert=True)

@router.callback_query(F.data.startswith("setprice_"))
async def price(call: CallbackQuery, bot: Bot):
    try:
        amt, code = call.data.split("_")[1], call.data.split("_")[2]
        app = await db.get_app_by_code(code)
        if app:
            await bot.send_message(app['user_id'], f"✅ Tasdiqlandi\n💰 To'lov: {amt}", reply_markup=kb.get_user_payment_methods(code, amt))
            await call.message.edit_text(f"✅ Yuborildi: {amt}")
            await db.update_status(code, f"Pay: {amt}")
    except: pass
    await call.answer()

@router.callback_query(F.data == "cancel_pay")
async def cancel_p(call: CallbackQuery):
    await call.message.delete()

# --- SUPPORT (FIXED) ---
@router.message(F.text.func(lambda text: "Aloqa" in text or "Support" in text or "Связь" in text or "Админ" in text))
async def enter_support(message: Message, state: FSMContext):
    t = await get_text(state, 'support_ask')
    data = await state.get_data()
    await message.answer(t, reply_markup=kb.get_step_control(data.get('lang', 'uz')))
    await state.set_state(SupportState.waiting_for_question)

@router.message(SupportState.waiting_for_question)
async def send_support(message: Message, state: FSMContext, bot: Bot):
    if message.text in ["⬅️ Ortga", "⬅️ Назад", "❌", "⬅️ Back", "❌ Bekor qilish"]:
        await cancel_process(message, state)
        return
    msg = f"📩 **SAVOL (SUPPORT)!**\n👤: {message.from_user.full_name}\n🆔: `{message.from_user.id}`\n📝: {message.text}"
    await bot.send_message(ADMIN_GROUP_ID, msg)
    t = await get_text(state, 'support_sent')
    await message.answer(t)
    await cancel_process(message, state)

# --- ADMIN GROUP HANDLER ---
@router.message(F.chat.id == ADMIN_GROUP_ID)
async def admin_handler(message: Message, bot: Bot):
    if message.reply_to_message:
        orig = message.reply_to_message.text or ""
        match = re.search(r"(?:ID|🆔):\s*`?(\d+)`?", orig)
        if match:
            try: await bot.send_message(int(match.group(1)), f"👮‍♂️ **Admin:**\n{message.text}")
            except: pass
    
    # Broadcast
    txt = (message.text or "").upper()
    car_m = re.search(r"(\d{2}[A-Z]\d{3}[A-Z]{2})|(\d{5}[A-Z]{3})", txt)
    if car_m:
        app = await db.get_app_by_car_number(car_m.group(0))
        if app: await bot.send_message(app['user_id'], f"🔔 Admin: {message.text}")

# --- MENYU & SOZLAMALAR ---
@router.message(F.text.contains("Sozlamalar") | F.text.contains("Settings") | F.text.contains("Настройки") | F.text.contains("Баптаулар"))
async def settings(message: Message, state: FSMContext):
    t = await get_text(state, 'settings_title')
    data = await state.get_data()
    await message.answer(t, reply_markup=kb.get_settings_kb(data.get('lang', 'uz')))

@router.message(F.text.contains("Til") | F.text.contains("Language"))
async def ch_lang(message: Message, state: FSMContext):
    await message.answer("Til:", reply_markup=kb.get_lang_kb())

@router.message(F.text.contains("Arizalar") | F.text.contains("Apps"))
async def my_apps(message: Message, state: FSMContext):
    apps = await db.get_user_apps(message.from_user.id)
    if not apps:
        t = await get_text(state, 'my_apps_empty')
        await message.answer(t)
    else:
        msg = "📂 **Arizalar:**\n"
        for a in apps: msg += f"🔹 `{a['app_code']}`: {a['status']}\n"
        await message.answer(msg, parse_mode="Markdown")

@router.message(F.text.contains("Tozalash"))
async def clr_cache(message: Message, state: FSMContext):
    await db.clear_user_cache(message.from_user.id)
    await state.clear()
    t = await get_text(state, 'cache_cleared')
    data = await state.get_data()
    await message.answer(t)
    await message.answer("🏠 Menu", reply_markup=kb.get_main_menu(data.get('lang', 'uz')))
