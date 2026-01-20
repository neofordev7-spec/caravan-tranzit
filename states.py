from aiogram.fsm.state import State, StatesGroup

# ==========================================================
# 1. RO'YXATDAN O'TISH (YANGILANGAN)
# ==========================================================
class Registration(StatesGroup):
    lang = State()          # Til tanlash
    agreement = State()     # Rozilik berish
    phone = State()         # Telefon raqam yuborish
    direction = State()     # Yo'nalish tanlash (IMPORT/EKSPORT/TRANZIT)

# ==========================================================
# 2. EPI KOD AT DEKLARATSIYA
# ==========================================================
class EPIKodFlow(StatesGroup):
    select_border_post = State()    # Chegara bojxona postini tanlash
    select_agent = State()           # Agent tanlash
    select_dest_post = State()       # Manzil bojxona postini tanlash (IMPORT/TRANZIT uchun)
    enter_car_number = State()       # Mashina raqamini kiritish
    collect_docs = State()           # Hujjatlarni yig'ish
    waiting_payment = State()        # To'lov kutish

# ==========================================================
# 3. MB DEKLARATSIYA
# ==========================================================
class MBDeklaratsiyaFlow(StatesGroup):
    select_border_post = State()    # Chegara bojxona postini tanlash
    select_agent = State()           # Agent tanlash
    select_dest_post = State()       # Manzil bojxona postini tanlash (faqat IMPORT/TRANZIT)
    enter_car_number = State()       # Mashina raqamini kiritish
    collect_docs = State()           # Hujjatlarni yig'ish
    waiting_payment = State()        # To'lov kutish

# ==========================================================
# 4. ARIZALARIM
# ==========================================================
class ApplicationsFlow(StatesGroup):
    choose_option = State()          # "ARIZA BOR" yoki "ARIZALARIM" tanlash
    enter_car_for_search = State()   # Mashina raqamini kiritish (ARIZA BOR uchun)
    view_my_apps = State()           # Arizalarimni ko'rish
    select_payment_method = State()  # To'lov usulini tanlash

# ==========================================================
# 5. SOZLAMALAR
# ==========================================================
class SettingsFlow(StatesGroup):
    menu = State()                   # Sozlamalar menyusi
    change_phone = State()           # Raqamni o'zgartirish
    change_language = State()        # Tilni o'zgartirish
    contact_admin = State()          # Admin bilan aloqa

# ==========================================================
# 5.5. ISHONCH TELEFONLARI (CONTACT INFO)
# ==========================================================
class ContactInfoFlow(StatesGroup):
    menu = State()                   # Ishonch telefonlari menyusi
    change_phone = State()           # Raqamni o'zgartirish
    change_language = State()        # Tilni o'zgartirish

# ==========================================================
# 6. KGD (E-TRANZIT) KO'RISH
# ==========================================================
class KGDFlow(StatesGroup):
    choose_method = State()          # "Dastur orqali" yoki "Xodimlar orqali"
    enter_car_number = State()       # Mashina raqamini kiritish (Xodimlar uchun)

# ==========================================================
# 7. BOT ORQALI BONUS (REFERRAL TIZIMI)
# ==========================================================
class BonusFlow(StatesGroup):
    menu = State()                   # Bonus menyusi
    show_link = State()              # Havolani ko'rsatish
    show_balance = State()           # Balansni ko'rsatish

# ==========================================================
# 8. GAPLASHISH (CHAT)
# ==========================================================
class ChatFlow(StatesGroup):
    waiting_message = State()        # Xabar kutish

# ==========================================================
# 9. ADMIN HARAKATLARI
# ==========================================================
class AdminState(StatesGroup):
    waiting_for_price = State()      # Narx belgilash
    waiting_for_response = State()   # Javob yozish
