"""
WEB APP HANDLERS
Telegram Web App ma'lumotlarini qabul qilish va qayta ishlash
10 ta til qo'llab-quvvatlanadi
"""
import json
import random
from datetime import datetime
from aiogram import Router, F, Bot
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database import db
from strings import TEXTS
import keyboards as kb

router = Router()

# Admin guruh ID
ADMIN_GROUP_ID = -1003463212374

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
        'accept': '✅ Qabul qilish'
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
        'accept': '✅ Принять'
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
        'accept': '✅ Accept'
    },
    'oz': {
        'app_received': '✅ Ариза муваффақиятли қабул қилинди!',
        'app_code': '🆔 Ариза коди',
        'service': '📋 Хизмат',
        'post': '📍 Пост',
        'destination': '🏁 Манзил',
        'vehicle': '🚛 Машина',
        'agent': '👤 Агент',
        'wait_admin': '⏳ Админ жавобини кутинг...',
        'wait_time': 'Одатда 5-15 дақиқа',
        'notification': '🔔 Жавоб келганда билдиришнома оласиз',
        'error_user': '❌ Хатолик: Фойдаланувчи топилмади. /start босинг.',
        'error_general': '❌ Хатолик юз берди. Қайтадан уриниб кўринг.',
        'new_app': '🆕 ЯНГИ АРИЗА',
        'via_webapp': '(Mini App орқали)',
        'user': '👤 Фойдаланувчи',
        'username': '📱 Username',
        'telegram_id': '🔑 ID',
        'files_count': '📎 Файллар',
        'language': '🌐 Тил',
        'time': '⏰ Вақт',
        'actions': '⚙️ Амаллар',
        'set_price': '💰 Нарх белгилаш',
        'reject': '❌ Рад этиш',
        'accept': '✅ Қабул қилиш'
    },
    'kz': {
        'app_received': '✅ Өтініш сәтті қабылданды!',
        'app_code': '🆔 Өтініш коды',
        'service': '📋 Қызмет',
        'post': '📍 Пост',
        'destination': '🏁 Бағыт',
        'vehicle': '🚛 Көлік',
        'agent': '👤 Агент',
        'wait_admin': '⏳ Админ жауабын күтіңіз...',
        'wait_time': 'Әдетте 5-15 минут',
        'notification': '🔔 Жауап келгенде хабарлама аласыз',
        'error_user': '❌ Қате: Пайдаланушы табылмады. /start басыңыз.',
        'error_general': '❌ Қате пайда болды. Қайта көріңіз.',
        'new_app': '🆕 ЖАҢА ӨТІНІШ',
        'via_webapp': '(Mini App арқылы)',
        'user': '👤 Пайдаланушы',
        'username': '📱 Username',
        'telegram_id': '🔑 ID',
        'files_count': '📎 Файлдар',
        'language': '🌐 Тіл',
        'time': '⏰ Уақыт',
        'actions': '⚙️ Әрекеттер',
        'set_price': '💰 Бағаны белгілеу',
        'reject': '❌ Қабылдамау',
        'accept': '✅ Қабылдау'
    },
    'kg': {
        'app_received': '✅ Арыз ийгиликтүү кабыл алынды!',
        'app_code': '🆔 Арыз коду',
        'service': '📋 Кызмат',
        'post': '📍 Пост',
        'destination': '🏁 Багыт',
        'vehicle': '🚛 Унаа',
        'agent': '👤 Агент',
        'wait_admin': '⏳ Админ жоопту күтүңүз...',
        'wait_time': 'Адатта 5-15 мүнөт',
        'notification': '🔔 Жооп келгенде билдирүү аласыз',
        'error_user': '❌ Ката: Колдонуучу табылган жок. /start басыңыз.',
        'error_general': '❌ Ката кетти. Кайра аракет кылыңыз.',
        'new_app': '🆕 ЖАҢЫ АРЫЗ',
        'via_webapp': '(Mini App аркылуу)',
        'user': '👤 Колдонуучу',
        'username': '📱 Username',
        'telegram_id': '🔑 ID',
        'files_count': '📎 Файлдар',
        'language': '🌐 Тил',
        'time': '⏰ Убакыт',
        'actions': '⚙️ Аракеттер',
        'set_price': '💰 Баа коюу',
        'reject': '❌ Четке кагуу',
        'accept': '✅ Кабыл алуу'
    },
    'tj': {
        'app_received': '✅ Ариза бо муваффақият қабул шуд!',
        'app_code': '🆔 Коди ариза',
        'service': '📋 Хизмат',
        'post': '📍 Пост',
        'destination': '🏁 Самт',
        'vehicle': '🚛 Мошин',
        'agent': '👤 Агент',
        'wait_admin': '⏳ Ҷавоби админро интизор шавед...',
        'wait_time': 'Одатан 5-15 дақиқа',
        'notification': '🔔 Вақте ки ҷавоб ояд, хабарнома мегиред',
        'error_user': '❌ Хатогӣ: Истифодабаранда ёфт нашуд. /start пахш кунед.',
        'error_general': '❌ Хатогӣ рух дод. Дубора кӯшиш кунед.',
        'new_app': '🆕 АРИЗАИ НАВ',
        'via_webapp': '(Mini App тавассути)',
        'user': '👤 Истифодабаранда',
        'username': '📱 Username',
        'telegram_id': '🔑 ID',
        'files_count': '📎 Файлҳо',
        'language': '🌐 Забон',
        'time': '⏰ Вақт',
        'actions': '⚙️ Амалҳо',
        'set_price': '💰 Нарх муқаррар кардан',
        'reject': '❌ Рад кардан',
        'accept': '✅ Қабул кардан'
    },
    'tr': {
        'app_received': '✅ Başvuru başarıyla alındı!',
        'app_code': '🆔 Başvuru Kodu',
        'service': '📋 Hizmet',
        'post': '📍 Gümrük',
        'destination': '🏁 Varış',
        'vehicle': '🚛 Araç',
        'agent': '👤 Temsilci',
        'wait_admin': '⏳ Yönetici yanıtı bekleniyor...',
        'wait_time': 'Genellikle 5-15 dakika',
        'notification': '🔔 Yanıt geldiğinde bildirim alacaksınız',
        'error_user': '❌ Hata: Kullanıcı bulunamadı. /start basın.',
        'error_general': '❌ Bir hata oluştu. Tekrar deneyin.',
        'new_app': '🆕 YENİ BAŞVURU',
        'via_webapp': '(Mini App ile)',
        'user': '👤 Kullanıcı',
        'username': '📱 Username',
        'telegram_id': '🔑 ID',
        'files_count': '📎 Dosyalar',
        'language': '🌐 Dil',
        'time': '⏰ Zaman',
        'actions': '⚙️ İşlemler',
        'set_price': '💰 Fiyat Belirle',
        'reject': '❌ Reddet',
        'accept': '✅ Kabul Et'
    },
    'tm': {
        'app_received': '✅ Arza üstünlikli kabul edildi!',
        'app_code': '🆔 Arza kody',
        'service': '📋 Hyzmat',
        'post': '📍 Post',
        'destination': '🏁 Baryş',
        'vehicle': '🚛 Ulag',
        'agent': '👤 Agent',
        'wait_admin': '⏳ Admin jogabyna garaşyň...',
        'wait_time': 'Adatça 5-15 minut',
        'notification': '🔔 Jogap gelende habar alarsyňyz',
        'error_user': '❌ Ýalňyşlyk: Ulanyjy tapylmady. /start basyň.',
        'error_general': '❌ Ýalňyşlyk ýüze çykdy. Gaýtadan synanyşyň.',
        'new_app': '🆕 TÄZE ARZA',
        'via_webapp': '(Mini App arkaly)',
        'user': '👤 Ulanyjy',
        'username': '📱 Username',
        'telegram_id': '🔑 ID',
        'files_count': '📎 Faýllar',
        'language': '🌐 Dil',
        'time': '⏰ Wagt',
        'actions': '⚙️ Amallar',
        'set_price': '💰 Bahany bellemek',
        'reject': '❌ Ret etmek',
        'accept': '✅ Kabul etmek'
    },
    'zh': {
        'app_received': '✅ 申请已成功接收！',
        'app_code': '🆔 申请代码',
        'service': '📋 服务',
        'post': '📍 口岸',
        'destination': '🏁 目的地',
        'vehicle': '🚛 车辆',
        'agent': '👤 代理',
        'wait_admin': '⏳ 等待管理员回复...',
        'wait_time': '通常5-15分钟',
        'notification': '🔔 收到回复时您将收到通知',
        'error_user': '❌ 错误：未找到用户。请按 /start。',
        'error_general': '❌ 发生错误。请重试。',
        'new_app': '🆕 新申请',
        'via_webapp': '(通过Mini App)',
        'user': '👤 用户',
        'username': '📱 用户名',
        'telegram_id': '🔑 ID',
        'files_count': '📎 文件',
        'language': '🌐 语言',
        'time': '⏰ 时间',
        'actions': '⚙️ 操作',
        'set_price': '💰 设定价格',
        'reject': '❌ 拒绝',
        'accept': '✅ 接受'
    }
}

def get_webapp_text(lang: str, key: str) -> str:
    """Tilga mos matnni olish"""
    # Map alternative language codes
    lang_map = {'uz_cyrillic': 'oz', 'kk': 'kz', 'ky': 'kg', 'tk': 'tm'}
    lang = lang_map.get(lang, lang)
    texts = WEBAPP_TEXTS.get(lang, WEBAPP_TEXTS.get('uz'))
    return texts.get(key, WEBAPP_TEXTS['uz'].get(key, key))


@router.message(F.web_app_data)
async def handle_web_app_data(message: Message, bot: Bot):
    """
    Web App dan kelgan ma'lumotlarni qayta ishlash
    """
    try:
        # Web App dan kelgan JSON ma'lumotlarni parse qilamiz
        data = json.loads(message.web_app_data.data)

        # Ma'lumot turini tekshiramiz
        data_type = data.get('type', 'application')

        if data_type == 'application':
            await handle_application_data(message, bot, data)
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
        await message.answer("❌ Xatolik yuz berdi. Qaytadan urinib ko'ring.")


async def handle_application_data(message: Message, bot: Bot, data: dict):
    """
    Ariza ma'lumotlarini qayta ishlash
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
        # Yangi foydalanuvchi yaratamiz
        await db.create_user(
            telegram_id=message.from_user.id,
            full_name=message.from_user.full_name,
            language=lang
        )
        user = await db.get_user(message.from_user.id)

    if not user:
        await message.answer(get_webapp_text(lang, 'error_user'))
        return

    # Agar ariza kodi yo'q bo'lsa generatsiya qilamiz
    if not app_code:
        prefix = service_type if service_type else 'APP'
        app_code = f"{prefix}-{datetime.now().year}-{random.randint(1000, 9999)}"

    # Arizani bazaga saqlaymiz
    try:
        app_record = await db.create_application(
            app_code=app_code,
            user_id=message.from_user.id,
            agent_id=agent_id,
            post_id=None,  # Postni nomdan topamiz
            vehicle_number=vehicle_number,
            vehicle_type=vehicle_type,
            files={},
            metadata={
                'service_type': service_type,
                'border_post': border_post,
                'destination': destination,
                'agent_name': agent_name,
                'files_count': files_count,
                'language': lang,
                'via_webapp': True,
                'status': 'new'
            }
        )
    except Exception as e:
        print(f"Database error: {e}")
        app_record = {'id': 0}

    # Foydalanuvchiga tasdiq xabarini yuboramiz
    success_msg = f"""
{get_webapp_text(lang, 'app_received')}

{get_webapp_text(lang, 'app_code')}: `{app_code}`
{get_webapp_text(lang, 'service')}: {service_type}
{get_webapp_text(lang, 'post')}: {border_post}
{get_webapp_text(lang, 'destination')}: {destination}
{get_webapp_text(lang, 'vehicle')}: {vehicle_number}
{get_webapp_text(lang, 'agent')}: {agent_name}

{get_webapp_text(lang, 'wait_admin')}
💡 {get_webapp_text(lang, 'wait_time')}
{get_webapp_text(lang, 'notification')}
"""

    await message.answer(
        success_msg,
        parse_mode="Markdown",
        reply_markup=kb.get_main_menu(lang) if hasattr(kb, 'get_main_menu') else None
    )

    # Admin guruhga xabar yuboramiz
    await send_to_admin_group(bot, app_code, message.from_user, data, app_record.get('id', 0))


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
📱 Username: @{message.from_user.username or "yoq"}
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


async def send_to_admin_group(bot: Bot, app_code: str, user, data: dict, app_id: int):
    """
    Admin guruhga ariza haqida to'liq xabar yuboradi
    """
    try:
        lang = data.get('language', 'uz')
        lang_name = LANG_NAMES.get(lang, "O'zbekcha")
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Xabar matnini tayyorlaymiz
        msg_text = f"""
🆕 **YANGI ARIZA** {get_webapp_text('uz', 'via_webapp')}

━━━━━━━━━━━━━━━━━━━━━━
🆔 **Kod:** `{app_code}`
━━━━━━━━━━━━━━━━━━━━━━

👤 **Foydalanuvchi:**
   • Ism: {user.full_name}
   • Username: @{user.username or "yoq"}
   • ID: `{user.id}`
   • Til: {lang_name}

📋 **Ariza ma'lumotlari:**
   • Xizmat: {data.get('service_type', 'EPI')}
   • Post: {data.get('border_post', '-')}
   • Manzil: {data.get('destination', '-')}
   • Mashina: {data.get('vehicle_number', '-')}
   • Mashina turi: {'Yuk' if data.get('vehicle_type') == 'truck' else 'Yengil'}
   • Agent: {data.get('agent_name', '-')}
   • Fayllar: {data.get('files_count', 0)} ta

⏰ **Vaqt:** {now}

━━━━━━━━━━━━━━━━━━━━━━
⚠️ Foydalanuvchiga hujjat rasmlarini
   alohida yuborishni so'rang!
━━━━━━━━━━━━━━━━━━━━━━
"""

        # Admin guruhga yuboramiz
        sent_msg = await bot.send_message(
            ADMIN_GROUP_ID,
            msg_text,
            parse_mode="Markdown"
        )

        # Admin tugmalarini qo'shamiz
        admin_kb = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Qabul qilish",
                    callback_data=f"accept_{app_code}"
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
            f"⚙️ `{app_code}` - Amallar:",
            reply_markup=admin_kb,
            parse_mode="Markdown"
        )

        # Message ID ni bazaga saqlaymiz
        try:
            await db.update_admin_message_id(app_code, sent_msg.message_id)
        except:
            pass

    except Exception as e:
        print(f"❌ Admin guruhga yuborishda xatolik: {e}")


# =========================================================================
# BALANCE CHECKER
# =========================================================================

@router.message(F.text.contains("Balans") | F.text.contains("Balance") | F.text.contains("💰") | F.text.contains("Tangalarim"))
async def show_balance(message: Message):
    user = await db.get_user(message.from_user.id)
    if not user:
        await message.answer("❌ /start bosing.")
        return

    balance = user.get('balance', 0)
    lang = user.get('language', 'uz')
    free_services = int(balance / 35000)

    msg = TEXTS.get(lang, TEXTS['uz']).get('balance_msg', '').format(balance=int(balance))
    if not msg:
        msg = f"💰 Balance: {balance:,.0f}"

    await message.answer(msg, parse_mode="Markdown")
