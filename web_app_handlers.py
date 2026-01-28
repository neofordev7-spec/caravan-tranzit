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
    }
}

def get_webapp_text(lang: str, key: str) -> str:
    """Tilga mos matnni olish"""
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
📱 Username: @{message.from_user.username or 'yo\'q'}
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
   • Username: @{user.username or 'yo\'q'}
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
