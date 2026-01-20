"""
WEB APP HANDLERS
Telegram Web App ma'lumotlarini qabul qilish va qayta ishlash
"""
import json
import random
from aiogram import Router, F, Bot
from aiogram.types import Message, InputMediaPhoto
from database import db
from strings import TEXTS
import keyboards as kb

router = Router()

# Admin guruh ID
ADMIN_GROUP_ID = -1003463212374

@router.message(F.web_app_data)
async def handle_web_app_data(message: Message, bot: Bot):
    """
    Web App dan kelgan ma'lumotlarni qayta ishlash
    """
    try:
        # Web App dan kelgan JSON ma'lumotlarni parse qilamiz
        data = json.loads(message.web_app_data.data)

        # Ma'lumotlarni olamiz
        post_id = data.get('post_id')
        post_name = data.get('post_name')
        agent_id = data.get('agent_id')
        agent_name = data.get('agent_name')
        vehicle_number = data.get('vehicle_number')
        vehicle_type = data.get('vehicle_type')
        files_count = data.get('files_count', 0)

        # Foydalanuvchi ma'lumotlarini olamiz
        user = await db.get_user(message.from_user.id)
        if not user:
            await message.answer("❌ Xatolik: Foydalanuvchi topilmadi. /start bosing.")
            return

        lang = user['language']

        # Ariza kodini generatsiya qilamiz
        app_type = "TRUCK" if vehicle_type == "truck" else "CAR"
        app_code = f"{app_type}-{random.randint(10000, 99999)}"

        # MUHIM: Hozircha rasmlar Web App dan to'g'ridan-to'g'ri kelmaydi
        # Chunki Telegram Web App faqat kichik hajmdagi ma'lumotlarni yuboradi
        # Shuning uchun biz foydalanuvchidan rasmlarni alohida yuborishini so'raymiz

        await message.answer(
            f"✅ **Ma'lumotlar qabul qilindi!**\n\n"
            f"🆔 Ariza: `{app_code}`\n"
            f"📍 Post: {post_name}\n"
            f"👤 Agent: {agent_name}\n"
            f"🚛 Mashina: {vehicle_number}\n\n"
            f"📸 **Endi hujjat rasmlarini yuborishingiz kerak:**\n"
            f"Barcha rasmlarni ketma-ket yuboring, keyin /done buyrug'ini yuboring.",
            parse_mode="Markdown"
        )

        # Arizani bazaga saqlaymiz (statusni 'awaiting_files' ga o'rnatamiz)
        await db.create_application(
            app_code=app_code,
            user_id=message.from_user.id,
            agent_id=agent_id,
            post_id=post_id,
            vehicle_number=vehicle_number,
            vehicle_type=vehicle_type,
            files={},  # Hozircha bo'sh
            metadata={
                'post_name': post_name,
                'agent_name': agent_name,
                'status': 'awaiting_files'
            }
        )

        # Vaqtinchalik ma'lumotlarni FSM state da saqlaymiz
        # (Bu yerda biz oddiy yondashuv qo'llaymiz - foydalanuvchidan rasmlarni to'g'ridan-to'g'ri so'raymiz)

    except json.JSONDecodeError:
        await message.answer("❌ Ma'lumotlarni o'qishda xatolik yuz berdi.")
    except Exception as e:
        print(f"Web App handler error: {e}")
        await message.answer("❌ Xatolik yuz berdi. Qaytadan urinib ko'ring.")


# =========================================================================
# ALTERNATIVE APPROACH: Full workflow through Web App (with file uploads)
# =========================================================================

@router.message(F.web_app_data)
async def handle_web_app_data_v2(message: Message, bot: Bot):
    """
    Web App dan kelgan to'liq ma'lumotlarni qayta ishlash
    (Rasmlar bilan birga - production versiya)
    """
    try:
        data = json.loads(message.web_app_data.data)

        # Ma'lumotlarni olamiz
        post_id = data.get('post_id')
        post_name = data.get('post_name')
        agent_id = data.get('agent_id')
        agent_name = data.get('agent_name')
        vehicle_number = data.get('vehicle_number')
        vehicle_type = data.get('vehicle_type')

        # Ariza kodini generatsiya qilamiz
        app_type = "TRUCK" if vehicle_type == "truck" else "CAR"
        app_code = f"{app_type}-{random.randint(10000, 99999)}"

        # Foydalanuvchiga tasdiq xabarini yuboramiz
        user = await db.get_user(message.from_user.id)
        lang = user['language'] if user else 'uz'

        success_msg = f"""
✅ **Ariza muvaffaqiyatli yuborildi!**

🆔 Ariza kodi: `{app_code}`
📍 Post: {post_name}
👤 Agent: {agent_name}
🚛 Transport: {vehicle_number}

⏳ Tez orada admindan javob olasiz...
"""

        await message.answer(success_msg, parse_mode="Markdown", reply_markup=kb.get_main_menu(lang))

        # Arizani bazaga saqlaymiz
        app_record = await db.create_application(
            app_code=app_code,
            user_id=message.from_user.id,
            agent_id=agent_id,
            post_id=post_id,
            vehicle_number=vehicle_number,
            vehicle_type=vehicle_type,
            files={},  # Rasmlar file_id lar shu yerda saqlanadi
            metadata={
                'post_name': post_name,
                'agent_name': agent_name,
                'via_webapp': True
            }
        )

        # Admin guruhga xabar yuboramiz
        await send_to_admin_group(bot, app_code, message.from_user, data, app_record['id'])

    except Exception as e:
        print(f"❌ Web App handler error: {e}")
        await message.answer("❌ Xatolik yuz berdi. /start bosib qaytadan urinib ko'ring.")


async def send_to_admin_group(bot: Bot, app_code: str, user, data: dict, app_id: int):
    """
    Admin guruhga ariza haqida xabar yuboradi
    """
    try:
        # Xabar matnini tayyorlaymiz
        msg_text = f"""
🆕 **YANGI ARIZA (Web App)**

🆔 Kod: `{app_code}`
👤 Foydalanuvchi: {user.full_name}
📞 Username: @{user.username or 'yo\'q'}
📱 ID: `{user.id}`

📍 Post: {data.get('post_name')}
👤 Agent: {data.get('agent_name')}
🚛 Mashina: {data.get('vehicle_number')}
🚗 Tur: {'Yuk mashinasi' if data.get('vehicle_type') == 'truck' else 'Yengil mashina'}

⚠️ **Hujjatlar:** Foydalanuvchi rasmlarni alohida yuboradi
"""

        # Admin guruhga yuboramiz
        sent_msg = await bot.send_message(
            ADMIN_GROUP_ID,
            msg_text,
            parse_mode="Markdown"
        )

        # Admin tugmalarini qo'shamiz
        from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
        admin_kb = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="❌ Rad etish", callback_data=f"reject_{app_code}"),
                InlineKeyboardButton(text="💰 Narx belgilash", callback_data=f"setprice_{app_code}")
            ]
        ])

        await bot.send_message(
            ADMIN_GROUP_ID,
            f"🆔 `{app_code}` - Amallar:",
            reply_markup=admin_kb,
            parse_mode="Markdown"
        )

        # Message ID ni bazaga saqlaymiz
        await db.update_admin_message_id(app_code, sent_msg.message_id)

    except Exception as e:
        print(f"❌ Admin guruhga yuborishda xatolik: {e}")


# =========================================================================
# BALANCE CHECKER
# =========================================================================

@router.message(F.text.contains("Balans") | F.text.contains("Balance") | F.text.contains("💰"))
async def show_balance(message: Message):
    """
    Foydalanuvchi balansini ko'rsatadi
    """
    user = await db.get_user(message.from_user.id)
    if not user:
        await message.answer("❌ /start bosing.")
        return

    balance = user['balance']
    lang = user['language']

    # 35,000 coins = 1 free service
    free_services = int(balance / 35000)

    msg = f"""
💰 **Sizning balansingiz:**

🪙 Tangalar: **{balance:,.0f}**
🎁 Bepul xizmatlar: **{free_services}**

📊 **Tanga ishlating:**
• 35,000 tanga = 1 bepul deklaratsiya
• Do'stlarni taklif qiling: +2,000 tanga
• Do'stingiz xizmatdan foydalansa: +17,500 tanga

🔗 **Taklif havolangiz:**
https://t.me/YOUR_BOT_USERNAME?start={message.from_user.id}
"""

    await message.answer(msg, parse_mode="Markdown")
