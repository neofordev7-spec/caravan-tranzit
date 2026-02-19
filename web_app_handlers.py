"""
WEB APP HANDLERS
Telegram Web App ma'lumotlarini qabul qilish va qayta ishlash
10 ta til qo'llab-quvvatlanadi
+ Mini App dan keyin hujjatlarni yig'ish
"""
import json
import random
from datetime import datetime
from aiogram import Router, F, Bot
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, InputMediaDocument
from aiogram.fsm.context import FSMContext
from database import db
from strings import TEXTS
from states import WebAppDocFlow
import keyboards as kb

router = Router()

# Admin guruh ID
ADMIN_GROUP_ID = -1003463212374

# Max fayl hajmi
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

# Til xaritasi
LANG_NAMES = {
    'uz': "O'zbekcha",
    'uz_cyrillic': 'Ўзбекча',
    'ru': 'Русский',
    'en': 'English',
    'zh': '中文',
    'tr': 'Türkçe',
    'kk': 'Қазақша',
    'ky': 'Кыргызча',
    'tj': 'Тоҷикӣ',
    'tk': 'Türkmençe'
}

# Ko'p tilli xabarlar
WEBAPP_TEXTS = {
    'uz': {
        'app_received': '✅ Ariza muvaffaqiyatli qabul qilindi!',
        'app_code': '🆔 Ariza kodi',
        'service': '📋 Xizmat',
        'post': '📍 Post',
        'destination': '🏁 Manzil',
        'vehicle': '🚛 Mashina',
        'agent': '👤 Agent',
        'wait_admin': '⏳ Admin javobini kuting...',
        'wait_time': 'Odatda 5-15 daqiqa',
        'notification': '🔔 Javob kelganda bildirishnoma olasiz',
        'error_user': '❌ Xatolik: Foydalanuvchi topilmadi. /start bosing.',
        'error_general': '❌ Xatolik yuz berdi. Qaytadan urinib ko\'ring.',
        'new_app': '🆕 YANGI ARIZA',
        'via_webapp': '(Mini App orqali)',
        'user': '👤 Foydalanuvchi',
        'username': '📱 Username',
        'telegram_id': '🔑 ID',
        'files_count': '📎 Fayllar',
        'language': '🌐 Til',
        'time': '⏰ Vaqt',
        'actions': '⚙️ Amallar',
        'set_price': '💰 Narx belgilash',
        'reject': '❌ Rad etish',
        'accept': '✅ Qabul qilish',
        'send_docs_prompt': (
            "📸 **Endi hujjatlaringizni shu yerga yuboring:**\n\n"
            "• Rasmlar (JPG, PNG)\n"
            "• PDF fayllar\n"
            "• Word, Excel fayllar\n\n"
            "Barcha hujjatlarni yuborganingizdan so'ng ✅ tugmasini bosing."
        ),
        'file_received': '✅ {count}-fayl qabul qilindi!',
        'file_too_big': '⚠️ Fayl juda katta (10MB dan ko\'p). Kichikroq fayl yuklang.',
        'min_one_file': '⚠️ Kamida 1 ta hujjat yuboring!',
        'app_sent_success': (
            "✅ **Ariza muvaffaqiyatli yuborildi!**\n\n"
            "🆔 Kod: `{code}`\n"
            "📎 Fayllar: {count} ta\n\n"
            "⏳ Admin javobini kuting..."
        ),
    },
    'ru': {
        'app_received': '✅ Заявка успешно принята!',
        'app_code': '🆔 Код заявки',
        'service': '📋 Услуга',
        'post': '📍 Пост',
        'destination': '🏁 Пункт назначения',
        'vehicle': '🚛 Транспорт',
        'agent': '👤 Агент',
        'wait_admin': '⏳ Ожидайте ответа администратора...',
        'wait_time': 'Обычно 5-15 минут',
        'notification': '🔔 Вы получите уведомление',
        'error_user': '❌ Ошибка: Пользователь не найден. Нажмите /start.',
        'error_general': '❌ Произошла ошибка. Попробуйте снова.',
        'new_app': '🆕 НОВАЯ ЗАЯВКА',
        'via_webapp': '(через Mini App)',
        'user': '👤 Пользователь',
        'username': '📱 Username',
        'telegram_id': '🔑 ID',
        'files_count': '📎 Файлы',
        'language': '🌐 Язык',
        'time': '⏰ Время',
        'actions': '⚙️ Действия',
        'set_price': '💰 Установить цену',
        'reject': '❌ Отклонить',
        'accept': '✅ Принять',
        'send_docs_prompt': (
            "📸 **Теперь отправьте ваши документы сюда:**\n\n"
            "• Фотографии (JPG, PNG)\n"
            "• PDF файлы\n"
            "• Word, Excel файлы\n\n"
            "После отправки всех документов нажмите ✅."
        ),
        'file_received': '✅ Файл {count} принят!',
        'file_too_big': '⚠️ Файл слишком большой (более 10МБ). Отправьте файл поменьше.',
        'min_one_file': '⚠️ Отправьте хотя бы 1 документ!',
        'app_sent_success': (
            "✅ **Заявка успешно отправлена!**\n\n"
            "🆔 Код: `{code}`\n"
            "📎 Файлы: {count} шт.\n\n"
            "⏳ Ожидайте ответа администратора..."
        ),
    },
    'en': {
        'app_received': '✅ Application received successfully!',
        'app_code': '🆔 Application Code',
        'service': '📋 Service',
        'post': '📍 Post',
        'destination': '🏁 Destination',
        'vehicle': '🚛 Vehicle',
        'agent': '👤 Agent',
        'wait_admin': '⏳ Waiting for admin response...',
        'wait_time': 'Usually 5-15 minutes',
        'notification': '🔔 You will receive a notification',
        'error_user': '❌ Error: User not found. Press /start.',
        'error_general': '❌ An error occurred. Please try again.',
        'new_app': '🆕 NEW APPLICATION',
        'via_webapp': '(via Mini App)',
        'user': '👤 User',
        'username': '📱 Username',
        'telegram_id': '🔑 ID',
        'files_count': '📎 Files',
        'language': '🌐 Language',
        'time': '⏰ Time',
        'actions': '⚙️ Actions',
        'set_price': '💰 Set Price',
        'reject': '❌ Reject',
        'accept': '✅ Accept',
        'send_docs_prompt': (
            "📸 **Now send your documents here:**\n\n"
            "• Photos (JPG, PNG)\n"
            "• PDF files\n"
            "• Word, Excel files\n\n"
            "After sending all documents, press ✅."
        ),
        'file_received': '✅ File {count} received!',
        'file_too_big': '⚠️ File too large (over 10MB). Send a smaller file.',
        'min_one_file': '⚠️ Send at least 1 document!',
        'app_sent_success': (
            "✅ **Application sent successfully!**\n\n"
            "🆔 Code: `{code}`\n"
            "📎 Files: {count}\n\n"
            "⏳ Waiting for admin response..."
        ),
    }
}

def get_webapp_text(lang: str, key: str) -> str:
    """Tilga mos matnni olish"""
    texts = WEBAPP_TEXTS.get(lang, WEBAPP_TEXTS.get('uz'))
    return texts.get(key, WEBAPP_TEXTS['uz'].get(key, key))


@router.message(F.web_app_data)
async def handle_web_app_data(message: Message, state: FSMContext, bot: Bot):
    """
    Web App dan kelgan ma'lumotlarni qayta ishlash
    """
    try:
        # Web App dan kelgan JSON ma'lumotlarni parse qilamiz
        data = json.loads(message.web_app_data.data)

        # Ma'lumot turini tekshiramiz
        data_type = data.get('type', 'application')

        if data_type == 'application':
            await handle_application_data(message, state, bot, data)
        elif data_type == 'chat_message':
            await handle_chat_message(message, bot, data)
        elif data_type == 'payment_selected':
            await handle_payment_selection(message, bot, data)
        else:
            print(f"Unknown data type: {data_type}")

    except json.JSONDecodeError:
        await message.answer("❌ Ma'lumotlarni o'qishda xatolik yuz berdi.")
    except Exception as e:
        print(f"Web App handler error: {e}")
        import traceback
        traceback.print_exc()
        await message.answer("❌ Xatolik yuz berdi. Qaytadan urinib ko'ring.")


async def handle_application_data(message: Message, state: FSMContext, bot: Bot, data: dict):
    """
    Ariza ma'lumotlarini qayta ishlash
    Mini App dan kelgan arizani saqlaydi va foydalanuvchidan hujjatlarni so'raydi
    """
    # Ma'lumotlarni olamiz
    app_code = data.get('code')
    service_type = data.get('service_type', 'EPI')
    border_post = data.get('border_post')
    destination = data.get('destination')
    vehicle_number = data.get('vehicle_number')
    vehicle_type = data.get('vehicle_type', 'truck')
    agent_id = data.get('agent_id')
    agent_name = data.get('agent_name')
    files_count = data.get('files_count', 0)
    lang = data.get('language', 'uz')

    # Foydalanuvchi ma'lumotlarini olamiz
    user = await db.get_user(message.from_user.id)
    if not user:
        # Yangi foydalanuvchi yaratamiz (add_user with required params)
        await db.add_user(
            telegram_id=message.from_user.id,
            full_name=message.from_user.full_name,
            phone='',
            lang=lang
        )
        user = await db.get_user(message.from_user.id)

    if not user:
        await message.answer(get_webapp_text(lang, 'error_user'))
        return

    # Agar ariza kodi yo'q bo'lsa generatsiya qilamiz
    if not app_code:
        prefix = service_type if service_type else 'APP'
        app_code = f"{prefix}-{datetime.now().year}-{random.randint(1000, 9999)}"

    # Arizani bazaga saqlaymiz (positional args matching db.create_application signature)
    metadata = {
        'service_type': service_type,
        'border_post': border_post,
        'destination': destination,
        'agent_name': agent_name,
        'agent_id': agent_id,
        'vehicle_type': vehicle_type,
        'files_count': files_count,
        'language': lang,
        'via_webapp': True,
        'status': 'new'
    }
    try:
        app_record = await db.create_application(
            app_code, message.from_user.id, service_type, vehicle_number or '', metadata
        )
    except Exception as e:
        print(f"Database error: {e}")
        import traceback
        traceback.print_exc()
        app_record = {'id': 0}

    # Foydalanuvchiga tasdiq va hujjat so'rash xabarini yuboramiz
    success_msg = f"""
{get_webapp_text(lang, 'app_received')}

{get_webapp_text(lang, 'app_code')}: `{app_code}`
{get_webapp_text(lang, 'service')}: {service_type}
{get_webapp_text(lang, 'post')}: {border_post}
{get_webapp_text(lang, 'destination')}: {destination}
{get_webapp_text(lang, 'vehicle')}: {vehicle_number}
"""

    await message.answer(
        success_msg,
        parse_mode="Markdown"
    )

    # Hujjatlarni so'raymiz - FSM state ga o'tkazamiz
    await state.update_data(
        webapp_app_code=app_code,
        webapp_data=data,
        webapp_app_id=app_record.get('id', 0) if isinstance(app_record, dict) else 0,
        photos=[],
        lang=lang
    )

    # Hujjat yuborishni so'raymiz
    await message.answer(
        get_webapp_text(lang, 'send_docs_prompt'),
        parse_mode="Markdown",
        reply_markup=kb.get_done_kb(lang)
    )
    await state.set_state(WebAppDocFlow.collect_docs)


# =========================================================================
# WEB APP DOCUMENT COLLECTION (Mini App dan keyin)
# =========================================================================

@router.message(WebAppDocFlow.collect_docs, F.photo | F.document)
async def webapp_doc_received(message: Message, state: FSMContext):
    """
    Mini App ariza yuborilgandan keyin hujjatlarni qabul qilish
    Rasmlar, PDF, Word, Excel va boshqa fayllarni qabul qiladi
    """
    data = await state.get_data()
    current_photos = data.get('photos', [])
    lang = data.get('lang', 'uz')

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
        await message.reply(get_webapp_text(lang, 'file_too_big'))
        return

    if file_id:
        current_photos.append({'file_id': file_id, 'type': file_type})
        await state.update_data(photos=current_photos)
        count = len(current_photos)
        await message.reply(get_webapp_text(lang, 'file_received').format(count=count))


@router.message(WebAppDocFlow.collect_docs, F.text)
async def webapp_docs_done(message: Message, state: FSMContext, bot: Bot):
    """
    Hujjatlarni yig'ish tugagach - admin guruhga yuborish
    """
    data = await state.get_data()
    lang = data.get('lang', 'uz')

    # Ortga yoki bekor qilish
    if message.text.startswith("⬅️") or message.text.startswith("❌"):
        await state.clear()
        await message.answer("🏠 Menu", reply_markup=kb.get_main_menu(lang))
        return

    # Yuklab bo'ldim tugmasi (✅ prefix)
    if message.text.startswith("✅"):
        photos = data.get('photos', [])

        if not photos:
            await message.answer(get_webapp_text(lang, 'min_one_file'))
            return

        # Admin guruhga yuborish
        app_code = data.get('webapp_app_code')
        webapp_data = data.get('webapp_data', {})

        admin_send_ok = await send_webapp_files_to_admin(bot, app_code, message.from_user, webapp_data, photos)

        if admin_send_ok:
            # Foydalanuvchiga tasdiqlash
            await message.answer(
                get_webapp_text(lang, 'app_sent_success').format(code=app_code, count=len(photos)),
                parse_mode="Markdown",
                reply_markup=kb.get_main_menu(lang)
            )
        else:
            # Xatolik haqida xabar berish
            await message.answer(
                f"⚠️ Ariza yuborishda xatolik yuz berdi. Iltimos qaytadan urinib ko'ring yoki admin bilan bog'laning: @CARAVAN_TRANZIT",
                reply_markup=kb.get_main_menu(lang)
            )

        await state.clear()
        await state.update_data(lang=lang)


# =========================================================================
# ADMIN GURUHGA YUBORISH (FAYLLAR BILAN)
# =========================================================================

def _escape_html(text: str) -> str:
    """Escape HTML special characters in user-provided text"""
    if not text:
        return ''
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


async def send_webapp_files_to_admin(bot: Bot, app_code: str, user, data: dict, files: list):
    """
    Admin guruhga ariza haqida to'liq xabar + fayllarni yuboradi
    """
    try:
        lang = data.get('language', 'uz')
        lang_name = LANG_NAMES.get(lang, "O'zbekcha")
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Fayllar sonini hisoblash
        photo_count = sum(1 for f in files if isinstance(f, dict) and f.get('type') == 'photo')
        doc_count = sum(1 for f in files if isinstance(f, dict) and f.get('type') == 'document')

        # Escape user-provided data to prevent parse errors (using HTML for safety)
        safe_name = _escape_html(user.full_name or '')
        safe_username = _escape_html(user.username or "yo'q")
        safe_post = _escape_html(data.get('border_post', '-') or '-')
        safe_dest = _escape_html(data.get('destination', '-') or '-')
        safe_vehicle = _escape_html(data.get('vehicle_number', '-') or '-')
        safe_agent = _escape_html(data.get('agent_name', '-') or '-')

        # Xabar matnini tayyorlaymiz (HTML format - safer with user data)
        msg_text = (
            f"🆕 <b>YANGI ARIZA</b> (Mini App orqali)\n\n"
            f"🆔 <b>Kod:</b> <code>{app_code}</code>\n\n"
            f"👤 <b>Foydalanuvchi:</b>\n"
            f"   Ism: {safe_name}\n"
            f"   Username: @{safe_username}\n"
            f"   ID: <code>{user.id}</code>\n"
            f"   Til: {lang_name}\n\n"
            f"📋 <b>Ariza:</b>\n"
            f"   Xizmat: {data.get('service_type', 'EPI')}\n"
            f"   Post: {safe_post}\n"
            f"   Manzil: {safe_dest}\n"
            f"   Mashina: {safe_vehicle}\n"
            f"   Agent: {safe_agent}\n"
            f"   Rasmlar: {photo_count} ta\n"
            f"   Hujjatlar: {doc_count} ta\n\n"
            f"⏰ <b>Vaqt:</b> {now}"
        )

        # Xabar matnini yuboramiz
        sent_msg = await bot.send_message(
            ADMIN_GROUP_ID,
            msg_text,
            parse_mode="HTML"
        )

        # Fayllarni ajratib yuboramiz
        photo_ids = []
        doc_ids = []
        for f in files:
            if isinstance(f, dict):
                if f.get('type') == 'document':
                    doc_ids.append(f['file_id'])
                else:
                    photo_ids.append(f['file_id'])

        # Rasmlarni yuboramiz
        if len(photo_ids) == 1:
            await bot.send_photo(ADMIN_GROUP_ID, photo_ids[0])
        elif len(photo_ids) > 1:
            for i in range(0, len(photo_ids), 10):
                chunk = photo_ids[i:i+10]
                media = [InputMediaPhoto(media=pid) for pid in chunk]
                await bot.send_media_group(ADMIN_GROUP_ID, media=media)

        # Hujjatlarni yuboramiz (PDF, Word, Excel va boshqalar)
        if len(doc_ids) == 1:
            await bot.send_document(ADMIN_GROUP_ID, doc_ids[0])
        elif len(doc_ids) > 1:
            for i in range(0, len(doc_ids), 10):
                chunk = doc_ids[i:i+10]
                media = [InputMediaDocument(media=did) for did in chunk]
                await bot.send_media_group(ADMIN_GROUP_ID, media=media)

        # Admin tugmalarini qo'shamiz
        admin_kb = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Qabul qilish",
                    callback_data=f"claim_{app_code}"
                ),
                InlineKeyboardButton(
                    text="💰 Narx belgilash",
                    callback_data=f"setprice_{app_code}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Rad etish",
                    callback_data=f"reject_{app_code}"
                ),
                InlineKeyboardButton(
                    text="💬 Xabar yuborish",
                    callback_data=f"message_{user.id}"
                )
            ]
        ])

        await bot.send_message(
            ADMIN_GROUP_ID,
            f"⚙️ <code>{app_code}</code> - Amallar:",
            reply_markup=admin_kb,
            parse_mode="HTML"
        )

        # Message ID ni bazaga saqlaymiz
        try:
            await db.update_admin_message_id(app_code, sent_msg.message_id)
        except:
            pass

        print(f"✅ Admin guruhga fayllar bilan yuborildi: {app_code} ({len(photo_ids)} rasm, {len(doc_ids)} hujjat)")
        return True

    except Exception as e:
        print(f"❌ Admin guruhga yuborishda xatolik: {e}")
        import traceback
        traceback.print_exc()
        return False


async def handle_chat_message(message: Message, bot: Bot, data: dict):
    """
    Chat xabarini qayta ishlash
    """
    chat_message = data.get('message', '')

    if not chat_message:
        return

    # Admin guruhga forward qilamiz
    try:
        admin_msg = f"""
💬 **YANGI XABAR (Mini App)**

👤 Foydalanuvchi: {message.from_user.full_name}
📱 Username: @{message.from_user.username or "yo'q"}
🔑 ID: `{message.from_user.id}`

💬 Xabar:
{chat_message}
"""

        reply_kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="↩️ Javob berish",
                callback_data=f"reply_{message.from_user.id}"
            )]
        ])

        await bot.send_message(
            ADMIN_GROUP_ID,
            admin_msg,
            parse_mode="Markdown",
            reply_markup=reply_kb
        )

    except Exception as e:
        print(f"Error forwarding chat message: {e}")


async def handle_payment_selection(message: Message, bot: Bot, data: dict):
    """
    To'lov tanlashni qayta ishlash
    """
    payment_method = data.get('method', '')

    # Admin guruhga xabar yuboramiz
    try:
        await bot.send_message(
            ADMIN_GROUP_ID,
            f"💳 **TO'LOV TANLANDI**\n\n"
            f"👤 Foydalanuvchi: {message.from_user.full_name}\n"
            f"🔑 ID: `{message.from_user.id}`\n"
            f"💳 Usul: {payment_method.upper()}",
            parse_mode="Markdown"
        )
    except Exception as e:
        print(f"Error notifying payment selection: {e}")


# =========================================================================
# BALANCE CHECKER
# =========================================================================

@router.message(F.text.contains("Balans") | F.text.contains("Balance") | F.text.contains("💰") | F.text.contains("Tangalarim"))
async def show_balance(message: Message):
    """
    Foydalanuvchi balansini ko'rsatadi
    """
    user = await db.get_user(message.from_user.id)
    if not user:
        await message.answer("❌ /start bosing.")
        return

    balance = user.get('balance', 0)
    lang = user.get('language', 'uz')

    # 35,000 coins = 1 free service
    free_services = int(balance / 35000)

    # Ko'p tilli matn
    if lang == 'ru':
        msg = f"""
💰 **Ваш баланс:**

🪙 Монеты: **{balance:,.0f}**
🎁 Бесплатные услуги: **{free_services}**

📊 **Как заработать монеты:**
• 35,000 монет = 1 бесплатная декларация
• Пригласите друзей: +2,000 монет
• Друг использует услугу: +17,500 монет

🔗 **Ваша реферальная ссылка:**
https://t.me/CARAVAN_TRANZIT_BOT?start={message.from_user.id}
"""
    elif lang == 'en':
        msg = f"""
💰 **Your Balance:**

🪙 Coins: **{balance:,.0f}**
🎁 Free services: **{free_services}**

📊 **How to earn coins:**
• 35,000 coins = 1 free declaration
• Invite friends: +2,000 coins
• Friend uses service: +17,500 coins

🔗 **Your referral link:**
https://t.me/CARAVAN_TRANZIT_BOT?start={message.from_user.id}
"""
    else:
        msg = f"""
💰 **Sizning balansingiz:**

🪙 Tangalar: **{balance:,.0f}**
🎁 Bepul xizmatlar: **{free_services}**

📊 **Tanga ishlating:**
• 35,000 tanga = 1 bepul deklaratsiya
• Do'stlarni taklif qiling: +2,000 tanga
• Do'stingiz xizmatdan foydalansa: +17,500 tanga

🔗 **Taklif havolangiz:**
https://t.me/CARAVAN_TRANZIT_BOT?start={message.from_user.id}
"""

    await message.answer(msg, parse_mode="Markdown")
