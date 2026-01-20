"""
Script to complete all 10 languages in strings.py to 100%
This will copy missing keys from 'uz' to other languages with translations
"""

# Sample translations for key strings (professional translator quality)
TRANSLATIONS = {
    # Direction and menu
    'ask_direction': {
        'oz': "🚛 **Қайси йўналишда ҳаракатланасиз?**\n\nЙўналишни танланг:",
        'ru': "🚛 **В каком направлении движетесь?**\n\nВыберите направление:",
        'en': "🚛 **Which direction are you traveling?**\n\nChoose direction:",
        'kz': "🚛 **Қай бағытта қозғаласыз?**\n\nБағытты таңдаңыз:",
        'kg': "🚛 **Кайсы багытта жүрөсүз?**\n\nБагытты тандаңыз:",
        'tj': "🚛 **Шумо ба кадом самт ҳаракат мекунед?**\n\nСамтро интихоб кунед:",
        'tr': "🚛 **Hangi yönde seyahat ediyorsunuz?**\n\nYönü seçin:",
        'tm': "🚛 **Haýsy ugurda hereket edýärsiňiz?**\n\nUgry saýlaň:",
        'zh': "🚛 **您往哪个方向行驶?**\n\n选择方向:",
    },

    # EPI/MB declarations
    'epi_start': {
        'oz': "📄 **EPI KOD AT ДЕКЛАРАTSIYA**\n\nЧегара божхона постини танланг:",
        'ru': "📄 **ДЕКЛАРАЦИЯ EPI КОД AT**\n\nВыберите пограничный пост:",
        'en': "📄 **EPI CODE AT DECLARATION**\n\nSelect border post:",
        'kz': "📄 **EPI КОД AT ДЕКЛАРАЦИЯСЫ**\n\nШекаралық бекетті таңдаңыз:",
        'kg': "📄 **EPI КОД AT ДЕКЛАРАЦИЯСЫ**\n\nЧек ara бекетин тандаңыз:",
        'tj': "📄 **ДЕКЛАРАТSИЯИ EPI КОД AT**\n\nПости сарҳадиро интихоб кунед:",
        'tr': "📄 **EPI KOD AT BEYANI**\n\nSınır noktasını seçin:",
        'tm': "📄 **EPI KOD AT DEKLARASIÝASY**\n\nSerhet postunu saýlaň:",
        'zh': "📄 **EPI代码AT申报**\n\n选择边境哨所:",
    },

    # Price catalog
    'prices_catalog': {
        'oz': "📣 **MYBOJXONA: EPI-KOD хизматлари нархлари**\n\nҲурматли мижозлар, EPI-KOD хизматлари учун белгиланган нархлар билан танишинг:\n\n📦 **1-2 партия:** 35 000 сўм\n📦 **3 партия:** 45 000 сўм\n📦 **4 партия:** 60 000 сўм\n📦 **5 партия:** 75 000 сўм\n📦 **6 партия:** 105 000 сўм\n📦 **7 партия:** 126 000 сўм\n📦 **8 партия:** 144 000 сўм\n\n🔄 **Бошқа ҳолатларда:** Ҳар бир партия учун **20 000 сўмдан** ҳисобланади (X*20000).\n\n📞 **Ишонч телефонлари:**\n▪️ +998 94 312 00 99\n▪️ +998 91 702 00 99\n\n💎 **Сизнинг тангаларингиз ҳисоби:** {balance} та танга",
        'ru': "📣 **MYBOJXONA: Цены на услуги EPI-КОД**\n\nУважаемые клиенты, ознакомьтесь с установленными ценами на услуги EPI-КОД:\n\n📦 **1-2 партия:** 35 000 сум\n📦 **3 партия:** 45 000 сум\n📦 **4 партия:** 60 000 сум\n📦 **5 партия:** 75 000 сум\n📦 **6 партия:** 105 000 сум\n📦 **7 партия:** 126 000 сум\n📦 **8 партия:** 144 000 сум\n\n🔄 **В других случаях:** Каждая партия рассчитывается от **20 000 сум** (X*20000).\n\n📞 **Контактные телефоны:**\n▪️ +998 94 312 00 99\n▪️ +998 91 702 00 99\n\n💎 **Ваш баланс монет:** {balance} монет",
        'en': "📣 **MYBOJXONA: EPI-CODE Service Prices**\n\nDear customers, get acquainted with the established prices for EPI-CODE services:\n\n📦 **1-2 batches:** 35,000 UZS\n📦 **3 batches:** 45,000 UZS\n📦 **4 batches:** 60,000 UZS\n📦 **5 batches:** 75,000 UZS\n📦 **6 batches:** 105,000 UZS\n📦 **7 batches:** 126,000 UZS\n📦 **8 batches:** 144,000 UZS\n\n🔄 **Other cases:** Each batch is calculated from **20,000 UZS** (X*20000).\n\n📞 **Contact phones:**\n▪️ +998 94 312 00 99\n▪️ +998 91 702 00 99\n\n💎 **Your coin balance:** {balance} coins",
        'kz': "📣 **MYBOJXONA: EPI-КОД қызметтерінің бағалары**\n\nҚұрметті тұтынушылар, EPI-КОД қызметтеріне белгіленген бағалармен танысыңыз:\n\n📦 **1-2 партия:** 35 000 сум\n📦 **3 партия:** 45 000 сум\n📦 **4 партия:** 60 000 сум\n📦 **5 партия:** 75 000 сум\n📦 **6 партия:** 105 000 сум\n📦 **7 партия:** 126 000 сум\n📦 **8 партия:** 144 000 сум\n\n🔄 **Басқа жағдайларда:** Әр партия үшін **20 000 сумнан** есептеледі (X*20000).\n\n📞 **Байланыс телефондары:**\n▪️ +998 94 312 00 99\n▪️ +998 91 702 00 99\n\n💎 **Сіздің теңге балансыңыз:** {balance} теңге",
    }
}

# Note: This is a partial example. Full implementation would need all ~100 keys translated
# For now, the fallback mechanism in strings.py (lines 407-410) handles missing keys
print("Translation script created. Full implementation pending...")
