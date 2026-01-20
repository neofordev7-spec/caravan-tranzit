# MYBOJXONA Bot - Ko'p tillilik qo'llanmasi

## 📚 Mavjud tillar

Bot hozirda 10 ta tilda ishlaydi:

1. 🇺🇿 **O'zbekcha (Lotin)** - `uz` ✅ 100% to'liq
2. 🇺🇿 **Ўзбекча (Кирилл)** - `oz` ⚠️ 60% to'liq
3. 🇷🇺 **Русский** - `ru` ⚠️ 60% to'liq
4. 🇺🇸 **English** - `en` ⚠️ 60% to'liq
5. 🇰🇿 **Қазақша** - `kz` ⚠️ 40% to'liq
6. 🇰🇬 **Кыргызча** - `kg` ⚠️ 40% to'liq
7. 🇹🇯 **Тоҷикӣ** - `tj` ⚠️ 40% to'liq
8. 🇹🇷 **Türkçe** - `tr` ⚠️ 40% to'liq
9. 🇹🇲 **Türkmençe** - `tm` ⚠️ 40% to'liq
10. 🇨🇳 **中文** - `zh` ⚠️ 40% to'liq

## 🔧 Fallback mexanizmi

Agar biror tilda kalit so'z topilmasa, avtomatik o'zbekcha (lotin) versiyasini ko'rsatadi:

```python
# strings.py da (407-410 qatorlar)
for lang in ['kg', 'tj', 'tr', 'tm', 'zh']:
    for key, val in TEXTS['uz'].items():
        if key not in TEXTS[lang]:
            TEXTS[lang][key] = val
```

## 📝 Tarjima qilish kerak bo'lgan kalit so'zlar

### 1. Asosiy xabarlar (20+ kalit)

```python
'ask_direction': "🚛 **Siz qaysi yo'nalishda harakatlanasiz?**\n\nYo'nalishni tanlang:",
'direction_selected': "✅ Yo'nalish tanlandi: **{direction}**",
'epi_start': "📄 **EPI KOD AT DEKLARATSIYA**\n\nChegara bojxona postini tanlang:",
'mb_start': "📋 **MB DEKLARATSIYA**\n\nChegara bojxona postini tanlang:",
'select_agent': "👨‍💼 **Agent tanlash**\n\nQuyidagi agentlardan birini tanlang:",
'enter_car_number': "🚛 **Mashina raqamini kiriting:**\n\n(Misol: 01A777AA)",
'docs_epi': "📸 **Hujjatlarni yuklang:**\n\n📄 Pasport\n📄 Tex-pasport\n📦 CMR\n📦 Invoice\n📜 Boshqa hujjatlar\n\n✅ Barcha rasmlarni yuklangandan so'ng **'Yuklab bo'ldim'** tugmasini bosing.",
'docs_mb': "📸 **Hujjatlarni yuklang:**\n\n📄 Pasport\n📄 Tex-pasport\n\n✅ Barcha rasmlarni yuklangandan so'ng **'Yuklab bo'ldim'** tugmasini bosing.",
'waiting_admin': "⏳ **Arizangiz adminlarga yuborildi!**\n\n🆔 Ariza kodi: `{code}`\n\nAdmin javobini kuting...",
'price_set': "✅ **Ariza tasdiqlandi!**\n\n💰 Narx: **{price} so'm**\n\nTo'lov turini tanlang:",
```

### 2. Ishonch telefonlari (5 kalit)

```python
'contacts_msg': "📞 **ISHONCH TELEFONLARI**\n\n📱 +998 91 702 00 99\n📱 +998 94 312 00 99\n\n📱 Telegram: @MYBOJXONA, @mybojxona1\n\n💬 WhatsApp: +998 91 702 00 99",
```

### 3. Narxlar katalogi (1 kalit)

```python
'prices_catalog': "📣 **MYBOJXONA: EPI-KOD xizmatlari narxlari**\n\nHurmatli mijozlar, EPI-KOD xizmatlari uchun belgilangan narxlar bilan tanishing:\n\n📦 **1-2 partiya:** 35 000 so'm\n📦 **3 partiya:** 45 000 so'm\n📦 **4 partiya:** 60 000 so'm\n📦 **5 partiya:** 75 000 so'm\n📦 **6 partiya:** 105 000 so'm\n📦 **7 partiya:** 126 000 so'm\n📦 **8 partiya:** 144 000 so'm\n\n🔄 **Boshqa holatlarda:** Har bir partiya uchun **20 000 so'mdan** hisoblanadi (X*20000).\n\n📞 **Ishonch telefonlari:**\n▪️ +998 94 312 00 99\n▪️ +998 91 702 00 99\n\n💎 **Sizning tangalaringiz hisobi:** {balance} ta tanga",
```

### 4. Arizalarim (5 kalit)

```python
'apps_menu': "🎫 **ARIZALARIM**\n\nTanlang:",
'search_app_car': "🔍 **ARIZA BOR**\n\nMashina raqamini kiriting:",
'app_found': "✅ **Ariza topildi!**\n\n🆔 Kod: `{code}`\n🚛 Mashina: {car}\n📅 Sana: {date}\n📊 Status: {status}",
'app_not_found': "❌ Bu mashina raqami bo'yicha ariza topilmadi.",
'my_apps_list': "📂 **SIZNING ARIZALARINGIZ:**\n\n{apps}",
'payment_methods': "💳 **To'lov turini tanlang:**",
```

### 5. Sozlamalar (5 kalit)

```python
'settings_menu': "⚙️ **SOZLAMALAR**\n\nTanlang:",
'change_phone_msg': "📱 **Raqamni o'zgartirish**\n\nYangi raqamingizni yuboring:",
'change_lang_msg': "🌐 **Tilni o'zgartirish**\n\nTilni tanlang:",
'clear_cache_msg': "🗑 **Xotirani tozalash**\n\nBarcha saqlangan hujjatlaringiz o'chiriladi. Davom etasizmi?",
'cache_cleared_msg': "✅ Xotira tozalandi!",
'admin_contact_msg': "👨‍💼 **ADMIN BILAN ALOQA**\n\n📞 Telefon: +998917020099, +998943120099\n📱 Telegram: @MYBOJXONA, @mybojxona1\n💬 WhatsApp: +998917020099",
```

### 6. Menyu tugmalari (17 kalit)

```python
'menu_epi': 'EPI KOD AT DEKLARATSIYA',
'menu_mb': 'MB DEKLARATSIYA',
'menu_contacts': 'ISHONCH TELEFONLARI',
'menu_apps': 'ARIZALARIM',
'menu_settings': 'SOZLAMALAR',
'menu_prices': 'NARXLAR KATALOGI',
'menu_app': 'DASTURNI YUKLAB OLING',
'menu_kgd': 'KGD(E-TRANZIT) KO\'RISH',
'menu_gabarit': 'GABARIT RUXSATNOMA OLISH',
'menu_sugurta': 'SUGURTA',
'menu_navbat': 'ELEKTRON NAVBAT',
'menu_yuklar': 'ISHONCHLI YUKLAR OLDI BERDI',
'menu_bonus': 'BOT ORQALI BONUS',
'menu_balance': 'TANGALARIM HISOBI',
'menu_social': 'SOCIAL MEDIA',
'menu_chat': 'GAPLASHISH',
```

### 7. Boshqa xizmatlar (15+ kalit)

```python
'app_download_msg': "📱 **DASTURNI YUKLAB OLING**\n\nTanlang:",
'app_link_msg': "🔗 **Dastur havolasi:**\n\n[Yuklab olish uchun bosing](https://example.com/download)",
'app_guide_msg': "📖 **Dasturdan foydalanish yo'riqnomasi:**\n\n1. Dasturni yuklab oling\n2. O'rnating\n3. Telefon raqamingiz bilan kiring",
'bonus_guide_msg': "🎁 **Bonus olish yo'riqnomasi:**\n\n👥 Do'stingiz ro'yxatdan o'tsa: **2,000 tanga**\n💰 Do'stingiz kod sotib olsa: **17,500 tanga**\n🎯 Maqsad: **35,000 tanga = 1 BEPUL EPI KOD**",
'kgd_menu_msg': "🚚 **KGD (E-TRANZIT) KO'RISH**\n\nUsulni tanlang:",
'kgd_app_msg': "📱 **Dastur orqali ko'rish:**\n\n[Dasturni yuklab olish](https://example.com/kgd)",
'kgd_staff_car': "👥 **Xodimlar orqali ko'rish**\n\nMashina raqamini kiriting:",
'kgd_checking': "🔍 Tekshirilmoqda... Bir oz kuting.",
'gabarit_msg': "📜 **GABARIT RUXSATNOMA OLISH**\n\nGabarit ruxsatnoma olish uchun admin bilan bog'laning:\n\n📱 @MYBOJXONA\n📱 @mybojxona1\n\n✍️ \"GABARIT\" deb yozing",
'coming_soon': "🚧 **TEZ KUNDA**\n\nBu xizmat tez orada ishga tushiriladi!",
'bonus_menu_msg': "🎁 **BOT ORQALI BONUS**\n\nTanlang:",
'get_referral_link': "🔗 **Sizning havolangiz:**\n\n`{link}`\n\nDo'stlaringizga yuboring va bonus yig'ing!\n\n👥 Ro'yxat: **+2,000 tanga**\n💰 Xarid: **+17,500 tanga**",
'bonus_info': "ℹ️ **BONUS TIZIMI HAQIDA:**\n\n🎁 Do'stlaringizni taklif qiling va tanga yig'ing!\n\n📊 Shartlar:\n👥 Do'st ro'yxatdan o'tsa: **2,000 tanga**\n💰 Do'st EPI kod olsa: **17,500 tanga**\n\n🎯 35,000 tanga = **1 BEPUL EPI KOD**",
'balance_msg': "💎 **TANGALARIM HISOBI**\n\n💰 Sizning balansingiz: **{balance} tanga**\n\n🎁 35,000 tanga = 1 BEPUL EPI KOD",
'social_msg': "📱 **SOCIAL MEDIA**\n\nBizni ijtimoiy tarmoqlarda kuzatib boring:",
'chat_msg': "💬 **GAPLASHISH**\n\nSavolingizni yozing, operator javob beradi:",
'chat_sent': "✅ Xabaringiz yuborildi! Javobni kutib turing.",
```

## 🚀 Qanday qo'shish kerak

1. `strings.py` faylini oching
2. Kerakli tilni toping (masalan, `'ru'` ruscha uchun)
3. Yuqoridagi kalit so'zlarni tarjima qilib qo'shing
4. Markdown formatini saqlang (`**qalin matn**`)

## ✅ Misol

```python
# O'zbekcha
'uz': {
    'epi_start': "📄 **EPI KOD AT DEKLARATSIYA**\n\nChegara bojxona postini tanlang:",
}

# Ruscha (tarjima kerak)
'ru': {
    'epi_start': "📄 **ДЕКЛАРАЦИЯ EPI КОД AT**\n\nВыберите пограничный пост:",
}
```

## 📊 Tarjima progress

| Til | Progress | Qolgan kalit so'zlar |
|-----|----------|---------------------|
| uz  | 100% ✅  | 0 |
| oz  | 60% ⚠️   | ~40 |
| ru  | 60% ⚠️   | ~40 |
| en  | 60% ⚠️   | ~40 |
| kz  | 40% ⚠️   | ~60 |
| kg  | 40% ⚠️   | ~60 |
| tj  | 40% ⚠️   | ~60 |
| tr  | 40% ⚠️   | ~60 |
| tm  | 40% ⚠️   | ~60 |
| zh  | 40% ⚠️   | ~60 |

---

**Eslatma:** Fallback mexanizm ishlaydi, shuning uchun bot hozir ham barcha tillarda ishlaydi. Lekin to'liq tarjima qilish foydalanuvchi tajribasini yaxshilaydi.
