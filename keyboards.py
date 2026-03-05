from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from strings import TEXTS

# =========================================================
# 1. POSTLAR RO'YXATI (REYTING BO'YICHA: TOP -> PASTGA) 🔥
# =========================================================

# CHEGARA BOJXONA POSTLARI (Jami 59 ta)
BORDER_POSTS_LIST = [
    "Yallama",
    "Olot",
    "Doʻstlik (Andijon)",
    "S. Najimov",
    "Dovut-ota",
    "Sirdaryo",
    "Ayritom",
    "Jartepa",
    "Oʻzbekiston",
    "Oybek",
    "Sariosiyo",
    "Uchqoʻrgʻon",
    "Shovot",
    "Islom Karimov nomidagi Toshkent xalqaro aeroporti",
    "Andarxon",
    "Xoʻjayli",
    "Kosonsoy",
    "Navoiy aeroporti",
    "Nukus aeroporti",
    "Qoraqalpogʻiston",
    "Doʻstlik (Qoraqalpog'iston)",
    "Andijon aeroporti",
    "Mingtepa",
    "Qorasuv",
    "Xonobod",
    "Pushmon",
    "Madaniyat",
    "Keskanyor",
    "Savay",
    "Buxoro aeroporti",
    "Xoʻjadavlat",
    "Uchtoʻrgʻon",
    "Qoʻshkent",
    "Qarshi-Kerki",
    "Qarshi aeroporti",
    "Namangan aeroporti",
    "Pop",
    "Samarqand aeroporti",
    "Termiz aeroporti",
    "Sariosiyo",
    "Gulbahor",
    "Boldir",
    "Xovosobod",
    "Oq oltin",
    "Malik",
    "Navoiy",
    "Bekobod avto",
    "Gʻishtkoʻprik",
    "Farhod",
    "Bekobod",
    "Fargʻona aeroporti",
    "Fargʻona",
    "Rishton",
    "Rovot",
    "Soʻx",
    "Doʻstlik (Xorazm)",
    "Urganch aeroporti",
    "Keles",
    "Chuqursoy texnik idora"
]

# TIF (TASHQI IQTISODIY FAOLIYAT) POSTLARI (Jami 33 ta)
TIF_POSTS_LIST = [
    "Avia yuklar",
    "Sirgʻali",
    "Chuqursoy",
    "Toshkent-tovar",
    "Termiz",
    "Buxoro",
    "Angren",
    "Vodiy",
    "Ark buloq",
    "Qorakoʻl",
    "Termiz xalqaro savdo markazi",
    "Nasaf",
    "Urganch",
    "Ulugʻbek",
    "Guliston",
    "Asaka",
    "Namangan",
    "Samarqand",
    "Jizzax",
    "Qoʻqon",
    "Nukus",
    "Andijon",
    "Qamashi-Gʻuzor",
    "Navoiy",
    "Zarafshon",
    "Denov",
    "Daryo porti",
    "Chirchiq",
    "Olmaliq",
    "Yangiyoʻl",
    "Nazarbek",
    "Keles",
    "Elektron tijorat"
]

# O'ZBEKISTON VILOYATLARI (14 ta hudud)
VILOYATLAR_LIST = [
    "Qoraqalpogʻiston Respublikasi",
    "Andijon viloyati",
    "Buxoro viloyati",
    "Fargʻona viloyati",
    "Jizzax viloyati",
    "Xorazm viloyati",
    "Namangan viloyati",
    "Navoiy viloyati",
    "Qashqadaryo viloyati",
    "Samarqand viloyati",
    "Sirdaryo viloyati",
    "Surxondaryo viloyati",
    "Toshkent viloyati",
    "Toshkent shahri"
]

# =========================================================
# 2. REGISTRATION KEYBOARDS
# =========================================================

# Tillar
def get_lang_kb():
    buttons = [
        [InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="lang_uz"),
         InlineKeyboardButton(text="🇺🇿 Ўзбекча", callback_data="lang_oz")],
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
         InlineKeyboardButton(text="🇺🇸 English", callback_data="lang_en")],
        [InlineKeyboardButton(text="🇰🇬 Кыргызча", callback_data="lang_kg"),
         InlineKeyboardButton(text="🇰🇿 Қазақша", callback_data="lang_kz")],
        [InlineKeyboardButton(text="🇹🇯 Тоҷикӣ", callback_data="lang_tj"),
         InlineKeyboardButton(text="🇹🇲 Turkmençe", callback_data="lang_tm")],
        [InlineKeyboardButton(text="🇹🇷 Türkçe", callback_data="lang_tr"),
         InlineKeyboardButton(text="🇨🇳 中文", callback_data="lang_zh")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_agreement_kb(lang):
    btn = "✅ Roziman" if lang in ['uz', 'oz'] else ("✅ Согласен" if lang == 'ru' else "✅ I Agree")
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=btn, callback_data="agree_yes")]])

def get_phone_kb(lang):
    t = "📱 Raqamni yuborish"
    if lang == 'ru': t = "📱 Отправить номер"
    elif lang == 'en': t = "📱 Share Contact"
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=t, request_contact=True)]], resize_keyboard=True)

# =========================================================
# 3. ASOSIY MENYU (17 TA XIZMAT)
# =========================================================

def get_main_menu(lang='uz'):
    """Asosiy menyu - 17 ta xizmat"""
    t = TEXTS.get(lang, TEXTS['uz'])

    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📄 " + t.get('menu_epi', 'EPI KOD AT DEKLARATSIYA')),
         KeyboardButton(text="📋 " + t.get('menu_mb', 'MB DEKLARATSIYA'))],
        [KeyboardButton(text="📞 " + t.get('menu_contacts', 'ISHONCH TELEFONLARI')),
         KeyboardButton(text="🎫 " + t.get('menu_apps', 'ARIZALARIM'))],
        [KeyboardButton(text="⚙️ " + t.get('menu_settings', 'SOZLAMALAR')),
         KeyboardButton(text="💰 " + t.get('menu_prices', 'NARXLAR KATALOGI'))],
        [KeyboardButton(text="📱 " + t.get('menu_app', 'DASTURNI YUKLAB OLING')),
         KeyboardButton(text="🚚 " + t.get('menu_kgd', 'KGD(E-TRANZIT) KORISH'))],
        [KeyboardButton(text="📜 " + t.get('menu_gabarit', 'GABARIT RUXSATNOMA OLISH')),
         KeyboardButton(text="🛡 " + t.get('menu_sugurta', 'SUGURTA'))],
        [KeyboardButton(text="🎯 " + t.get('menu_navbat', 'ELEKTRON NAVBAT')),
         KeyboardButton(text="✅ " + t.get('menu_yuklar', 'ISHONCHLI YUKLAR OLDI BERDI'))],
        [KeyboardButton(text="🎁 " + t.get('menu_bonus', 'BOT ORQALI BONUS')),
         KeyboardButton(text="💎 " + t.get('menu_balance', 'TANGALARIM HISOBI'))],
        [KeyboardButton(text="📱 " + t.get('menu_social', 'SOCIAL MEDIA')),
         KeyboardButton(text="💬 " + t.get('menu_chat', 'GAPLASHISH'))]
    ], resize_keyboard=True)

# =========================================================
# 4. ORTGA VA BEKOR QILISH TUGMALARI
# =========================================================

def get_back_kb(lang='uz'):
    """Ortga qaytish tugmasi"""
    t = TEXTS.get(lang, TEXTS['uz'])
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="⬅️ " + t.get('btn_back', 'Ortga'))]
    ], resize_keyboard=True)

def get_cancel_kb(lang='uz'):
    """Bekor qilish va ortga"""
    t = TEXTS.get(lang, TEXTS['uz'])
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="⬅️ " + t.get('btn_back', 'Ortga')),
         KeyboardButton(text="❌ " + t.get('btn_cancel', 'Bekor qilish'))]
    ], resize_keyboard=True)

def get_chat_kb(lang='uz'):
    """Chat davom etish - Chatni tugatish tugmasi"""
    t = TEXTS.get(lang, TEXTS['uz'])
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="🏁 " + t.get('btn_end_chat', 'Chatni tugatish'))]
    ], resize_keyboard=True)

# =========================================================
# 5. ISHONCH TELEFONLARI KEYBOARDS
# =========================================================

def get_contact_info_kb(lang='uz'):
    """Ishonch telefonlari menyusi - 4 ta asosiy funksiya"""
    t = TEXTS.get(lang, TEXTS['uz'])
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📱 " + t.get('btn_change_phone', 'RAQAMNI O\'ZGARTIRISH'))],
        [KeyboardButton(text="🌐 " + t.get('btn_change_lang', 'TILNI O\'ZGARTIRISH'))],
        [KeyboardButton(text="🗑 " + t.get('btn_clear_cache', 'XOTIRANI TOZALASH'))],
        [KeyboardButton(text="👨‍💼 " + t.get('btn_admin_contact', 'ADMIN BILAN ALOQA'))],
        [KeyboardButton(text="⬅️ " + t.get('btn_back', 'Ortga'))]
    ], resize_keyboard=True)

def get_contact_info_inline_kb():
    """Admin bilan aloqa - 3 ta tugma"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📞 +998 91 702 00 99\n📞 +998 94 312 00 99", callback_data="contact_phone")],
        [InlineKeyboardButton(text="📱 TELEGRAM: @CARAVAN_TRANZIT @caravan_tranzit1", url="https://t.me/CARAVAN_TRANZIT")],
        [InlineKeyboardButton(text="💬 WHATSAPP: +998 91 702 00 99\n+998 94 312 00 99", url="https://chat.whatsapp.com/Ka6XhUv2ueVFZPNuHo06BP")]
    ])

def get_admin_contact_detailed_kb():
    """Admin bilan aloqa - batafsil inline klaviatura"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📱 Telegram: @CARAVAN_TRANZIT", url="https://t.me/CARAVAN_TRANZIT")],
        [InlineKeyboardButton(text="📱 Telegram: @caravan_tranzit1", url="https://t.me/caravan_tranzit1")],
        [InlineKeyboardButton(text="💬 WhatsApp Group", url="https://chat.whatsapp.com/Ka6XhUv2ueVFZPNuHo06BP")]
    ])

# =========================================================
# 6. ARIZALARIM KEYBOARDS
# =========================================================

def get_applications_menu_kb(lang='uz'):
    """Arizalarim menyusi"""
    t = TEXTS.get(lang, TEXTS['uz'])
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="🔍 " + t.get('btn_search_app', 'ARIZA BOR'))],
        [KeyboardButton(text="📂 " + t.get('btn_my_apps', 'ARIZALARIM'))],
        [KeyboardButton(text="⬅️ " + t.get('btn_back', 'Ortga'))]
    ], resize_keyboard=True)

def get_payment_methods_kb(lang='uz'):
    """To'lov usullari"""
    t = TEXTS.get(lang, TEXTS['uz'])
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="💳 UzumBank"), KeyboardButton(text="💳 Click")],
        [KeyboardButton(text="💳 Paynet"), KeyboardButton(text="💳 Payme")],
        [KeyboardButton(text="💵 " + t.get('btn_cash', 'AGENTLAR ORQALI NAXD PULDA'))],
        [KeyboardButton(text="⬅️ " + t.get('btn_back', 'Ortga'))]
    ], resize_keyboard=True)

# =========================================================
# 7. SOZLAMALAR KEYBOARDS
# =========================================================

def get_settings_kb(lang='uz'):
    """Sozlamalar menyusi"""
    t = TEXTS.get(lang, TEXTS['uz'])
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📱 " + t.get('btn_change_phone', 'RAQAMNI O\'ZGARTIRISH'))],
        [KeyboardButton(text="🌐 " + t.get('btn_change_lang', 'TILNI O\'ZGARTIRISH'))],
        [KeyboardButton(text="🗑 " + t.get('btn_clear_cache', 'XOTIRANI TOZALASH'))],
        [KeyboardButton(text="👨‍💼 " + t.get('btn_admin_contact', 'ADMIN BILAN ALOQA'))],
        [KeyboardButton(text="⬅️ " + t.get('btn_back', 'Ortga'))]
    ], resize_keyboard=True)

def get_admin_contact_kb():
    """Admin bilan aloqa - inline"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📱 Telegram: @CARAVAN_TRANZIT", url="https://t.me/CARAVAN_TRANZIT")],
        [InlineKeyboardButton(text="📱 Telegram: @caravan_tranzit1", url="https://t.me/caravan_tranzit1")],
        [InlineKeyboardButton(text="💬 WhatsApp", url="https://wa.me/998917020099")]
    ])

# =========================================================
# 8. DASTURNI YUKLAB OLING KEYBOARDS
# =========================================================

def get_app_download_kb(lang='uz'):
    """Dastur yuklab olish menyusi"""
    t = TEXTS.get(lang, TEXTS['uz'])
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="🔗 " + t.get('btn_app_link', 'DASTURNI YUKLAB OLING HAVOLA'))],
        [KeyboardButton(text="📖 " + t.get('btn_app_guide', 'DASTURDAN FOYDALANISH YO\'RIQNOMASI'))],
        [KeyboardButton(text="🎁 " + t.get('btn_bonus_guide', 'DASTUR ORQALI BONUS OLISH YO\'RIQNOMASI'))],
        [KeyboardButton(text="⬅️ " + t.get('btn_back', 'Ortga'))]
    ], resize_keyboard=True)

# =========================================================
# 9. KGD (E-TRANZIT) KO'RISH KEYBOARDS
# =========================================================

def get_kgd_menu_kb(lang='uz'):
    """KGD ko'rish menyusi"""
    t = TEXTS.get(lang, TEXTS['uz'])
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📱 " + t.get('btn_kgd_app', 'DASTUR ORQALI KO\'RISH'))],
        [KeyboardButton(text="👥 " + t.get('btn_kgd_staff', 'XODIMLAR ORQALI KO\'RISH'))],
        [KeyboardButton(text="⬅️ " + t.get('btn_back', 'Ortga'))]
    ], resize_keyboard=True)

def get_kgd_app_submenu_kb(lang='uz'):
    """KGD dastur submenyusi"""
    t = TEXTS.get(lang, TEXTS['uz'])
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="🔗 " + t.get('btn_download', 'Yuklab olish uchun havola'))],
        [KeyboardButton(text="📖 " + t.get('btn_guide_use', 'Foydalanish bo\'yicha qo\'llanma'))],
        [KeyboardButton(text="🔍 " + t.get('btn_guide_kgd', 'KGD ko\'rish bo\'yicha qo\'llanma'))],
        [KeyboardButton(text="🎁 " + t.get('btn_bonus_rule', 'Bonus olish qoidasi'))],
        [KeyboardButton(text="⬅️ " + t.get('btn_back', 'Ortga'))]
    ], resize_keyboard=True)

# =========================================================
# 10. BOT ORQALI BONUS KEYBOARDS
# =========================================================

def get_bonus_menu_kb(lang='uz'):
    """Bonus menyusi"""
    t = TEXTS.get(lang, TEXTS['uz'])
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="🔗 " + t.get('btn_get_link', 'HAVOLANGIZNI OLING VA DO\'STLARINGIZGA YUBORING'))],
        [KeyboardButton(text="ℹ️ " + t.get('btn_bonus_info', 'QANDAY BONUS EKANLIGI HAQIDA TUSHUNTIRISHNOMA'))],
        [KeyboardButton(text="💎 " + t.get('btn_my_coins', 'TANGALARIM'))],
        [KeyboardButton(text="⬅️ " + t.get('btn_back', 'Ortga'))]
    ], resize_keyboard=True)

# =========================================================
# 11. SOCIAL MEDIA KEYBOARDS
# =========================================================

def get_social_media_kb():
    """Social Media havolalar"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 TELEGRAM KANAL", url="https://t.me/caravan_tranzit_channel")],
        [InlineKeyboardButton(text="💬 TELEGRAM GRUPPA", url="https://t.me/caravan_tranzit_chat")],
        [InlineKeyboardButton(text="💬 WHATSAPP", url="https://chat.whatsapp.com/Ka6XhUv2ueVFZPNuHo06BP")],
        [InlineKeyboardButton(text="📺 YOUTUBE", url="https://youtube.com/@caravan_tranzit")],
        [InlineKeyboardButton(text="📸 INSTAGRAM", url="https://instagram.com/caravan_tranzit")],
        [InlineKeyboardButton(text="🤖 TELEGRAM BOT", url="https://t.me/caravan_tranzit_bot")]
    ])

# =========================================================
# 12. DINAMIK POSTLAR (2 QATORLI)
# =========================================================
def get_posts_kb():
    """Chegara postlari - birinchi qatorda ANIQ EMAS"""
    builder = ReplyKeyboardBuilder()
    # Birinchi qatorda ANIQ EMAS
    builder.add(KeyboardButton(text="❓ ANIQ EMAS"))
    for post in BORDER_POSTS_LIST:
        builder.add(KeyboardButton(text=post))
    builder.add(KeyboardButton(text="⬅️ Ortga"))
    builder.adjust(1, 2)  # Birinchi qator 1 ta, qolganlari 2 tadan
    return builder.as_markup(resize_keyboard=True)

def get_dest_posts_kb():
    """TIF (Manzil) postlari - birinchi qatorda ANIQ EMAS"""
    builder = ReplyKeyboardBuilder()
    # Birinchi qatorda ANIQ EMAS
    builder.add(KeyboardButton(text="❓ ANIQ EMAS"))
    for post in TIF_POSTS_LIST:
        builder.add(KeyboardButton(text=post))
    builder.add(KeyboardButton(text="⬅️ Ortga"))
    builder.adjust(1, 2)  # Birinchi qator 1 ta, qolganlari 2 tadan
    return builder.as_markup(resize_keyboard=True)

def get_dest_border_posts_kb():
    """Manzil chegara postlari - TRANZIT uchun"""
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="❓ ANIQ EMAS"))
    for post in BORDER_POSTS_LIST:
        builder.add(KeyboardButton(text=post))
    builder.add(KeyboardButton(text="⬅️ Ortga"))
    builder.adjust(1, 2)
    return builder.as_markup(resize_keyboard=True)

def get_viloyatlar_kb():
    """O'zbekiston viloyatlari - ANIQ EMAS bosilganda"""
    builder = ReplyKeyboardBuilder()
    for viloyat in VILOYATLAR_LIST:
        builder.add(KeyboardButton(text=viloyat))
    builder.add(KeyboardButton(text="⬅️ Ortga"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

# =========================================================
# 13. HUJJAT YIQISH KEYBOARDS
# =========================================================

def get_done_kb(lang='uz'):
    """Yuklab bo'ldim tugmasi"""
    t = TEXTS.get(lang, TEXTS['uz'])
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="✅ " + t.get('btn_done', 'Yuklab bo\'ldim'))],
        [KeyboardButton(text="⬅️ " + t.get('btn_back', 'Ortga'))]
    ], resize_keyboard=True)

# =========================================================
# 14. ADMIN KEYBOARDS
# =========================================================

def get_admin_claim_kb(app_code):
    """Admin qabul qilish va rad etish tugmalari"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ QABUL QILISH", callback_data=f"claim_{app_code}")],
        [InlineKeyboardButton(text="❌ RAD ETISH", callback_data=f"reject_{app_code}")]
    ])

def get_pricing_kb(app_code):
    """Narx belgilash tugmalari"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📦 1-2 Partiya (35 000)", callback_data=f"setprice_35000_{app_code}")],
        [InlineKeyboardButton(text="📦 3 Partiya (45 000)", callback_data=f"setprice_45000_{app_code}")],
        [InlineKeyboardButton(text="📦 4+ Partiya (60 000)", callback_data=f"setprice_60000_{app_code}")],
        [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel_pay")]
    ])

def get_user_payment_methods(app_code, amount):
    """Foydalanuvchi uchun to'lov usullari"""
    from payme_api import generate_checkout_url
    from click_api import ClickAPI
    from decimal import Decimal

    payme_url = generate_checkout_url(app_code, Decimal(str(amount)))
    click_url = ClickAPI.generate_payment_url(app_code, Decimal(str(amount)))

    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"💳 Payme ({amount:,.0f} UZS)", url=payme_url)],
        [InlineKeyboardButton(text=f"💳 Click ({amount:,.0f} UZS)", url=click_url)],
        [InlineKeyboardButton(text="🪙 Tangalardan to'lash", callback_data=f"pay_coins_{app_code}")],
        [InlineKeyboardButton(text="❌ Bekor qilish", callback_data=f"cancel_payment_{app_code}")]
    ])
