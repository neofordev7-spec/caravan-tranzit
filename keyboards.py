import base64
import os
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from strings import TEXTS
from decimal import Decimal

# PAYME_MERCHANT_ID ni Railway Variables'dan oladi
PAYME_ID = os.getenv("PAYME_MERCHANT_ID", "YOUR_MERCHANT_ID")

# =========================================================
# 1. POSTLAR RO'YXATI
# =========================================================

BORDER_POSTS_LIST = [
    "Yallama", "Olot", "Doʻstlik (Andijon)", "S. Najimov", "Dovut-ota", "Sirdaryo",
    "Ayritom", "Jartepa", "Oʻzbekiston", "Oybek", "Sariosiyo", "Uchqoʻrgʻon",
    "Shovot", "Islom Karimov nomidagi Toshkent xalqaro aeroporti", "Andarxon",
    "Xoʻjayli", "Kosonsoy", "Navoiy aeroporti", "Nukus aeroporti", "Qoraqalpogʻiston",
    "Doʻstlik (Qoraqalpog'iston)", "Andijon aeroporti", "Mingtepa", "Qorasuv",
    "Xonobod", "Pushmon", "Madaniyat", "Keskanyor", "Savay", "Buxoro aeroporti",
    "Xoʻjadavlat", "Uchtoʻrgʻon", "Qoʻshkent", "Qarshi-Kerki", "Qarshi aeroporti",
    "Namangan aeroporti", "Pop", "Samarqand aeroporti", "Termiz aeroporti",
    "Sariosiyo", "Gulbahor", "Boldir", "Xovosobod", "Oq oltin", "Malik", "Navoiy",
    "Bekobod avto", "Gʻishtkoʻprik", "Farhod", "Bekobod", "Fargʻona aeroporti",
    "Fargʻona", "Rishton", "Rovot", "Soʻx", "Doʻstlik (Xorazm)", "Urganch aeroporti",
    "Keles", "Chuqursoy texnik idora"
]

TIF_POSTS_LIST = [
    "Avia yuklar", "Sirgʻali", "Chuqursoy", "Toshkent-tovar", "Termiz", "Buxoro",
    "Angren", "Vodiy", "Ark buloq", "Qorakoʻl", "Termiz xalqaro savdo markazi",
    "Nasaf", "Urganch", "Ulugʻbek", "Guliston", "Asaka", "Namangan", "Samarqand",
    "Jizzax", "Qoʻqon", "Nukus", "Andijon", "Qamashi-Gʻuzor", "Navoiy", "Zarafshon",
    "Denov", "Daryo porti", "Chirchiq", "Olmaliq", "Yangiyoʻl", "Nazarbek",
    "Keles", "Elektron tijorat"
]

VILOYATLAR_LIST = [
    "Qoraqalpogʻiston Respublikasi", "Andijon viloyati", "Buxoro viloyati",
    "Fargʻona viloyati", "Jizzax viloyati", "Xorazm viloyati", "Namangan viloyati",
    "Navoiy viloyati", "Qashqadaryo viloyati", "Samarqand viloyati",
    "Sirdaryo viloyati", "Surxondaryo viloyati", "Toshkent viloyati", "Toshkent shahri"
]

# =========================================================
# 2. TO'LOV LINKI GENERATORI (PAYME FIX) 🔥
# =========================================================

def generate_payme_link(app_code, amount_uzs):
    """Payme uchun to'g'ridan-to'g'ri to'lov havolasini yaratish"""
    # Payme summani tiyinda qabul qiladi (So'm * 100)
    tiyin_amount = int(Decimal(str(amount_uzs)) * 100)
    # Parametrlarni yig'amiz
    params = f"m={PAYME_ID};ac.app_code={app_code};a={tiyin_amount}"
    # Base64 kodlash
    encoded_params = base64.b64encode(params.encode()).decode()
    return f"https://checkout.payme.uz/{encoded_params}"

# =========================================================
# 3. KLAVIATURALAR
# =========================================================

def get_lang_kb():
    buttons = [
        [InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="lang_uz"),
         InlineKeyboardButton(text="🇺🇿 Ўзбекча", callback_data="lang_oz")],
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
         InlineKeyboardButton(text="🇺🇸 English", callback_data="lang_en")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_main_menu(lang='uz'):
    t = TEXTS.get(lang, TEXTS['uz'])
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📄 " + t.get('menu_epi', 'EPI KOD AT DEKLARATSIYA')),
         KeyboardButton(text="📋 " + t.get('menu_mb', 'MB DEKLARATSIYA'))],
        [KeyboardButton(text="🎫 " + t.get('menu_apps', 'ARIZALARIM')),
         KeyboardButton(text="⚙️ " + t.get('menu_settings', 'SOZLAMALAR'))],
        [KeyboardButton(text="💰 " + t.get('menu_prices', 'NARXLAR KATALOGI')),
         KeyboardButton(text="🚚 " + t.get('menu_kgd', 'KGD(E-TRANZIT)'))],
        [KeyboardButton(text="🎁 " + t.get('menu_bonus', 'BONUS')),
         KeyboardButton(text="💬 " + t.get('menu_chat', 'GAPLASHISH'))]
    ], resize_keyboard=True)

# MB DEKLARATSIYA UCHUN MAXSUS MANZIL POSTLARI 🚚
def get_mb_dest_posts_kb():
    """MB uchun: Yo'q, Aniq emas va Chegara postlari"""
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="❌ YO'Q"))
    builder.add(KeyboardButton(text="❓ ANIQ EMAS"))
    for post in BORDER_POSTS_LIST:
        builder.add(KeyboardButton(text=post))
    builder.add(KeyboardButton(text="⬅️ Ortga"))
    builder.adjust(2) # Tugmalarni chiroyli 2 qator qiladi
    return builder.as_markup(resize_keyboard=True)

def get_posts_kb():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="❓ ANIQ EMAS"))
    for post in BORDER_POSTS_LIST:
        builder.add(KeyboardButton(text=post))
    builder.add(KeyboardButton(text="⬅️ Ortga"))
    builder.adjust(1, 2)
    return builder.as_markup(resize_keyboard=True)

def get_dest_posts_kb():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="❓ ANIQ EMAS"))
    for post in TIF_POSTS_LIST:
        builder.add(KeyboardButton(text=post))
    builder.add(KeyboardButton(text="⬅️ Ortga"))
    builder.adjust(1, 2)
    return builder.as_markup(resize_keyboard=True)

# TO'LOV TUGMALARI FIX 🔥
def get_user_payment_methods(app_code, amount):
    """Foydalanuvchi uchun to'lov usullari (Dinamik linklar bilan)"""
    payme_url = generate_payme_link(app_code, amount)
    # Click linki (Agar kodingizda ClickAPI bo'lsa shuni ishlating)
    click_url = f"https://my.click.uz/services/pay?service_id=YOUR_ID&merchant_id=YOUR_M_ID&amount={amount}&transaction_param={app_code}"

    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"💳 Payme ({amount:,.0f} UZS)", url=payme_url)],
        [InlineKeyboardButton(text=f"💳 Click ({amount:,.0f} UZS)", url=click_url)],
        [InlineKeyboardButton(text="🪙 Tangalardan to'lash", callback_data=f"pay_coins_{app_code}")],
        [InlineKeyboardButton(text="❌ Bekor qilish", callback_data=f"cancel_payment_{app_code}")]
    ])

def get_admin_contact_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📱 Telegram: @CARAVAN_TRANZIT", url="https://t.me/CARAVAN_TRANZIT")],
        [InlineKeyboardButton(text="💬 WhatsApp", url="https://wa.me/998917020099")]
    ])

# Qolgan barcha standart funksiyalar (get_phone_kb, get_done_kb va h.k.) o'z holicha qoladi...
