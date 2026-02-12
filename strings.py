TEXTS = {
    # =================================================
    # 1. O'ZBEKCHA (LOTIN) - ASOSIY
    # =================================================
    'uz': {
        # Start
        'start': "🇺🇿 Iltimos, muloqot tilini tanlang:",
        'agreement': "⚠️ **Diqqat!**\nSizning ma'lumotlaringiz bojxona organlarida qayta ishlanishiga rozimisiz?",
        'ask_phone': "📱 Iltimos, pastdagi **'Raqamni yuborish'** tugmasini bosing:",
        'registered': "✅ **Muvaffaqiyatli ro'yxatdan o'tdingiz!**\nKerakli xizmat turini tanlang:",
        
        # Ariza jarayoni
        'enter_car': "🚛 Mashina raqamini yozing (Misol: 01A777AA):",
        
        # Auto-Fill (Eslab qolish)
        'autofill_found': "🤖 **Auto-Fill tizimi:**\n\nHurmatli haydovchi, **{car}** mashinasi uchun avvalgi hujjatlaringiz (Tex-pasport, Prava) bazada mavjud.\n\n**O'shalarni ishlataymi?** (Vaqtingiz tejaladi)",
        'autofill_used': "✅ **Eski hujjatlar yuklandi!**\n\nEndi faqat ushbu reysga tegishli yangi hujjatlarni (CMR, Yuk xati) rasmga olib tashlang.",
        
        # Hujjatlar
        'docs_header': "📸 **Hujjatlarni yuklash**\n\nQuyidagi hujjatlarni aniq qilib rasmga olib yuboring:",
        'docs_list_at': "📄 **Tex-pasport** (Oldi-Orqa)\n🪪 **Prava** (Oldi-Orqa)\n🚛 **Tirkama** (Tex-pasport)\n📦 **CMR va Invoice**\n📜 **Sertifikatlar**\n⚖️ **Notarial hujjatlar**",
        'docs_list_mb': "📄 **Tex-pasport** (Oldi-Orqa)\n🪪 **Prava** (Oldi-Orqa)",
        'docs_footer': "\n✅ Barcha rasmlarni tashlab bo'lgach, pastdagi **'Yuklab bo'ldim'** tugmasini bosing.",
        'zero_photos': "⚠️ Siz hali birorta rasm yuklamadingiz!",
        
        # Postlar
        'select_post': "🏢 **Kirish (Chegara)** postini tanlang:",
        'select_dest_post': "🏁 **Manzil (TIF)** postini tanlang:",
        'select_viloyat': "🗺 **Qaysi viloyatga borasiz?**\n\nViloyatni tanlang:",
        
        # Yakunlash
        'finish': "✅ **Arizangiz Adminga yuborildi!**\n\n🆔 ID: `{code}`\n📄 Rasmlar soni: {count} ta\n\n⏳ Admin javobini kuting...",
        
        # Sozlamalar va Yordam
        'settings_title': "⚙️ **Sozlamalar bo'limi:**\nMa'lumotlaringizni o'zgartirish yoki admin bilan bog'lanish uchun tanlang:",
        'cache_cleared': "✅ **Xotira tozalandi!**\nEndi bot eski hujjatlaringizni eslab qolmaydi.",
        'support_ask': "✍️ **Savolingiz yoki muammongizni yozib qoldiring:**\n\nBizning operatorlar tez orada javob berishadi.",
        'support_sent': "✅ **Xabaringiz adminga yuborildi!**\nJavobni shu yerda kutib oling.",
        'my_apps_empty': "📭 Sizda hali arizalar mavjud emas.",
        
        # Admin va To'lov
        'invoice_msg': "✅ **Arizangiz tasdiqlandi!**\n\n🆔 ID: `{code}`\n📦 Yuk hajmi: **{tier}**\n💰 To'lov summasi: **{amount} so'm**\n\nTo'lov usulini tanlang:",
        'admin_broadcast': "🔔 **YANGILIK (Admin):**\n\n{text}",
        
        # Tugmalar
        'btn_done': "Yuklab bo'ldim",
        'btn_yes_auto': "Ha, ishlatamiz",
        'btn_no_auto': "Yo'q, yangi yuklayman",
        'btn_lang': "Tilni o'zgartirish",
        'btn_phone': "Raqamni o'zgartirish",
        'btn_clear': "Xotirani tozalash",
        'btn_support': "Admin bilan aloqa",
        'btn_back': "Ortga",
        'btn_cancel': "Bekor qilish",
        'btn_change_phone': "RAQAMNI O'ZGARTIRISH",
        'btn_change_lang': "TILNI O'ZGARTIRISH",
        'btn_clear_cache': "XOTIRANI TOZALASH",
        'btn_admin_contact': "ADMIN BILAN ALOQA",
        'btn_search_app': "ARIZA BOR",
        'btn_my_apps': "ARIZALARIM",
        'btn_cash': "AGENTLAR ORQALI NAXD PULDA",
        
        # Bosqichlar
        'step_1': "1-qadam: Raqam", 'step_2': "2-qadam: Hujjatlar", 'step_3': "3-qadam: Post", 'step_4': "4-qadam: Manzil", 'step_5': "Yakunlash",

        # ===== YANGI QISMLAR =====

        # Asosiy menyu (17 ta xizmat)
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

        # EPI KOD va MB Deklaratsiya
        'epi_start': "📄 **EPI KOD AT DEKLARATSIYA**\n\nChegara bojxona postini tanlang:",
        'mb_start': "📋 **MB DEKLARATSIYA**\n\nChegara bojxona postini tanlang:",
        'select_agent': "👨‍💼 **Agent tanlash**\n\nQuyidagi agentlardan birini tanlang:",
        'enter_car_number': "🚛 **Mashina raqamini kiriting:**\n\n(Misol: 01A777AA)",
        'docs_epi': "📸 **Hujjatlarni yuklang:**\n\n📄 Pasport\n📄 Tex-pasport\n📦 CMR ; Invoice ; Packing list\n📜 Boshqa hujjatlar (Gabarit ruxsatnoma; Karantin ruxsatnoma; Fitosanitariya sertifikati; Sanitariya; Veterinariya)\n\n✅ Barcha rasmlarni yuklangandan so'ng **'Yuklab bo'ldim'** tugmasini bosing.",
        'docs_mb': "📸 **Hujjatlarni yuklang:**\n\n📄 Pasport\n📄 Tex-pasport\n\n✅ Barcha rasmlarni yuklangandan so'ng **'Yuklab bo'ldim'** tugmasini bosing.",
        'waiting_admin': "⏳ **Arizangiz adminlarga yuborildi!**\n\n🆔 Ariza kodi: `{code}`\n\nAdmin javobini kuting...",
        'price_set': "✅ **Ariza tasdiqlandi!**\n\n💰 Narx: **{price} so'm**\n\nTo'lov turini tanlang:",

        # Ishonch telefonlari
        'contacts_msg': "📞 **ISHONCH TELEFONLARI**\n\n📱 +998 91 702 00 99\n📱 +998 94 312 00 99\n\n📱 Telegram: @CARAVAN_TRANZIT, @caravan_tranzit1\n\n💬 WhatsApp: +998 91 702 00 99",

        # Narxlar katalogi
        'prices_catalog': "<b>🚛 CARAVAN TRANZIT — EPI-KOD XIZMATI</b>\n\nEPI-kod xizmatlari uchun tasdiqlangan narxlar ro'yxati:\n\n➖➖➖➖➖➖➖➖➖➖➖\n<b>📦 Kichik partiyalar:</b>\n▪️ <b>1-2 partiya:</b> 35 000 so'm\n▪️ <b>3 partiya:</b> 45 000 so'm\n\n<b>📈 Katta partiyalar:</b>\n▪️ <b>4 partiya:</b> 60 000 so'm\n▪️ <b>5 partiya:</b> 75 000 so'm\n▪️ <b>6 partiya:</b> 105 000 so'm\n▪️ <b>7 partiya:</b> 126 000 so'm\n▪️ <b>8 partiya:</b> 144 000 so'm\n▪️ <b>9 partiya:</b> 180 000 so'm\n➖➖➖➖➖➖➖➖➖➖➖\n\n<i>💡 To'lovlar milliy valyutada (UZS) qabul qilinadi.</i>\n\n<b>📞 Bog'lanish uchun:</b>\n+998 94 312 00 99\n+998 91 702 00 99\n\n🏢 <i>Caravan Broker MCHJ</i>",

        # Arizalarim
        'apps_menu': "🎫 **ARIZALARIM**\n\nTanlang:",
        'search_app_car': "🔍 **ARIZA BOR**\n\nMashina raqamini kiriting:",
        'app_found': "✅ **Ariza topildi!**\n\n🆔 Kod: `{code}`\n🚛 Mashina: {car}\n📅 Sana: {date}\n📊 Status: {status}",
        'app_not_found': "❌ Bu mashina raqami bo'yicha ariza topilmadi.",
        'my_apps_list': "📂 **SIZNING ARIZALARINGIZ:**\n\n{apps}",
        'payment_methods': "💳 **To'lov turini tanlang:**",

        # Sozlamalar
        'settings_menu': "⚙️ **SOZLAMALAR**\n\nTanlang:",
        'change_phone_msg': "📱 **Raqamni o'zgartirish**\n\nYangi raqamingizni yuboring:",
        'change_lang_msg': "🌐 **Tilni o'zgartirish**\n\nTilni tanlang:",
        'clear_cache_msg': "🗑 **Xotirani tozalash**\n\nBarcha saqlangan hujjatlaringiz o'chiriladi. Davom etasizmi?",
        'cache_cleared_msg': "✅ Xotira tozalandi!",
        'admin_contact_msg': "👨‍💼 **ADMIN BILAN ALOQA**\n\n📞 Telefon: +998917020099, +998943120099\n📱 Telegram: @CARAVAN_TRANZIT, @caravan_tranzit1\n💬 WhatsApp: +998917020099",

        # Narxlar katalogi
        'prices_msg': "💰 **NARXLAR KATALOGI**\n\nBarcha narxlarni ko'rish uchun quyidagi havolaga o'ting:\n\n🔗 https://taplink.at/en/profile/17507824/pages/",

        # Dasturni yuklab olish
        'app_download_msg': "📱 **DASTURNI YUKLAB OLING**\n\nTanlang:",
        'app_link_msg': "🔗 **Dastur havolasi:**\n\n[Yuklab olish uchun bosing](https://example.com/download)",
        'app_guide_msg': "📖 **Dasturdan foydalanish yo'riqnomasi:**\n\n1. Dasturni yuklab oling\n2. O'rnating\n3. Telefon raqamingiz bilan kiring",
        'bonus_guide_msg': "🎁 **Bonus olish yo'riqnomasi:**\n\n👥 Do'stingiz ro'yxatdan o'tsa: **2,000 tanga**\n💰 Do'stingiz kod sotib olsa: **17,500 tanga**\n🎯 Maqsad: **35,000 tanga = 1 BEPUL EPI KOD**",

        # KGD ko'rish
        'kgd_menu_msg': "🚚 **KGD (E-TRANZIT) KO'RISH**\n\nUsulni tanlang:",
        'kgd_app_msg': "📱 **Dastur orqali ko'rish:**\n\n[Dasturni yuklab olish](https://example.com/kgd)",
        'kgd_staff_car': "👥 **Xodimlar orqali ko'rish**\n\nMashina raqamini kiriting:",
        'kgd_checking': "🔍 Tekshirilmoqda... Bir oz kuting.",

        # Gabarit ruxsatnoma
        'gabarit_msg': "📜 **GABARIT RUXSATNOMA OLISH**\n\nGabarit ruxsatnoma olish uchun admin bilan bog'laning:\n\n📱 @CARAVAN_TRANZIT\n📱 @caravan_tranzit1\n\n✍️ \"GABARIT\" deb yozing",

        # Placeholder xizmatlar
        'coming_soon': "🚧 **TEZ KUNDA**\n\nBu xizmat tez orada ishga tushiriladi!",

        # Bonus tizimi
        'bonus_menu_msg': "🎁 **BOT ORQALI BONUS**\n\nTanlang:",
        'get_referral_link': "🔗 **Sizning havolangiz:**\n\n`{link}`\n\nDo'stlaringizga yuboring va bonus yig'ing!\n\n👥 Ro'yxat: **+2,000 tanga**\n💰 Xarid: **+17,500 tanga**",
        'bonus_info': "ℹ️ **BONUS TIZIMI HAQIDA:**\n\n🎁 Do'stlaringizni taklif qiling va tanga yig'ing!\n\n📊 Shartlar:\n👥 Do'st ro'yxatdan o'tsa: **2,000 tanga**\n💰 Do'st EPI kod olsa: **17,500 tanga**\n\n🎯 35,000 tanga = **1 BEPUL EPI KOD**",

        # Tangalar hisobi
        'balance_msg': "💎 **TANGALARIM HISOBI**\n\n💰 Sizning balansingiz: **{balance} tanga**\n\n🎁 35,000 tanga = 1 BEPUL EPI KOD",

        # Social media
        'social_msg': "📱 **SOCIAL MEDIA**\n\nBizni ijtimoiy tarmoqlarda kuzatib boring:",

        # Gaplashish
        'chat_msg': "💬 **GAPLASHISH**\n\nSavolingizni yozing, operator javob beradi:",
        'chat_sent': "✅ Xabaringiz yuborildi! Javobni kutib turing.",
        'chat_continue': "✅ Xabaringiz yuborildi! Yana yozishingiz mumkin yoki chatni tugating.",
        'chat_ended': "✅ Chat tugadi. Rahmat!",
        'btn_end_chat': "Chatni tugatish",

        # Button texts
        'btn_search_app': 'ARIZA BOR',
        'btn_my_apps': 'ARIZALARIM',
        'btn_cash': 'AGENTLAR ORQALI NAXD PULDA',
        'btn_change_phone': 'RAQAMNI O\'ZGARTIRISH',
        'btn_change_lang': 'TILNI O\'ZGARTIRISH',
        'btn_clear_cache': 'XOTIRANI TOZALASH',
        'btn_admin_contact': 'ADMIN BILAN ALOQA',
        'btn_app_link': 'DASTURNI YUKLAB OLING HAVOLA',
        'btn_app_guide': 'DASTURDAN FOYDALANISH YO\'RIQNOMASI',
        'btn_bonus_guide': 'DASTUR ORQALI BONUS OLISH YO\'RIQNOMASI',
        'btn_kgd_app': 'DASTUR ORQALI KO\'RISH',
        'btn_kgd_staff': 'XODIMLAR ORQALI KO\'RISH',
        'btn_download': 'Yuklab olish uchun havola',
        'btn_guide_use': 'Foydalanish bo\'yicha qo\'llanma',
        'btn_guide_kgd': 'KGD ko\'rish bo\'yicha qo\'llanma',
        'btn_bonus_rule': 'Bonus olish qoidasi',
        'btn_get_link': 'HAVOLANGIZNI OLING VA DO\'STLARINGIZGA YUBORING',
        'btn_bonus_info': 'QANDAY BONUS EKANLIGI HAQIDA TUSHUNTIRISHNOMA',
        'btn_my_coins': 'TANGALARIM',
    },

    # =================================================
    # 2. O'ZBEKCHA (KIRILL)
    # =================================================
    'oz': {
        'start': "🇺🇿 Илтимос, тилни танланг:",
        'agreement': "⚠️ **Диққат!**\nМаълумотларингиз божхона органларида қайта ишланишига розимисиз?",
        'ask_phone': "📱 Илтимос, пастдаги **'Рақамни юбориш'** тугмасини босинг:",
        'registered': "✅ **Муваффақиятли рўйхатдан ўтдингиз!**\nКеракли хизмат турини танланг:",
        'enter_car': "🚛 Машина рақамини ёзинг (Мисол: 01A777AA):",
        'autofill_found': "🤖 **Авто-Тўлдириш тизими:**\n\nҲурматли ҳайдовчи, **{car}** машинаси учун аввалги ҳужжатларингиз (Тех-паспорт, Права) базада мавжуд.\n\n**Ўшаларни ишлатайми?** (Вақтингиз тежалади)",
        'autofill_used': "✅ **Эски ҳужжатлар юкланди!**\n\nЭнди фақат ушбу рейсга тегишли янги ҳужжатларни (CMR, Юк хати) расмга олиб ташланг.",
        'docs_header': "📸 **Ҳужжатларни юклаш**\n\nҚуйидаги ҳужжатларни аниқ қилиб расмга олиб юборинг:",
        'docs_list_at': "📄 **Тех-паспорт** (Олди-Орқа)\n🪪 **Права** (Олди-Орқа)\n🚛 **Тиркама** (Тех-паспорт)\n📦 **CMR ва Инвойс**\n📜 **Сертификатлар**\n⚖️ **Нотариал ҳужжатлар**",
        'docs_list_mb': "📄 **Тех-паспорт** (Олди-Орқа)\n🪪 **Права** (Олди-Орқа)",
        'docs_footer': "\n✅ Барча расмларни ташлаб бўлгач, пастдаги **'Юклаб бўлдим'** тугмасини босинг.",
        'zero_photos': "⚠️ Сиз ҳали бирорта расм юкламадингиз!",
        'select_post': "🏢 **Кириш (Чегара)** постини танланг:",
        'select_dest_post': "🏁 **Манзил (ТИФ)** постини танланг:",
        'select_viloyat': "🗺 **Қайси вилоятга борасиз?**\n\nВилоятни танланг:",
        'finish': "✅ **Аризангиз Админга юборилди!**\n\n🆔 ID: `{code}`\n📄 Расмлар сони: {count} та\n\n⏳ Админ жавобини кутинг...",
        'settings_title': "⚙️ **Созламалар бўлими:**\nМаълумотларингизни ўзгартириш ёки админ билан боғланиш учун танланг:",
        'cache_cleared': "✅ **Хотира тозаланди!**\nЭнди бот эски ҳужжатларингизни эслаб қолмайди.",
        'support_ask': "✍️ **Саволингиз ёки муаммоингизни ёзиб қолдиринг:**\n\nБизнинг операторлар тез орада жавоб беришади.",
        'support_sent': "✅ **Хабарингиз админга юборилди!**\nЖавобни шу ерда кутиб олинг.",
        'my_apps_empty': "📭 Сизда ҳали аризалар мавжуд эмас.",
        'invoice_msg': "✅ **Аризангиз тасдиқланди!**\n\n🆔 ID: `{code}`\n📦 Юк ҳажми: **{tier}**\n💰 Тўлов суммаси: **{amount} сўм**\n\nТўлов усулини танланг:",
        'admin_broadcast': "🔔 **ЯНГИЛИК (Админ):**\n\n{text}",

        # Tugmalar
        'btn_done': "Юклаб бўлдим",
        'btn_yes_auto': "Ҳа, ишлатамиз",
        'btn_no_auto': "Йўқ, янги юклайман",
        'btn_lang': "Тилни ўзгартириш",
        'btn_phone': "Рақамни ўзгартириш",
        'btn_clear': "Хотирани тозалаш",
        'btn_support': "Админ билан алоқа",
        'btn_back': "Орқага",
        'btn_cancel': "Бекор қилиш",
        'btn_change_phone': "РАҚАМНИ ЎЗГАРТИРИШ",
        'btn_change_lang': "ТИЛНИ ЎЗГАРТИРИШ",
        'btn_clear_cache': "ХОТИРАНИ ТОЗАЛАШ",
        'btn_admin_contact': "АДМИН БИЛАН АЛОҚА",
        'btn_search_app': "АРИЗА БОР",
        'btn_my_apps': "АРИЗАЛАРИМ",
        'btn_cash': "АГЕНТЛАР ОРҚАЛИ НАҚД ПУЛДА",

        # Bosqichlar
        'step_1': "1-қадам: Рақам", 'step_2': "2-қадам: Ҳужжатлар", 'step_3': "3-қадам: Пост", 'step_4': "4-қадам: Манзил", 'step_5': "Якунлаш",

        # Asosiy menyu
        'menu_epi': 'ЭПИ КОД АТ ДЕКЛАРАЦИЯ',
        'menu_mb': 'МБ ДЕКЛАРАЦИЯ',
        'menu_contacts': 'ИШОНЧ ТЕЛЕФОНЛАРИ',
        'menu_apps': 'АРИЗАЛАРИМ',
        'menu_settings': 'СОЗЛАМАЛАР',
        'menu_prices': 'НАРХЛАР КАТАЛОГИ',
        'menu_app': 'ДАСТУРНИ ЮКЛАБ ОЛИНГ',
        'menu_kgd': 'КГД(Э-ТРАНЗИТ) КЎРИШ',
        'menu_gabarit': 'ГАБАРИТ РУХСАТНОМА ОЛИШ',
        'menu_sugurta': 'СУҒУРТА',
        'menu_navbat': 'ЭЛЕКТРОН НАВБАТ',
        'menu_yuklar': 'ИШОНЧЛИ ЮКЛАР ОЛДИ БЕРДИ',
        'menu_bonus': 'БОТ ОРҚАЛИ БОНУС',
        'menu_balance': 'ТАНГАЛАРИМ ҲИСОБИ',
        'menu_social': 'ИЖТИМОИЙ ТАРМОҚЛАР',
        'menu_chat': 'ГАПЛАШИШ',

        # EPI va MB
        'epi_start': "📄 **ЭПИ КОД АТ ДЕКЛАРАЦИЯ**\n\nЧегара божхона постини танланг:",
        'mb_start': "📋 **МБ ДЕКЛАРАЦИЯ**\n\nЧегара божхона постини танланг:",
        'select_agent': "👨‍💼 **Агент танлаш**\n\nҚуйидаги агентлардан бирини танланг:",
        'enter_car_number': "🚛 **Машина рақамини киритинг:**\n\n(Мисол: 01A777AA)",
        'docs_epi': "📸 **Ҳужжатларни юкланг:**\n\n📄 Паспорт\n📄 Тех-паспорт\n📦 CMR ; Инвойс ; Пакинг лист\n📜 Бошқа ҳужжатлар\n\n✅ Барча расмларни юклангандан сўнг **'Юклаб бўлдим'** тугмасини босинг.",
        'docs_mb': "📸 **Ҳужжатларни юкланг:**\n\n📄 Паспорт\n📄 Тех-паспорт\n\n✅ Барча расмларни юклангандан сўнг **'Юклаб бўлдим'** тугмасини босинг.",
        'waiting_admin': "⏳ **Аризангиз админларга юборилди!**\n\n🆔 Ариза коди: `{code}`\n\nАдмин жавобини кутинг...",
        'price_set': "✅ **Ариза тасдиқланди!**\n\n💰 Нарх: **{price} сўм**\n\nТўлов турини танланг:",

        # Ishonch telefonlari
        'contacts_msg': "📞 **ИШОНЧ ТЕЛЕФОНЛАРИ**\n\n📱 +998 91 702 00 99\n📱 +998 94 312 00 99\n\n📱 Telegram: @CARAVAN_TRANZIT, @caravan_tranzit1\n\n💬 WhatsApp: +998 91 702 00 99",

        # Narxlar
        'prices_catalog': "<b>🚛 CARAVAN TRANZIT — ЭПИ-КОД ХИЗМАТИ</b>\n\nЭПИ-код хизматлари учун тасдиқланган нархлар рўйхати:\n\n➖➖➖➖➖➖➖➖➖➖➖\n<b>📦 Кичик партиялар:</b>\n▪️ <b>1-2 партия:</b> 35 000 сўм\n▪️ <b>3 партия:</b> 45 000 сўм\n\n<b>📈 Катта партиялар:</b>\n▪️ <b>4 партия:</b> 60 000 сўм\n▪️ <b>5 партия:</b> 75 000 сўм\n▪️ <b>6 партия:</b> 105 000 сўм\n▪️ <b>7 партия:</b> 126 000 сўм\n▪️ <b>8 партия:</b> 144 000 сўм\n▪️ <b>9 партия:</b> 180 000 сўм\n➖➖➖➖➖➖➖➖➖➖➖",

        # Arizalarim
        'apps_menu': "🎫 **АРИЗАЛАРИМ**\n\nТанланг:",
        'search_app_car': "🔍 **АРИЗА БОР**\n\nМашина рақамини киритинг:",
        'app_found': "✅ **Ариза топилди!**\n\n🆔 Код: `{code}`\n🚛 Машина: {car}\n📅 Сана: {date}\n📊 Статус: {status}",
        'app_not_found': "❌ Бу машина рақами бўйича ариза топилмади.",
        'my_apps_list': "📂 **СИЗНИНГ АРИЗАЛАРИНГИЗ:**\n\n{apps}",
        'payment_methods': "💳 **Тўлов турини танланг:**",

        # Sozlamalar
        'settings_menu': "⚙️ **СОЗЛАМАЛАР**\n\nТанланг:",
        'change_phone_msg': "📱 **Рақамни ўзгартириш**\n\nЯнги рақамингизни юборинг:",
        'change_lang_msg': "🌐 **Тилни ўзгартириш**\n\nТилни танланг:",
        'clear_cache_msg': "🗑 **Хотирани тозалаш**\n\nБарча сақланган ҳужжатларингиз ўчирилади. Давом этасизми?",
        'cache_cleared_msg': "✅ Хотира тозаланди!",
        'admin_contact_msg': "👨‍💼 **АДМИН БИЛАН АЛОҚА**\n\n📞 Телефон: +998917020099, +998943120099\n📱 Telegram: @CARAVAN_TRANZIT, @caravan_tranzit1\n💬 WhatsApp: +998917020099",

        # Narxlar
        'prices_msg': "💰 **НАРХЛАР КАТАЛОГИ**\n\nБарча нархларни кўриш учун қуйидаги ҳаволага ўтинг:",

        # Dastur yuklab olish
        'app_download_msg': "📱 **ДАСТУРНИ ЮКЛАБ ОЛИНГ**\n\nТанланг:",
        'app_link_msg': "🔗 **Дастур ҳаволаси:**\n\nЮклаб олиш учун босинг",
        'app_guide_msg': "📖 **Дастурдан фойдаланиш йўриқномаси:**\n\n1. Дастурни юклаб олинг\n2. Ўрнатинг\n3. Телефон рақамингиз билан киринг",
        'bonus_guide_msg': "🎁 **Бонус олиш йўриқномаси:**\n\n👥 Дўстингиз рўйхатдан ўтса: **2,000 танга**\n💰 Дўстингиз код сотиб олса: **17,500 танга**\n🎯 Мақсад: **35,000 танга = 1 БЕПУЛ ЭПИ КОД**",

        # KGD
        'kgd_menu_msg': "🚚 **КГД (Э-ТРАНЗИТ) КЎРИШ**\n\nУсулни танланг:",
        'kgd_app_msg': "📱 **Дастур орқали кўриш:**",
        'kgd_staff_car': "👥 **Ходимлар орқали кўриш**\n\nМашина рақамини киритинг:",
        'kgd_checking': "🔍 Текширилмоқда... Бир оз кутинг.",

        # Gabarit
        'gabarit_msg': "📜 **ГАБАРИТ РУХСАТНОМА ОЛИШ**\n\nГабарит рухсатнома олиш учун админ билан боғланинг:\n\n📱 @CARAVAN_TRANZIT\n📱 @caravan_tranzit1\n\n✍️ \"ГАБАРИТ\" деб ёзинг",

        # Placeholder
        'coming_soon': "🚧 **ТЕЗ КУНДА**\n\nБу хизмат тез орада ишга туширилади!",

        # Bonus
        'bonus_menu_msg': "🎁 **БОТ ОРҚАЛИ БОНУС**\n\nТанланг:",
        'get_referral_link': "🔗 **Сизнинг ҳаволангиз:**\n\n`{link}`\n\nДўстларингизга юборинг ва бонус йиғинг!",
        'bonus_info': "ℹ️ **БОНУС ТИЗИМИ ҲАҚИДА:**\n\n🎁 Дўстларингизни таклиф қилинг ва танга йиғинг!\n\n👥 Дўст рўйхатдан ўтса: **2,000 танга**\n💰 Дўст ЭПИ код олса: **17,500 танга**\n\n🎯 35,000 танга = **1 БЕПУЛ ЭПИ КОД**",

        # Tangalar
        'balance_msg': "💎 **ТАНГАЛАРИМ ҲИСОБИ**\n\n💰 Сизнинг балансингиз: **{balance} танга**\n\n🎁 35,000 танга = 1 БЕПУЛ ЭПИ КОД",

        # Social
        'social_msg': "📱 **ИЖТИМОИЙ ТАРМОҚЛАР**\n\nБизни ижтимоий тармоқларда кузатиб боринг:",

        # Chat
        'chat_msg': "💬 **ГАПЛАШИШ**\n\nСаволингизни ёзинг, оператор жавоб беради:",
        'chat_sent': "✅ Хабарингиз юборилди! Жавобни кутиб туринг.",
        'chat_continue': "✅ Хабарингиз юборилди! Яна ёзишингиз мумкин ёки чатни тугатинг.",
        'chat_ended': "✅ Чат тугади. Раҳмат!",
        'btn_end_chat': "Чатни тугатиш",

        # Button texts
        'btn_app_link': 'ДАСТУРНИ ЮКЛАБ ОЛИНГ ҲАВОЛА',
        'btn_app_guide': 'ДАСТУРДАН ФОЙДАЛАНИШ ЙЎРИҚНОМАСИ',
        'btn_bonus_guide': 'ДАСТУР ОРҚАЛИ БОНУС ОЛИШ ЙЎРИҚНОМАСИ',
        'btn_kgd_app': 'ДАСТУР ОРҚАЛИ КЎРИШ',
        'btn_kgd_staff': 'ХОДИМЛАР ОРҚАЛИ КЎРИШ',
        'btn_download': 'Юклаб олиш учун ҳавола',
        'btn_guide_use': 'Фойдаланиш бўйича қўлланма',
        'btn_guide_kgd': 'КГД кўриш бўйича қўлланма',
        'btn_bonus_rule': 'Бонус олиш қоидаси',
        'btn_get_link': 'ҲАВОЛАНГИЗНИ ОЛИНГ ВА ДЎСТЛАРИНГИЗГА ЮБОРИНГ',
        'btn_bonus_info': 'ҚАНДАЙ БОНУС ЭКАНЛИГИ ҲАҚИДА ТУШУНТИРИШНОМА',
        'btn_my_coins': 'ТАНГАЛАРИМ',
    },

    # =================================================
    # 3. RUSCHA (РУССКИЙ)
    # =================================================
    'ru': {
        'start': "🇷🇺 Пожалуйста, выберите язык:",
        'agreement': "⚠️ **Внимание!**\nВы согласны на обработку данных таможенными органами?",
        'ask_phone': "📱 Пожалуйста, нажмите кнопку **'Отправить номер'**:",
        'registered': "✅ **Регистрация прошла успешно!**\nВыберите нужную услугу:",
        'enter_car': "🚛 Введите номер авто (Пример: 01A777AA):",
        'autofill_found': "🤖 **Автозаполнение:**\n\nУважаемый водитель, для машины **{car}** есть сохраненные документы (Техпаспорт, Права).\n\n**Использовать их?** (Это сэкономит время)",
        'autofill_used': "✅ **Старые документы загружены!**\n\nТеперь отправьте только новые документы рейса (CMR, Накладная).",
        'docs_header': "📸 **Загрузка документов**\n\nСфотографируйте и отправьте следующие документы:",
        'docs_list_at': "📄 **Техпаспорт** (Перед-Зад)\n🪪 **Права** (Перед-Зад)\n🚛 **Прицеп** (Техпаспорт)\n📦 **CMR и Инвойс**\n📜 **Сертификаты**\n⚖️ **Нотариальные док.**",
        'docs_list_mb': "📄 **Техпаспорт** (Перед-Зад)\n🪪 **Права** (Перед-Зад)",
        'docs_footer': "\n✅ После загрузки всех фото нажмите **'Загрузил'**.",
        'zero_photos': "⚠️ Вы еще не загрузили ни одного фото!",
        'select_post': "🏢 Выберите пост **Въезда (Граница)**:",
        'select_dest_post': "🏁 Выберите пост **Назначения (ТЭД)**:",
        'select_viloyat': "🗺 **В какую область едете?**\n\nВыберите область:",
        'finish': "✅ **Заявка отправлена админу!**\n\n🆔 ID: `{code}`\n📄 Фотографий: {count} шт\n\n⏳ Ждите ответа администратора...",
        'settings_title': "⚙️ **Раздел настроек:**\nВыберите для изменения данных или связи с админом:",
        'cache_cleared': "✅ **Память очищена!**\nТеперь бот не будет помнить старые документы.",
        'support_ask': "✍️ **Напишите ваш вопрос или проблему:**\n\nНаши операторы скоро ответят.",
        'support_sent': "✅ **Сообщение отправлено админу!**\nОжидайте ответ здесь.",
        'my_apps_empty': "📭 У вас пока нет заявок.",
        'invoice_msg': "✅ **Заявка подтверждена!**\n\n🆔 ID: `{code}`\n📦 Объем груза: **{tier}**\n💰 К оплате: **{amount} сум**\n\nВыберите способ оплаты:",
        'admin_broadcast': "🔔 **НОВОСТЬ (Админ):**\n\n{text}",

        # Кнопки
        'btn_done': "Загрузил",
        'btn_yes_auto': "Да, использовать",
        'btn_no_auto': "Нет, загружу новые",
        'btn_lang': "Изменить язык",
        'btn_phone': "Изменить номер",
        'btn_clear': "Очистить память",
        'btn_support': "Связь с админом",
        'btn_back': "Назад",
        'btn_cancel': "Отмена",
        'btn_change_phone': "ИЗМЕНИТЬ НОМЕР",
        'btn_change_lang': "ИЗМЕНИТЬ ЯЗЫК",
        'btn_clear_cache': "ОЧИСТИТЬ ПАМЯТЬ",
        'btn_admin_contact': "СВЯЗЬ С АДМИНОМ",
        'btn_search_app': "ПОИСК ЗАЯВКИ",
        'btn_my_apps': "МОИ ЗАЯВКИ",
        'btn_cash': "НАЛИЧНЫМИ ЧЕРЕЗ АГЕНТОВ",

        # Шаги
        'step_1': "Шаг 1: Номер", 'step_2': "Шаг 2: Документы", 'step_3': "Шаг 3: Пост", 'step_4': "Шаг 4: Пункт", 'step_5': "Завершение",

        # Главное меню
        'menu_epi': 'ЭПИ КОД АТ ДЕКЛАРАЦИЯ',
        'menu_mb': 'МБ ДЕКЛАРАЦИЯ',
        'menu_contacts': 'ДОВЕРИТЕЛЬНЫЕ ТЕЛЕФОНЫ',
        'menu_apps': 'МОИ ЗАЯВКИ',
        'menu_settings': 'НАСТРОЙКИ',
        'menu_prices': 'КАТАЛОГ ЦЕН',
        'menu_app': 'СКАЧАТЬ ПРИЛОЖЕНИЕ',
        'menu_kgd': 'КГД(Э-ТРАНЗИТ) ПРОСМОТР',
        'menu_gabarit': 'ПОЛУЧИТЬ ГАБАРИТНОЕ РАЗРЕШЕНИЕ',
        'menu_sugurta': 'СТРАХОВКА',
        'menu_navbat': 'ЭЛЕКТРОННАЯ ОЧЕРЕДЬ',
        'menu_yuklar': 'НАДЕЖНЫЕ ГРУЗЫ КУПЛЯ-ПРОДАЖА',
        'menu_bonus': 'БОНУС ЧЕРЕЗ БОТА',
        'menu_balance': 'МОИ МОНЕТЫ',
        'menu_social': 'СОЦИАЛЬНЫЕ СЕТИ',
        'menu_chat': 'ЧАТИТЬСЯ',

        # EPI и MB
        'epi_start': "📄 **ЭПИ КОД АТ ДЕКЛАРАЦИЯ**\n\nВыберите пограничный таможенный пост:",
        'mb_start': "📋 **МБ ДЕКЛАРАЦИЯ**\n\nВыберите пограничный таможенный пост:",
        'select_agent': "👨‍💼 **Выбор агента**\n\nВыберите одного из агентов:",
        'enter_car_number': "🚛 **Введите номер машины:**\n\n(Пример: 01A777AA)",
        'docs_epi': "📸 **Загрузите документы:**\n\n📄 Паспорт\n📄 Техпаспорт\n📦 CMR; Инвойс; Упаковочный лист\n📜 Другие документы\n\n✅ После загрузки нажмите **'Загрузил'**.",
        'docs_mb': "📸 **Загрузите документы:**\n\n📄 Паспорт\n📄 Техпаспорт\n\n✅ После загрузки нажмите **'Загрузил'**.",
        'waiting_admin': "⏳ **Заявка отправлена админам!**\n\n🆔 Код заявки: `{code}`\n\nОжидайте ответа...",
        'price_set': "✅ **Заявка подтверждена!**\n\n💰 Цена: **{price} сум**\n\nВыберите способ оплаты:",

        # Телефоны доверия
        'contacts_msg': "📞 **ДОВЕРИТЕЛЬНЫЕ ТЕЛЕФОНЫ**\n\n📱 +998 91 702 00 99\n📱 +998 94 312 00 99\n\n📱 Telegram: @CARAVAN_TRANZIT, @caravan_tranzit1\n\n💬 WhatsApp: +998 91 702 00 99",

        # Цены
        'prices_catalog': "<b>🚛 CARAVAN TRANZIT — УСЛУГА ЭПИ-КОД</b>\n\nУтвержденный прайс-лист:\n\n➖➖➖➖➖➖➖➖➖➖➖\n<b>📦 Малые партии:</b>\n▪️ <b>1-2 партии:</b> 35 000 сум\n▪️ <b>3 партии:</b> 45 000 сум\n\n<b>📈 Большие партии:</b>\n▪️ <b>4 партии:</b> 60 000 сум\n▪️ <b>5 партий:</b> 75 000 сум\n▪️ <b>6 партий:</b> 105 000 сум\n▪️ <b>7 партий:</b> 126 000 сум\n▪️ <b>8 партий:</b> 144 000 сум\n▪️ <b>9 партий:</b> 180 000 сум\n➖➖➖➖➖➖➖➖➖➖➖",

        # Мои заявки
        'apps_menu': "🎫 **МОИ ЗАЯВКИ**\n\nВыберите:",
        'search_app_car': "🔍 **ПОИСК ЗАЯВКИ**\n\nВведите номер машины:",
        'app_found': "✅ **Заявка найдена!**\n\n🆔 Код: `{code}`\n🚛 Машина: {car}\n📅 Дата: {date}\n📊 Статус: {status}",
        'app_not_found': "❌ Заявка по этому номеру не найдена.",
        'my_apps_list': "📂 **ВАШИ ЗАЯВКИ:**\n\n{apps}",
        'payment_methods': "💳 **Выберите способ оплаты:**",

        # Настройки
        'settings_menu': "⚙️ **НАСТРОЙКИ**\n\nВыберите:",
        'change_phone_msg': "📱 **Изменить номер**\n\nОтправьте новый номер:",
        'change_lang_msg': "🌐 **Изменить язык**\n\nВыберите язык:",
        'clear_cache_msg': "🗑 **Очистить память**\n\nВсе сохраненные документы будут удалены. Продолжить?",
        'cache_cleared_msg': "✅ Память очищена!",
        'admin_contact_msg': "👨‍💼 **СВЯЗЬ С АДМИНОМ**\n\n📞 Телефон: +998917020099, +998943120099\n📱 Telegram: @CARAVAN_TRANZIT, @caravan_tranzit1\n💬 WhatsApp: +998917020099",

        # Цены
        'prices_msg': "💰 **КАТАЛОГ ЦЕН**\n\nДля просмотра всех цен перейдите по ссылке:",

        # Скачать приложение
        'app_download_msg': "📱 **СКАЧАТЬ ПРИЛОЖЕНИЕ**\n\nВыберите:",
        'app_link_msg': "🔗 **Ссылка на приложение:**\n\nНажмите для скачивания",
        'app_guide_msg': "📖 **Инструкция по использованию:**\n\n1. Скачайте приложение\n2. Установите\n3. Войдите по номеру телефона",
        'bonus_guide_msg': "🎁 **Инструкция по бонусам:**\n\n👥 Друг регистрируется: **2,000 монет**\n💰 Друг покупает код: **17,500 монет**\n🎯 Цель: **35,000 монет = 1 БЕСПЛАТНЫЙ ЭПИ КОД**",

        # KGD
        'kgd_menu_msg': "🚚 **КГД (Э-ТРАНЗИТ) ПРОСМОТР**\n\nВыберите способ:",
        'kgd_app_msg': "📱 **Просмотр через приложение:**",
        'kgd_staff_car': "👥 **Просмотр через сотрудников**\n\nВведите номер машины:",
        'kgd_checking': "🔍 Проверяем... Подождите.",

        # Габарит
        'gabarit_msg': "📜 **ПОЛУЧИТЬ ГАБАРИТНОЕ РАЗРЕШЕНИЕ**\n\nДля получения свяжитесь с админом:\n\n📱 @CARAVAN_TRANZIT\n📱 @caravan_tranzit1\n\n✍️ Напишите \"ГАБАРИТ\"",

        # Placeholder
        'coming_soon': "🚧 **СКОРО**\n\nЭта услуга скоро будет доступна!",

        # Бонус
        'bonus_menu_msg': "🎁 **БОНУС ЧЕРЕЗ БОТА**\n\nВыберите:",
        'get_referral_link': "🔗 **Ваша ссылка:**\n\n`{link}`\n\nОтправьте друзьям и собирайте бонусы!",
        'bonus_info': "ℹ️ **О БОНУСНОЙ СИСТЕМЕ:**\n\n🎁 Приглашайте друзей и собирайте монеты!\n\n👥 Друг регистрируется: **2,000 монет**\n💰 Друг получает ЭПИ код: **17,500 монет**\n\n🎯 35,000 монет = **1 БЕСПЛАТНЫЙ ЭПИ КОД**",

        # Монеты
        'balance_msg': "💎 **МОИ МОНЕТЫ**\n\n💰 Ваш баланс: **{balance} монет**\n\n🎁 35,000 монет = 1 БЕСПЛАТНЫЙ ЭПИ КОД",

        # Соцсети
        'social_msg': "📱 **СОЦИАЛЬНЫЕ СЕТИ**\n\nСледите за нами в социальных сетях:",

        # Чат
        'chat_msg': "💬 **ЧАТИТЬСЯ**\n\nНапишите вопрос, оператор ответит:",
        'chat_sent': "✅ Сообщение отправлено! Ожидайте ответа.",
        'chat_continue': "✅ Сообщение отправлено! Можете продолжить писать или завершить чат.",
        'chat_ended': "✅ Чат завершён. Спасибо!",
        'btn_end_chat': "Завершить чат",

        # Тексты кнопок
        'btn_app_link': 'СКАЧАТЬ ПРИЛОЖЕНИЕ ССЫЛКА',
        'btn_app_guide': 'ИНСТРУКЦИЯ ПО ИСПОЛЬЗОВАНИЮ',
        'btn_bonus_guide': 'ИНСТРУКЦИЯ ПО БОНУСАМ',
        'btn_kgd_app': 'ПРОСМОТР ЧЕРЕЗ ПРИЛОЖЕНИЕ',
        'btn_kgd_staff': 'ПРОСМОТР ЧЕРЕЗ СОТРУДНИКОВ',
        'btn_download': 'Ссылка для скачивания',
        'btn_guide_use': 'Руководство по использованию',
        'btn_guide_kgd': 'Руководство по просмотру КГД',
        'btn_bonus_rule': 'Правила получения бонуса',
        'btn_get_link': 'ПОЛУЧИТЕ ССЫЛКУ И ОТПРАВЬТЕ ДРУЗЬЯМ',
        'btn_bonus_info': 'ОПИСАНИЕ БОНУСНОЙ СИСТЕМЫ',
        'btn_my_coins': 'МОИ МОНЕТЫ',
    },

    # =================================================
    # 4. INGLIZCHA (ENGLISH)
    # =================================================
    'en': {
        'start': "🇺🇸 Please select your language:",
        'agreement': "⚠️ **Attention!**\nDo you agree to your data being processed by customs authorities?",
        'ask_phone': "📱 Please click the **'Send Number'** button below:",
        'registered': "✅ **Registration successful!**\nChoose the service you need:",
        'enter_car': "🚛 Enter vehicle number (Ex: 01A777AA):",
        'autofill_found': "🤖 **Auto-Fill System:**\n\nDear driver, saved documents found for **{car}** (Tech Passport, License).\n\n**Use them?** (Saves your time)",
        'autofill_used': "✅ **Saved documents loaded!**\n\nNow upload only new shipment documents (CMR, Waybill).",
        'docs_header': "📸 **Upload Documents**\n\nPlease take clear photos of the following documents:",
        'docs_list_at': "📄 **Tech Passport** (Front-Back)\n🪪 **License** (Front-Back)\n🚛 **Trailer** (Tech Passport)\n📦 **CMR & Invoice**\n📜 **Certificates**\n⚖️ **Notarized Documents**",
        'docs_list_mb': "📄 **Tech Passport** (Front-Back)\n🪪 **License** (Front-Back)",
        'docs_footer': "\n✅ After uploading all photos, click **'Done'**.",
        'zero_photos': "⚠️ You haven't uploaded any photos yet!",
        'select_post': "🏢 Select **Entry (Border)** Post:",
        'select_dest_post': "🏁 Select **Destination (TED)** Post:",
        'select_viloyat': "🗺 **Which region are you going to?**\n\nSelect a region:",
        'finish': "✅ **Application sent to Admin!**\n\n🆔 ID: `{code}`\n📄 Photos: {count}\n\n⏳ Wait for admin reply...",
        'settings_title': "⚙️ **Settings Section:**\nSelect to change your information or contact admin:",
        'cache_cleared': "✅ **Cache cleared!**\nThe bot will no longer remember your old documents.",
        'support_ask': "✍️ **Write your question or problem:**\n\nOur operators will respond soon.",
        'support_sent': "✅ **Message sent to admin!**\nWait for the response here.",
        'my_apps_empty': "📭 You don't have any applications yet.",
        'invoice_msg': "✅ **Application Approved!**\n\n🆔 ID: `{code}`\n📦 Cargo Volume: **{tier}**\n💰 Amount: **{amount} UZS**\n\nSelect payment method:",
        'admin_broadcast': "🔔 **NOTIFICATION:**\n\n{text}",

        # Buttons
        'btn_done': "Done",
        'btn_yes_auto': "Yes, use saved",
        'btn_no_auto': "No, upload new",
        'btn_lang': "Change Language",
        'btn_phone': "Change Number",
        'btn_clear': "Clear Cache",
        'btn_support': "Contact Admin",
        'btn_back': "Back",
        'btn_cancel': "Cancel",
        'btn_change_phone': "CHANGE NUMBER",
        'btn_change_lang': "CHANGE LANGUAGE",
        'btn_clear_cache': "CLEAR CACHE",
        'btn_admin_contact': "CONTACT ADMIN",
        'btn_search_app': "SEARCH APPLICATION",
        'btn_my_apps': "MY APPLICATIONS",
        'btn_cash': "CASH VIA AGENTS",

        # Steps
        'step_1': "Step 1: Number", 'step_2': "Step 2: Documents", 'step_3': "Step 3: Post", 'step_4': "Step 4: Destination", 'step_5': "Finish",

        # Main menu
        'menu_epi': 'EPI CODE AT DECLARATION',
        'menu_mb': 'MB DECLARATION',
        'menu_contacts': 'TRUST PHONES',
        'menu_apps': 'MY APPLICATIONS',
        'menu_settings': 'SETTINGS',
        'menu_prices': 'PRICE CATALOG',
        'menu_app': 'DOWNLOAD APP',
        'menu_kgd': 'KGD(E-TRANSIT) VIEW',
        'menu_gabarit': 'GET OVERSIZE PERMIT',
        'menu_sugurta': 'INSURANCE',
        'menu_navbat': 'ELECTRONIC QUEUE',
        'menu_yuklar': 'TRUSTED CARGO BUY-SELL',
        'menu_bonus': 'BOT BONUS',
        'menu_balance': 'MY COINS',
        'menu_social': 'SOCIAL MEDIA',
        'menu_chat': 'CHAT',

        # EPI and MB
        'epi_start': "📄 **EPI CODE AT DECLARATION**\n\nSelect border customs post:",
        'mb_start': "📋 **MB DECLARATION**\n\nSelect border customs post:",
        'select_agent': "👨‍💼 **Select Agent**\n\nChoose one of the agents:",
        'enter_car_number': "🚛 **Enter vehicle number:**\n\n(Example: 01A777AA)",
        'docs_epi': "📸 **Upload documents:**\n\n📄 Passport\n📄 Tech Passport\n📦 CMR; Invoice; Packing list\n📜 Other documents\n\n✅ After uploading click **'Done'**.",
        'docs_mb': "📸 **Upload documents:**\n\n📄 Passport\n📄 Tech Passport\n\n✅ After uploading click **'Done'**.",
        'waiting_admin': "⏳ **Application sent to admins!**\n\n🆔 Application code: `{code}`\n\nWait for admin response...",
        'price_set': "✅ **Application confirmed!**\n\n💰 Price: **{price} UZS**\n\nSelect payment type:",

        # Trust phones
        'contacts_msg': "📞 **TRUST PHONES**\n\n📱 +998 91 702 00 99\n📱 +998 94 312 00 99\n\n📱 Telegram: @CARAVAN_TRANZIT, @caravan_tranzit1\n\n💬 WhatsApp: +998 91 702 00 99",

        # Prices
        'prices_catalog': "<b>🚛 CARAVAN TRANZIT — EPI-CODE SERVICE</b>\n\nApproved price list:\n\n➖➖➖➖➖➖➖➖➖➖➖\n<b>📦 Small batches:</b>\n▪️ <b>1-2 batches:</b> 35,000 UZS\n▪️ <b>3 batches:</b> 45,000 UZS\n\n<b>📈 Large batches:</b>\n▪️ <b>4 batches:</b> 60,000 UZS\n▪️ <b>5 batches:</b> 75,000 UZS\n▪️ <b>6 batches:</b> 105,000 UZS\n▪️ <b>7 batches:</b> 126,000 UZS\n▪️ <b>8 batches:</b> 144,000 UZS\n▪️ <b>9 batches:</b> 180,000 UZS\n➖➖➖➖➖➖➖➖➖➖➖",

        # My applications
        'apps_menu': "🎫 **MY APPLICATIONS**\n\nSelect:",
        'search_app_car': "🔍 **SEARCH APPLICATION**\n\nEnter vehicle number:",
        'app_found': "✅ **Application found!**\n\n🆔 Code: `{code}`\n🚛 Vehicle: {car}\n📅 Date: {date}\n📊 Status: {status}",
        'app_not_found': "❌ No application found for this vehicle number.",
        'my_apps_list': "📂 **YOUR APPLICATIONS:**\n\n{apps}",
        'payment_methods': "💳 **Select payment method:**",

        # Settings
        'settings_menu': "⚙️ **SETTINGS**\n\nSelect:",
        'change_phone_msg': "📱 **Change Number**\n\nSend your new number:",
        'change_lang_msg': "🌐 **Change Language**\n\nSelect language:",
        'clear_cache_msg': "🗑 **Clear Cache**\n\nAll saved documents will be deleted. Continue?",
        'cache_cleared_msg': "✅ Cache cleared!",
        'admin_contact_msg': "👨‍💼 **CONTACT ADMIN**\n\n📞 Phone: +998917020099, +998943120099\n📱 Telegram: @CARAVAN_TRANZIT, @caravan_tranzit1\n💬 WhatsApp: +998917020099",

        # Prices
        'prices_msg': "💰 **PRICE CATALOG**\n\nGo to the following link to view all prices:",

        # Download app
        'app_download_msg': "📱 **DOWNLOAD APP**\n\nSelect:",
        'app_link_msg': "🔗 **App link:**\n\nClick to download",
        'app_guide_msg': "📖 **Usage guide:**\n\n1. Download the app\n2. Install it\n3. Log in with your phone number",
        'bonus_guide_msg': "🎁 **Bonus guide:**\n\n👥 Friend registers: **2,000 coins**\n💰 Friend buys code: **17,500 coins**\n🎯 Goal: **35,000 coins = 1 FREE EPI CODE**",

        # KGD
        'kgd_menu_msg': "🚚 **KGD (E-TRANSIT) VIEW**\n\nSelect method:",
        'kgd_app_msg': "📱 **View via app:**",
        'kgd_staff_car': "👥 **View via staff**\n\nEnter vehicle number:",
        'kgd_checking': "🔍 Checking... Please wait.",

        # Oversize
        'gabarit_msg': "📜 **GET OVERSIZE PERMIT**\n\nContact admin to get permit:\n\n📱 @CARAVAN_TRANZIT\n📱 @caravan_tranzit1\n\n✍️ Write \"OVERSIZE\"",

        # Placeholder
        'coming_soon': "🚧 **COMING SOON**\n\nThis service will be available soon!",

        # Bonus
        'bonus_menu_msg': "🎁 **BOT BONUS**\n\nSelect:",
        'get_referral_link': "🔗 **Your link:**\n\n`{link}`\n\nSend to friends and collect bonuses!",
        'bonus_info': "ℹ️ **ABOUT BONUS SYSTEM:**\n\n🎁 Invite friends and collect coins!\n\n👥 Friend registers: **2,000 coins**\n💰 Friend gets EPI code: **17,500 coins**\n\n🎯 35,000 coins = **1 FREE EPI CODE**",

        # Coins
        'balance_msg': "💎 **MY COINS**\n\n💰 Your balance: **{balance} coins**\n\n🎁 35,000 coins = 1 FREE EPI CODE",

        # Social
        'social_msg': "📱 **SOCIAL MEDIA**\n\nFollow us on social media:",

        # Chat
        'chat_msg': "💬 **CHAT**\n\nWrite your question, operator will respond:",
        'chat_sent': "✅ Message sent! Wait for response.",
        'chat_continue': "✅ Message sent! You can continue writing or end the chat.",
        'chat_ended': "✅ Chat ended. Thank you!",
        'btn_end_chat': "End chat",

        # Button texts
        'btn_app_link': 'DOWNLOAD APP LINK',
        'btn_app_guide': 'APP USAGE GUIDE',
        'btn_bonus_guide': 'BONUS GUIDE VIA APP',
        'btn_kgd_app': 'VIEW VIA APP',
        'btn_kgd_staff': 'VIEW VIA STAFF',
        'btn_download': 'Download link',
        'btn_guide_use': 'Usage guide',
        'btn_guide_kgd': 'KGD viewing guide',
        'btn_bonus_rule': 'Bonus rules',
        'btn_get_link': 'GET YOUR LINK AND SEND TO FRIENDS',
        'btn_bonus_info': 'ABOUT BONUS SYSTEM',
        'btn_my_coins': 'MY COINS',
    },

    # =================================================
    # 5. QOZOQCHA (QAZAQ)
    # =================================================
    'kz': {
        'start': "🇰🇿 Тілді таңдаңыз:",
        'agreement': "⚠️ **Назар аударыңыз!**\nСіздің деректеріңізді кеден органдары өңдеуге келісесіз бе?",
        'ask_phone': "📱 Төмендегі **'Нөмірді жіберу'** түймесін басыңыз:",
        'registered': "✅ **Сәтті тіркелдіңіз!**\nҚажетті қызметті таңдаңыз:",
        'enter_car': "🚛 Көлік нөмірін енгізіңіз (Мысалы: 01A777AA):",
        'autofill_found': "🤖 **Авто-Толтыру жүйесі:**\n\nҚұрметті жүргізуші, **{car}** көлігі үшін ескі құжаттарыңыз (Тех-паспорт, Куәлік) базада бар.\n\n**Қолданамыз ба?** (Уақыт үнемдейсіз)",
        'autofill_used': "✅ **Ескі құжаттар жүктелді!**\n\nЕнді тек осы рейстің жаңа құжаттарын (CMR, Жүк қағазы) жіберіңіз.",
        'docs_header': "📸 **Құжаттарды жүктеу**\n\nТөмендегі құжаттарды анық түсіріп жіберіңіз:",
        'docs_list_at': "📄 **Тех-паспорт** (Алды-Арты)\n🪪 **Куәлік** (Алды-Арты)\n🚛 **Тіркеме** (Тех-паспорт)\n📦 **CMR және Инвойс**\n📜 **Сертификаттар**\n⚖️ **Нотариалды құжаттар**",
        'docs_list_mb': "📄 **Тех-паспорт** (Алды-Арты)\n🪪 **Куәлік** (Алды-Арты)",
        'docs_footer': "\n✅ Барлық фотоларды жүктегеннен кейін **'Болды'** батырмасын басыңыз.",
        'zero_photos': "⚠️ Сіз әлі бірде-бір фото жүктемедіңіз!",
        'select_post': "🏢 **Кіру (Шекара)** бекетін таңдаңыз:",
        'select_dest_post': "🏁 **Баратын жер (ТЭҚ)** бекетін таңдаңыз:",
        'select_viloyat': "🗺 **Қай облысқа барасыз?**\n\nОблысты таңдаңыз:",
        'finish': "✅ **Өтінішіңіз Админге жіберілді!**\n\n🆔 ID: `{code}`\n📄 Фотолар саны: {count}\n\n⏳ Админ жауабын күтіңіз...",
        'settings_title': "⚙️ **Баптаулар бөлімі:**\nМәліметтеріңізді өзгерту немесе админмен байланысу үшін таңдаңыз:",
        'cache_cleared': "✅ **Жады тазаланды!**\nЕнді бот ескі құжаттарыңызды есте сақтамайды.",
        'support_ask': "✍️ **Сұрағыңызды немесе мәселеңізді жазыңыз:**\n\nБіздің операторлар жақын арада жауап береді.",
        'support_sent': "✅ **Хабарыңыз админге жіберілді!**\nЖауапты осында күтіңіз.",
        'my_apps_empty': "📭 Сізде әлі өтініштер жоқ.",
        'invoice_msg': "✅ **Өтінішіңіз расталды!**\n\n🆔 ID: `{code}`\n📦 Жүк көлемі: **{tier}**\n💰 Төлем сомасы: **{amount} сум**\n\nТөлем әдісін таңдаңыз:",
        'admin_broadcast': "🔔 **ЖАҢАЛЫҚ (Админ):**\n\n{text}",

        # Батырмалар
        'btn_done': "Болды",
        'btn_yes_auto': "Иә, қолданамыз",
        'btn_no_auto': "Жоқ, жаңасын жүктеймін",
        'btn_lang': "Тілді өзгерту",
        'btn_phone': "Нөмірді өзгерту",
        'btn_clear': "Жадыны тазалау",
        'btn_support': "Админмен байланыс",
        'btn_back': "Артқа",
        'btn_cancel': "Бас тарту",
        'btn_change_phone': "НӨМІРДІ ӨЗГЕРТУ",
        'btn_change_lang': "ТІЛДІ ӨЗГЕРТУ",
        'btn_clear_cache': "ЖАДЫНЫ ТАЗАЛАУ",
        'btn_admin_contact': "АДМИНМЕН БАЙЛАНЫС",
        'btn_search_app': "ӨТІНІШ БАР",
        'btn_my_apps': "ӨТІНІШТЕРІМ",
        'btn_cash': "АГЕНТТЕР АРҚЫЛЫ ҚОЛМА-ҚОЛ",

        # Қадамдар
        'step_1': "1-қадам: Нөмір", 'step_2': "2-қадам: Құжаттар", 'step_3': "3-қадам: Бекет", 'step_4': "4-қадам: Баратын жер", 'step_5': "Аяқтау",

        # Негізгі мәзір
        'menu_epi': 'ЭПИ КОД АТ ДЕКЛАРАЦИЯ',
        'menu_mb': 'МБ ДЕКЛАРАЦИЯ',
        'menu_contacts': 'СЕНІМ ТЕЛЕФОНДАРЫ',
        'menu_apps': 'ӨТІНІШТЕРІМ',
        'menu_settings': 'БАПТАУЛАР',
        'menu_prices': 'БАҒАЛАР КАТАЛОГЫ',
        'menu_app': 'ҚОСЫМШАНЫ ЖҮКТЕУ',
        'menu_kgd': 'КГД(Э-ТРАНЗИТ) КӨРУ',
        'menu_gabarit': 'ГАБАРИТ РҰҚСАТ АЛУ',
        'menu_sugurta': 'САҚТАНДЫРУ',
        'menu_navbat': 'ЭЛЕКТРОНДЫ КЕЗЕК',
        'menu_yuklar': 'СЕНІМДІ ЖҮКТЕР САТУ-АЛЫМ',
        'menu_bonus': 'БОТ АРҚЫЛЫ БОНУС',
        'menu_balance': 'ТИЫНДАРЫМ ЕСЕБІ',
        'menu_social': 'ӘЛЕУМЕТТІК ЖЕЛІЛЕР',
        'menu_chat': 'СӨЙЛЕСУ',

        # EPI және MB
        'epi_start': "📄 **ЭПИ КОД АТ ДЕКЛАРАЦИЯ**\n\nШекара кеден бекетін таңдаңыз:",
        'mb_start': "📋 **МБ ДЕКЛАРАЦИЯ**\n\nШекара кеден бекетін таңдаңыз:",
        'select_agent': "👨‍💼 **Агент таңдау**\n\nАгенттердің бірін таңдаңыз:",
        'enter_car_number': "🚛 **Көлік нөмірін енгізіңіз:**\n\n(Мысалы: 01A777AA)",
        'docs_epi': "📸 **Құжаттарды жүктеңіз:**\n\n📄 Паспорт\n📄 Тех-паспорт\n📦 CMR; Инвойс; Орама тізімі\n📜 Басқа құжаттар\n\n✅ Жүктегеннен кейін **'Болды'** басыңыз.",
        'docs_mb': "📸 **Құжаттарды жүктеңіз:**\n\n📄 Паспорт\n📄 Тех-паспорт\n\n✅ Жүктегеннен кейін **'Болды'** басыңыз.",
        'waiting_admin': "⏳ **Өтінішіңіз админдерге жіберілді!**\n\n🆔 Өтініш коды: `{code}`\n\nАдмин жауабын күтіңіз...",
        'price_set': "✅ **Өтініш расталды!**\n\n💰 Бағасы: **{price} сум**\n\nТөлем түрін таңдаңыз:",

        # Сенім телефондары
        'contacts_msg': "📞 **СЕНІМ ТЕЛЕФОНДАРЫ**\n\n📱 +998 91 702 00 99\n📱 +998 94 312 00 99\n\n📱 Telegram: @CARAVAN_TRANZIT, @caravan_tranzit1\n\n💬 WhatsApp: +998 91 702 00 99",

        # Бағалар
        'prices_catalog': "<b>🚛 CARAVAN TRANZIT — ЭПИ-КОД ҚЫЗМЕТІ</b>\n\nБекітілген баға тізімі:\n\n➖➖➖➖➖➖➖➖➖➖➖\n<b>📦 Шағын партиялар:</b>\n▪️ <b>1-2 партия:</b> 35 000 сум\n▪️ <b>3 партия:</b> 45 000 сум\n\n<b>📈 Үлкен партиялар:</b>\n▪️ <b>4 партия:</b> 60 000 сум\n▪️ <b>5 партия:</b> 75 000 сум\n▪️ <b>6 партия:</b> 105 000 сум\n▪️ <b>7 партия:</b> 126 000 сум\n▪️ <b>8 партия:</b> 144 000 сум\n▪️ <b>9 партия:</b> 180 000 сум\n➖➖➖➖➖➖➖➖➖➖➖",

        # Өтініштерім
        'apps_menu': "🎫 **ӨТІНІШТЕРІМ**\n\nТаңдаңыз:",
        'search_app_car': "🔍 **ӨТІНІШ ІЗДЕУ**\n\nКөлік нөмірін енгізіңіз:",
        'app_found': "✅ **Өтініш табылды!**\n\n🆔 Код: `{code}`\n🚛 Көлік: {car}\n📅 Күні: {date}\n📊 Күйі: {status}",
        'app_not_found': "❌ Бұл көлік нөмірі бойынша өтініш табылмады.",
        'my_apps_list': "📂 **СІЗДІҢ ӨТІНІШТЕРІҢІЗ:**\n\n{apps}",
        'payment_methods': "💳 **Төлем әдісін таңдаңыз:**",

        # Баптаулар
        'settings_menu': "⚙️ **БАПТАУЛАР**\n\nТаңдаңыз:",
        'change_phone_msg': "📱 **Нөмірді өзгерту**\n\nЖаңа нөміріңізді жіберіңіз:",
        'change_lang_msg': "🌐 **Тілді өзгерту**\n\nТілді таңдаңыз:",
        'clear_cache_msg': "🗑 **Жадыны тазалау**\n\nБарлық сақталған құжаттарыңыз жойылады. Жалғастырасыз ба?",
        'cache_cleared_msg': "✅ Жады тазаланды!",
        'admin_contact_msg': "👨‍💼 **АДМИНМЕН БАЙЛАНЫС**\n\n📞 Телефон: +998917020099, +998943120099\n📱 Telegram: @CARAVAN_TRANZIT, @caravan_tranzit1\n💬 WhatsApp: +998917020099",

        # Бағалар
        'prices_msg': "💰 **БАҒАЛАР КАТАЛОГЫ**\n\nБарлық бағаларды көру үшін сілтемеге өтіңіз:",

        # Қосымшаны жүктеу
        'app_download_msg': "📱 **ҚОСЫМШАНЫ ЖҮКТЕУ**\n\nТаңдаңыз:",
        'app_link_msg': "🔗 **Қосымша сілтемесі:**\n\nЖүктеу үшін басыңыз",
        'app_guide_msg': "📖 **Пайдалану нұсқаулығы:**\n\n1. Қосымшаны жүктеңіз\n2. Орнатыңыз\n3. Телефон нөміріңізбен кіріңіз",
        'bonus_guide_msg': "🎁 **Бонус алу нұсқаулығы:**\n\n👥 Достыңыз тіркелсе: **2,000 тиын**\n💰 Достыңыз код сатып алса: **17,500 тиын**\n🎯 Мақсат: **35,000 тиын = 1 ТЕГІН ЭПИ КОД**",

        # KGD
        'kgd_menu_msg': "🚚 **КГД (Э-ТРАНЗИТ) КӨРУ**\n\nӘдісті таңдаңыз:",
        'kgd_app_msg': "📱 **Қосымша арқылы көру:**",
        'kgd_staff_car': "👥 **Қызметкерлер арқылы көру**\n\nКөлік нөмірін енгізіңіз:",
        'kgd_checking': "🔍 Тексерілуде... Күте тұрыңыз.",

        # Габарит
        'gabarit_msg': "📜 **ГАБАРИТ РҰҚСАТ АЛУ**\n\nРұқсат алу үшін админмен байланысыңыз:\n\n📱 @CARAVAN_TRANZIT\n📱 @caravan_tranzit1\n\n✍️ \"ГАБАРИТ\" деп жазыңыз",

        # Placeholder
        'coming_soon': "🚧 **ЖАҚЫНДА**\n\nБұл қызмет жақында іске қосылады!",

        # Бонус
        'bonus_menu_msg': "🎁 **БОТ АРҚЫЛЫ БОНУС**\n\nТаңдаңыз:",
        'get_referral_link': "🔗 **Сіздің сілтемеңіз:**\n\n`{link}`\n\nДостарыңызға жіберіңіз және бонус жинаңыз!",
        'bonus_info': "ℹ️ **БОНУС ЖҮЙЕСІ ТУРАЛЫ:**\n\n🎁 Достарыңызды шақырыңыз және тиын жинаңыз!\n\n👥 Дос тіркелсе: **2,000 тиын**\n💰 Дос ЭПИ код алса: **17,500 тиын**\n\n🎯 35,000 тиын = **1 ТЕГІН ЭПИ КОД**",

        # Тиындар
        'balance_msg': "💎 **ТИЫНДАРЫМ ЕСЕБІ**\n\n💰 Сіздің балансыңыз: **{balance} тиын**\n\n🎁 35,000 тиын = 1 ТЕГІН ЭПИ КОД",

        # Әлеуметтік
        'social_msg': "📱 **ӘЛЕУМЕТТІК ЖЕЛІЛЕР**\n\nБізді әлеуметтік желілерде қадағалаңыз:",

        # Чат
        'chat_msg': "💬 **СӨЙЛЕСУ**\n\nСұрағыңызды жазыңыз, оператор жауап береді:",
        'chat_sent': "✅ Хабарыңыз жіберілді! Жауапты күтіңіз.",
        'chat_continue': "✅ Хабарыңыз жіберілді! Жазуды жалғастыра аласыз немесе чатты аяқтаңыз.",
        'chat_ended': "✅ Чат аяқталды. Рахмет!",
        'btn_end_chat': "Чатты аяқтау",

        # Батырма мәтіндері
        'btn_app_link': 'ҚОСЫМШАНЫ ЖҮКТЕУ СІЛТЕМЕСІ',
        'btn_app_guide': 'ПАЙДАЛАНУ НҰСҚАУЛЫҒЫ',
        'btn_bonus_guide': 'ҚОСЫМША АРҚЫЛЫ БОНУС АЛУ НҰСҚАУЛЫҒЫ',
        'btn_kgd_app': 'ҚОСЫМША АРҚЫЛЫ КӨРУ',
        'btn_kgd_staff': 'ҚЫЗМЕТКЕРЛЕР АРҚЫЛЫ КӨРУ',
        'btn_download': 'Жүктеу сілтемесі',
        'btn_guide_use': 'Пайдалану бойынша нұсқаулық',
        'btn_guide_kgd': 'КГД көру бойынша нұсқаулық',
        'btn_bonus_rule': 'Бонус алу ережесі',
        'btn_get_link': 'СІЛТЕМЕҢІЗДІ АЛЫҢЫЗ ЖӘНЕ ДОСТАРЫҢЫЗҒА ЖІБЕРІҢІЗ',
        'btn_bonus_info': 'БОНУС ЖҮЙЕСІ ТУРАЛЫ ТҮСІНДІРМЕ',
        'btn_my_coins': 'ТИЫНДАРЫМ',
    },

    # =================================================
    # 6. QIRG'IZCHA (KYRGYZ)
    # =================================================
    'kg': {
        'start': "🇰🇬 Тилди тандаңыз:",
        'agreement': "⚠️ **Көңүл буруңуз!**\nСиздин маалыматтарыңыз бажы органдарында иштетилишине макулсузбу?",
        'ask_phone': "📱 Төмөндөгү **'Номерди жөнөтүү'** баскычын басыңыз:",
        'registered': "✅ **Ийгиликтүү катталдыңыз!**\nКеректүү кызматты тандаңыз:",
        'enter_car': "🚛 Унаа номерин жазыңыз (Мисал: 01A777AA):",
        'autofill_found': "🤖 **Авто-Толтуруу системасы:**\n\nУрматтуу айдоочу, **{car}** унаасы үчүн мурунку документтериңиз (Тех-паспорт, Права) базада бар.\n\n**Аларды колдоноюнбу?** (Убактыңыз үнөмдөлөт)",
        'autofill_used': "✅ **Эски документтер жүктөлдү!**\n\nЭми бул рейстин жаңы документтерин гана (CMR, Жүк каты) сүрөткө тартып жөнөтүңүз.",
        'docs_header': "📸 **Документтерди жүктөө**\n\nТөмөнкү документтерди так сүрөткө тартып жөнөтүңүз:",
        'docs_list_at': "📄 **Тех-паспорт** (Алды-Арты)\n🪪 **Права** (Алды-Арты)\n🚛 **Тиркеме** (Тех-паспорт)\n📦 **CMR жана Инвойс**\n📜 **Сертификаттар**\n⚖️ **Нотариалдык документтер**",
        'docs_list_mb': "📄 **Тех-паспорт** (Алды-Арты)\n🪪 **Права** (Алды-Арты)",
        'docs_footer': "\n✅ Бардык сүрөттөрдү жүктөгөндөн кийин **'Бүттүм'** баскычын басыңыз.",
        'zero_photos': "⚠️ Сиз али бир дагы сүрөт жүктөгөн жоксуз!",
        'select_post': "🏢 **Кирүү (Чек ара)** постун тандаңыз:",
        'select_dest_post': "🏁 **Баратаган жер (ТИФ)** постун тандаңыз:",
        'select_viloyat': "🗺 **Кайсы облуска барасыз?**\n\nОблусту тандаңыз:",
        'finish': "✅ **Арызыңыз Админге жөнөтүлдү!**\n\n🆔 ID: `{code}`\n📄 Сүрөттөр саны: {count}\n\n⏳ Админ жообун күтүңүз...",
        'settings_title': "⚙️ **Орнотуулар бөлүмү:**\nМаалыматтарыңызды өзгөртүү же админ менен байланышуу үчүн тандаңыз:",
        'cache_cleared': "✅ **Эстутум тазаланды!**\nЭми бот эски документтериңизди эстебейт.",
        'support_ask': "✍️ **Суроонуз же көйгөйүңүздү жазыңыз:**\n\nБиздин операторлор жакында жооп беришет.",
        'support_sent': "✅ **Кабарыңыз админге жөнөтүлдү!**\nЖоопту ушул жерде күтүңүз.",
        'my_apps_empty': "📭 Сизде азырынча арыздар жок.",
        'invoice_msg': "✅ **Арызыңыз тастыкталды!**\n\n🆔 ID: `{code}`\n📦 Жүк көлөмү: **{tier}**\n💰 Төлөө суммасы: **{amount} сум**\n\nТөлөө ыкмасын тандаңыз:",
        'admin_broadcast': "🔔 **ЖАҢЫЛЫК (Админ):**\n\n{text}",

        # Баскычтар
        'btn_done': "Бүттүм",
        'btn_yes_auto': "Ооба, колдоноюн",
        'btn_no_auto': "Жок, жаңысын жүктөйм",
        'btn_lang': "Тилди өзгөртүү",
        'btn_phone': "Номерди өзгөртүү",
        'btn_clear': "Эстутумду тазалоо",
        'btn_support': "Админ менен байланыш",
        'btn_back': "Артка",
        'btn_cancel': "Жокко чыгаруу",
        'btn_change_phone': "НОМЕРДИ ӨЗГӨРТҮҮ",
        'btn_change_lang': "ТИЛДИ ӨЗГӨРТҮҮ",
        'btn_clear_cache': "ЭСТУТУМДУ ТАЗАЛОО",
        'btn_admin_contact': "АДМИН МЕНЕН БАЙЛАНЫШ",
        'btn_search_app': "АРЫЗ БАР",
        'btn_my_apps': "АРЫЗДАРЫМ",
        'btn_cash': "АГЕНТТЕР АРКЫЛУУ НАКТАЛАЙ",

        # Кадамдар
        'step_1': "1-кадам: Номер", 'step_2': "2-кадам: Документтер", 'step_3': "3-кадам: Пост", 'step_4': "4-кадам: Баратаган жер", 'step_5': "Бүтүрүү",

        # Негизги меню
        'menu_epi': 'ЭПИ КОД АТ ДЕКЛАРАЦИЯ',
        'menu_mb': 'МБ ДЕКЛАРАЦИЯ',
        'menu_contacts': 'ИШЕНИМ ТЕЛЕФОНДОРУ',
        'menu_apps': 'АРЫЗДАРЫМ',
        'menu_settings': 'ОРНОТУУЛАР',
        'menu_prices': 'БААЛАР КАТАЛОГУ',
        'menu_app': 'ТИРКЕМЕНИ ЖҮКТӨӨ',
        'menu_kgd': 'КГД(Э-ТРАНЗИТ) КӨРҮҮ',
        'menu_gabarit': 'ГАБАРИТ УРУКСАТ АЛУУ',
        'menu_sugurta': 'КАМСЫЗДАНДЫРУУ',
        'menu_navbat': 'ЭЛЕКТРОНДУК КЕЗЕК',
        'menu_yuklar': 'ИШЕНИМДҮҮ ЖҮКТӨР САТУУ-АЛУУ',
        'menu_bonus': 'БОТ АРКЫЛУУ БОНУС',
        'menu_balance': 'ТЫЙЫНДАРЫМ ЭСЕБИ',
        'menu_social': 'СОЦИАЛДЫК ТАРМАКТАР',
        'menu_chat': 'СҮЙЛӨШҮҮ',

        # EPI жана MB
        'epi_start': "📄 **ЭПИ КОД АТ ДЕКЛАРАЦИЯ**\n\nЧек ара бажы постун тандаңыз:",
        'mb_start': "📋 **МБ ДЕКЛАРАЦИЯ**\n\nЧек ара бажы постун тандаңыз:",
        'select_agent': "👨‍💼 **Агент тандоо**\n\nАгенттердин бирин тандаңыз:",
        'enter_car_number': "🚛 **Унаа номерин киргизиңиз:**\n\n(Мисал: 01A777AA)",
        'docs_epi': "📸 **Документтерди жүктөңүз:**\n\n📄 Паспорт\n📄 Тех-паспорт\n📦 CMR; Инвойс; Орома тизмеси\n📜 Башка документтер\n\n✅ Жүктөгөндөн кийин **'Бүттүм'** басыңыз.",
        'docs_mb': "📸 **Документтерди жүктөңүз:**\n\n📄 Паспорт\n📄 Тех-паспорт\n\n✅ Жүктөгөндөн кийин **'Бүттүм'** басыңыз.",
        'waiting_admin': "⏳ **Арызыңыз админдерге жөнөтүлдү!**\n\n🆔 Арыз коду: `{code}`\n\nАдмин жообун күтүңүз...",
        'price_set': "✅ **Арыз тастыкталды!**\n\n💰 Баасы: **{price} сум**\n\nТөлөө түрүн тандаңыз:",

        # Ишеним телефондору
        'contacts_msg': "📞 **ИШЕНИМ ТЕЛЕФОНДОРУ**\n\n📱 +998 91 702 00 99\n📱 +998 94 312 00 99\n\n📱 Telegram: @CARAVAN_TRANZIT, @caravan_tranzit1\n\n💬 WhatsApp: +998 91 702 00 99",

        # Баалар
        'prices_catalog': "<b>🚛 CARAVAN TRANZIT — ЭПИ-КОД КЫЗМАТЫ</b>\n\nБекитилген баа тизмеси:\n\n➖➖➖➖➖➖➖➖➖➖➖\n<b>📦 Кичине партиялар:</b>\n▪️ <b>1-2 партия:</b> 35 000 сум\n▪️ <b>3 партия:</b> 45 000 сум\n\n<b>📈 Чоң партиялар:</b>\n▪️ <b>4 партия:</b> 60 000 сум\n▪️ <b>5 партия:</b> 75 000 сум\n▪️ <b>6 партия:</b> 105 000 сум\n▪️ <b>7 партия:</b> 126 000 сум\n▪️ <b>8 партия:</b> 144 000 сум\n▪️ <b>9 партия:</b> 180 000 сум\n➖➖➖➖➖➖➖➖➖➖➖",

        # Арыздарым
        'apps_menu': "🎫 **АРЫЗДАРЫМ**\n\nТандаңыз:",
        'search_app_car': "🔍 **АРЫЗ ИЗДӨӨ**\n\nУнаа номерин киргизиңиз:",
        'app_found': "✅ **Арыз табылды!**\n\n🆔 Код: `{code}`\n🚛 Унаа: {car}\n📅 Күнү: {date}\n📊 Статусу: {status}",
        'app_not_found': "❌ Бул унаа номери боюнча арыз табылган жок.",
        'my_apps_list': "📂 **СИЗДИН АРЫЗДАРЫҢЫЗ:**\n\n{apps}",
        'payment_methods': "💳 **Төлөө ыкмасын тандаңыз:**",

        # Орнотуулар
        'settings_menu': "⚙️ **ОРНОТУУЛАР**\n\nТандаңыз:",
        'change_phone_msg': "📱 **Номерди өзгөртүү**\n\nЖаңы номериңизди жөнөтүңүз:",
        'change_lang_msg': "🌐 **Тилди өзгөртүү**\n\nТилди тандаңыз:",
        'clear_cache_msg': "🗑 **Эстутумду тазалоо**\n\nБардык сакталган документтериңиз өчүрүлөт. Уланасызбы?",
        'cache_cleared_msg': "✅ Эстутум тазаланды!",
        'admin_contact_msg': "👨‍💼 **АДМИН МЕНЕН БАЙЛАНЫШ**\n\n📞 Телефон: +998917020099, +998943120099\n📱 Telegram: @CARAVAN_TRANZIT, @caravan_tranzit1\n💬 WhatsApp: +998917020099",

        # Баалар
        'prices_msg': "💰 **БААЛАР КАТАЛОГУ**\n\nБардык бааларды көрүү үчүн шилтемеге өтүңүз:",

        # Тиркемени жүктөө
        'app_download_msg': "📱 **ТИРКЕМЕНИ ЖҮКТӨӨ**\n\nТандаңыз:",
        'app_link_msg': "🔗 **Тиркеме шилтемеси:**\n\nЖүктөө үчүн басыңыз",
        'app_guide_msg': "📖 **Колдонуу көрсөтмөсү:**\n\n1. Тиркемени жүктөңүз\n2. Орнотуңуз\n3. Телефон номериңиз менен кириңиз",
        'bonus_guide_msg': "🎁 **Бонус алуу көрсөтмөсү:**\n\n👥 Досуңуз катталса: **2,000 тыйын**\n💰 Досуңуз код сатып алса: **17,500 тыйын**\n🎯 Максат: **35,000 тыйын = 1 АКЫСЫЗ ЭПИ КОД**",

        # KGD
        'kgd_menu_msg': "🚚 **КГД (Э-ТРАНЗИТ) КӨРҮҮ**\n\nЫкманы тандаңыз:",
        'kgd_app_msg': "📱 **Тиркеме аркылуу көрүү:**",
        'kgd_staff_car': "👥 **Кызматкерлер аркылуу көрүү**\n\nУнаа номерин киргизиңиз:",
        'kgd_checking': "🔍 Текшерилүүдө... Бир аз күтүңүз.",

        # Габарит
        'gabarit_msg': "📜 **ГАБАРИТ УРУКСАТ АЛУУ**\n\nУруксат алуу үчүн админ менен байланышыңыз:\n\n📱 @CARAVAN_TRANZIT\n📱 @caravan_tranzit1\n\n✍️ \"ГАБАРИТ\" деп жазыңыз",

        # Placeholder
        'coming_soon': "🚧 **ЖАКЫНДА**\n\nБул кызмат жакында иштей баштайт!",

        # Бонус
        'bonus_menu_msg': "🎁 **БОТ АРКЫЛУУ БОНУС**\n\nТандаңыз:",
        'get_referral_link': "🔗 **Сиздин шилтемеңиз:**\n\n`{link}`\n\nДостроруңузга жөнөтүңүз жана бонус чогултуңуз!",
        'bonus_info': "ℹ️ **БОНУС СИСТЕМАСЫ ТУУРАЛУУ:**\n\n🎁 Достроруңузду чакырыңыз жана тыйын чогултуңуз!\n\n👥 Дос катталса: **2,000 тыйын**\n💰 Дос ЭПИ код алса: **17,500 тыйын**\n\n🎯 35,000 тыйын = **1 АКЫСЫЗ ЭПИ КОД**",

        # Тыйындар
        'balance_msg': "💎 **ТЫЙЫНДАРЫМ ЭСЕБИ**\n\n💰 Сиздин балансыңыз: **{balance} тыйын**\n\n🎁 35,000 тыйын = 1 АКЫСЫЗ ЭПИ КОД",

        # Социалдык
        'social_msg': "📱 **СОЦИАЛДЫК ТАРМАКТАР**\n\nБизди социалдык тармактарда байкаңыз:",

        # Чат
        'chat_msg': "💬 **СҮЙЛӨШҮҮ**\n\nСуроонузду жазыңыз, оператор жооп берет:",
        'chat_sent': "✅ Кабарыңыз жөнөтүлдү! Жоопту күтүңүз.",
        'chat_continue': "✅ Кабарыңыз жөнөтүлдү! Жазууну улантсаңыз болот же чатты аяктаңыз.",
        'chat_ended': "✅ Чат аяктады. Рахмат!",
        'btn_end_chat': "Чатты аяктоо",

        # Баскыч тексттери
        'btn_app_link': 'ТИРКЕМЕНИ ЖҮКТӨӨ ШИЛТЕМЕСИ',
        'btn_app_guide': 'КОЛДОНУУ КӨРСӨТМӨСҮ',
        'btn_bonus_guide': 'ТИРКЕМЕ АРКЫЛУУ БОНУС АЛУУ КӨРСӨТМӨСҮ',
        'btn_kgd_app': 'ТИРКЕМЕ АРКЫЛУУ КӨРҮҮ',
        'btn_kgd_staff': 'КЫЗМАТКЕРЛЕР АРКЫЛУУ КӨРҮҮ',
        'btn_download': 'Жүктөө шилтемеси',
        'btn_guide_use': 'Колдонуу боюнча колдонмо',
        'btn_guide_kgd': 'КГД көрүү боюнча колдонмо',
        'btn_bonus_rule': 'Бонус алуу эрежеси',
        'btn_get_link': 'ШИЛТЕМЕҢИЗДИ АЛЫҢЫЗ ЖАНА ДОСТРОРУҢУЗГА ЖӨНӨТҮҢҮЗ',
        'btn_bonus_info': 'БОНУС СИСТЕМАСЫ ТУУРАЛУУ ТҮШҮНДҮРМӨ',
        'btn_my_coins': 'ТЫЙЫНДАРЫМ',
    },

    # =================================================
    # 7. TOJIKCHA (TAJIK)
    # =================================================
    'tj': {
        'start': "🇹🇯 Забонро интихоб кунед:",
        'agreement': "⚠️ **Диққат!**\nОё шумо ба коркарди маълумоти худ аз ҷониби мақомоти гумрукӣ розиед?",
        'ask_phone': "📱 Лутфан тугмаи **'Рақамро фиристед'** -ро пахш кунед:",
        'registered': "✅ **Бомуваффақият бақайдгирӣ шудед!**\nХизмати заруриро интихоб кунед:",
        'enter_car': "🚛 Рақами мошинро ворид кунед (Мисол: 01A777AA):",
        'autofill_found': "🤖 **Системаи авто-пуркунӣ:**\n\nҲурматли ронанда, барои мошини **{car}** ҳуҷҷатҳои пештара (Тех-паспорт, Гувоҳнома) дар база мавҷуданд.\n\n**Онҳоро истифода барем?** (Вақти шумо сарфа мешавад)",
        'autofill_used': "✅ **Ҳуҷҷатҳои кӯҳна бор шуданд!**\n\nАкнун танҳо ҳуҷҷатҳои нави ин рейсро (CMR, Барги бор) сурат гирифта фиристед.",
        'docs_header': "📸 **Боркунии ҳуҷҷатҳо**\n\nҲуҷҷатҳои зеринро аниқ сурат гирифта фиристед:",
        'docs_list_at': "📄 **Тех-паспорт** (Пеш-Қафо)\n🪪 **Гувоҳнома** (Пеш-Қафо)\n🚛 **Прицеп** (Тех-паспорт)\n📦 **CMR ва Инвойс**\n📜 **Сертификатҳо**\n⚖️ **Ҳуҷҷатҳои нотариалӣ**",
        'docs_list_mb': "📄 **Тех-паспорт** (Пеш-Қафо)\n🪪 **Гувоҳнома** (Пеш-Қафо)",
        'docs_footer': "\n✅ Пас аз боркунии ҳамаи суратҳо тугмаи **'Тайёр'**-ро пахш кунед.",
        'zero_photos': "⚠️ Шумо ҳанӯз ягон сурат бор накардаед!",
        'select_post': "🏢 Пости **Воридшавӣ (Сарҳад)**-ро интихоб кунед:",
        'select_dest_post': "🏁 Пости **Мақсад (ТИФ)**-ро интихоб кунед:",
        'select_viloyat': "🗺 **Ба кадом вилоят меравед?**\n\nВилоятро интихоб кунед:",
        'finish': "✅ **Аризаи шумо ба Админ фиристода шуд!**\n\n🆔 ID: `{code}`\n📄 Миқдори суратҳо: {count}\n\n⏳ Ҷавоби админро интизор шавед...",
        'settings_title': "⚙️ **Бахши танзимот:**\nБарои тағйири маълумот ё алоқа бо админ интихоб кунед:",
        'cache_cleared': "✅ **Хотира тоза шуд!**\nАкнун бот ҳуҷҷатҳои кӯҳнаи шуморо дар ёд намедорад.",
        'support_ask': "✍️ **Саволи худ ё мушкилро нависед:**\n\nОператорони мо ба наздикӣ ҷавоб медиҳанд.",
        'support_sent': "✅ **Паёми шумо ба админ фиристода шуд!**\nҶавобро дар ҳамин ҷо интизор шавед.",
        'my_apps_empty': "📭 Шумо ҳанӯз аризаҳо надоред.",
        'invoice_msg': "✅ **Аризаи шумо тасдиқ шуд!**\n\n🆔 ID: `{code}`\n📦 Ҳаҷми бор: **{tier}**\n💰 Маблағи пардохт: **{amount} сум**\n\nУсули пардохтро интихоб кунед:",
        'admin_broadcast': "🔔 **ХАБАР (Админ):**\n\n{text}",

        # Тугмаҳо
        'btn_done': "Тайёр",
        'btn_yes_auto': "Ҳа, истифода мебарем",
        'btn_no_auto': "Не, нав бор мекунам",
        'btn_lang': "Тағйири забон",
        'btn_phone': "Тағйири рақам",
        'btn_clear': "Тозакунии хотира",
        'btn_support': "Алоқа бо админ",
        'btn_back': "Бозгашт",
        'btn_cancel': "Бекор кардан",
        'btn_change_phone': "ТАҒЙИРИ РАҚАМ",
        'btn_change_lang': "ТАҒЙИРИ ЗАБОН",
        'btn_clear_cache': "ТОЗАКУНИИ ХОТИРА",
        'btn_admin_contact': "АЛОҚА БО АДМИН",
        'btn_search_app': "АРИЗА ҲАСТ",
        'btn_my_apps': "АРИЗАҲОИ МАН",
        'btn_cash': "БО НАҚД ТАВАССУТИ АГЕНТҲО",

        # Қадамҳо
        'step_1': "Қадами 1: Рақам", 'step_2': "Қадами 2: Ҳуҷҷатҳо", 'step_3': "Қадами 3: Пост", 'step_4': "Қадами 4: Мақсад", 'step_5': "Анҷом",

        # Менюи асосӣ
        'menu_epi': 'ЭПИ КОД АТ ДЕКЛАРАТСИЯ',
        'menu_mb': 'МБ ДЕКЛАРАТСИЯ',
        'menu_contacts': 'ТЕЛЕФОНҲОИ БОВАРӢ',
        'menu_apps': 'АРИЗАҲОИ МАН',
        'menu_settings': 'ТАНЗИМОТ',
        'menu_prices': 'КАТАЛОГИ НАРХҲО',
        'menu_app': 'БАРНОМАРО БОРГИРӢ КУНЕД',
        'menu_kgd': 'КГД(Э-ТРАНЗИТ) ДИДАН',
        'menu_gabarit': 'ИҶОЗАТИ ГАБАРИТ ГИРИФТАН',
        'menu_sugurta': 'СУҒУРТА',
        'menu_navbat': 'НАВБАТИ ЭЛЕКТРОНӢ',
        'menu_yuklar': 'БОРҲОИ БОЭЪТИМОД ХАРИДУ ФУРӮШ',
        'menu_bonus': 'БОНУС ТАВАССУТИ БОТ',
        'menu_balance': 'ҲИСОБИ ТАНГАҲОЯМ',
        'menu_social': 'ШАБАКАҲОИ ИҶТИМОӢ',
        'menu_chat': 'СӮҲБАТ',

        # EPI ва MB
        'epi_start': "📄 **ЭПИ КОД АТ ДЕКЛАРАТСИЯ**\n\nПости гумрукии сарҳадро интихоб кунед:",
        'mb_start': "📋 **МБ ДЕКЛАРАТСИЯ**\n\nПости гумрукии сарҳадро интихоб кунед:",
        'select_agent': "👨‍💼 **Интихоби агент**\n\nЯке аз агентҳоро интихоб кунед:",
        'enter_car_number': "🚛 **Рақами мошинро ворид кунед:**\n\n(Мисол: 01A777AA)",
        'docs_epi': "📸 **Ҳуҷҷатҳоро бор кунед:**\n\n📄 Шиноснома\n📄 Тех-паспорт\n📦 CMR; Инвойс; Рӯйхати борбандӣ\n📜 Ҳуҷҷатҳои дигар\n\n✅ Пас аз боркунӣ **'Тайёр'**-ро пахш кунед.",
        'docs_mb': "📸 **Ҳуҷҷатҳоро бор кунед:**\n\n📄 Шиноснома\n📄 Тех-паспорт\n\n✅ Пас аз боркунӣ **'Тайёр'**-ро пахш кунед.",
        'waiting_admin': "⏳ **Аризаи шумо ба админҳо фиристода шуд!**\n\n🆔 Коди ариза: `{code}`\n\nҶавоби админро интизор шавед...",
        'price_set': "✅ **Ариза тасдиқ шуд!**\n\n💰 Нарх: **{price} сум**\n\nНавъи пардохтро интихоб кунед:",

        # Телефонҳои боварӣ
        'contacts_msg': "📞 **ТЕЛЕФОНҲОИ БОВАРӢ**\n\n📱 +998 91 702 00 99\n📱 +998 94 312 00 99\n\n📱 Telegram: @CARAVAN_TRANZIT, @caravan_tranzit1\n\n💬 WhatsApp: +998 91 702 00 99",

        # Нархҳо
        'prices_catalog': "<b>🚛 CARAVAN TRANZIT — ХИЗМАТИ ЭПИ-КОД</b>\n\nРӯйхати нархҳои тасдиқшуда:\n\n➖➖➖➖➖➖➖➖➖➖➖\n<b>📦 Партияҳои хурд:</b>\n▪️ <b>1-2 партия:</b> 35 000 сум\n▪️ <b>3 партия:</b> 45 000 сум\n\n<b>📈 Партияҳои калон:</b>\n▪️ <b>4 партия:</b> 60 000 сум\n▪️ <b>5 партия:</b> 75 000 сум\n▪️ <b>6 партия:</b> 105 000 сум\n▪️ <b>7 партия:</b> 126 000 сум\n▪️ <b>8 партия:</b> 144 000 сум\n▪️ <b>9 партия:</b> 180 000 сум\n➖➖➖➖➖➖➖➖➖➖➖",

        # Аризаҳои ман
        'apps_menu': "🎫 **АРИЗАҲОИ МАН**\n\nИнтихоб кунед:",
        'search_app_car': "🔍 **ҶУСТУҶӮИ АРИЗА**\n\nРақами мошинро ворид кунед:",
        'app_found': "✅ **Ариза ёфт шуд!**\n\n🆔 Код: `{code}`\n🚛 Мошин: {car}\n📅 Сана: {date}\n📊 Ҳолат: {status}",
        'app_not_found': "❌ Аз рӯйи ин рақами мошин ариза ёфт нашуд.",
        'my_apps_list': "📂 **АРИЗАҲОИ ШУМО:**\n\n{apps}",
        'payment_methods': "💳 **Усули пардохтро интихоб кунед:**",

        # Танзимот
        'settings_menu': "⚙️ **ТАНЗИМОТ**\n\nИнтихоб кунед:",
        'change_phone_msg': "📱 **Тағйири рақам**\n\nРақами нави худро фиристед:",
        'change_lang_msg': "🌐 **Тағйири забон**\n\nЗабонро интихоб кунед:",
        'clear_cache_msg': "🗑 **Тозакунии хотира**\n\nҲамаи ҳуҷҷатҳои захирашуда нест мешаванд. Идома медиҳед?",
        'cache_cleared_msg': "✅ Хотира тоза шуд!",
        'admin_contact_msg': "👨‍💼 **АЛОҚА БО АДМИН**\n\n📞 Телефон: +998917020099, +998943120099\n📱 Telegram: @CARAVAN_TRANZIT, @caravan_tranzit1\n💬 WhatsApp: +998917020099",

        # Нархҳо
        'prices_msg': "💰 **КАТАЛОГИ НАРХҲО**\n\nБарои дидани ҳамаи нархҳо ба линк гузаред:",

        # Боргирии барнома
        'app_download_msg': "📱 **БАРНОМАРО БОРГИРӢ КУНЕД**\n\nИнтихоб кунед:",
        'app_link_msg': "🔗 **Линки барнома:**\n\nБарои боргирӣ пахш кунед",
        'app_guide_msg': "📖 **Дастури истифода:**\n\n1. Барномаро боргирӣ кунед\n2. Насб кунед\n3. Бо рақами телефон ворид шавед",
        'bonus_guide_msg': "🎁 **Дастури гирифтани бонус:**\n\n👥 Дӯстатон бақайдгирӣ шавад: **2,000 танга**\n💰 Дӯстатон код харад: **17,500 танга**\n🎯 Ҳадаф: **35,000 танга = 1 ЭПИ КОДИ РОЙГОН**",

        # KGD
        'kgd_menu_msg': "🚚 **КГД (Э-ТРАНЗИТ) ДИДАН**\n\nУсулро интихоб кунед:",
        'kgd_app_msg': "📱 **Тавассути барнома дидан:**",
        'kgd_staff_car': "👥 **Тавассути кормандон дидан**\n\nРақами мошинро ворид кунед:",
        'kgd_checking': "🔍 Санҷида истодааст... Каме интизор шавед.",

        # Габарит
        'gabarit_msg': "📜 **ИҶОЗАТИ ГАБАРИТ ГИРИФТАН**\n\nБарои гирифтани иҷозат бо админ алоқа гиред:\n\n📱 @CARAVAN_TRANZIT\n📱 @caravan_tranzit1\n\n✍️ \"ГАБАРИТ\" нависед",

        # Placeholder
        'coming_soon': "🚧 **БА НАЗДИКӢ**\n\nИн хизмат ба наздикӣ оғоз мешавад!",

        # Бонус
        'bonus_menu_msg': "🎁 **БОНУС ТАВАССУТИ БОТ**\n\nИнтихоб кунед:",
        'get_referral_link': "🔗 **Линки шумо:**\n\n`{link}`\n\nБа дӯстон фиристед ва бонус ҷамъ кунед!",
        'bonus_info': "ℹ️ **ДАР БОРАИ СИСТЕМАИ БОНУС:**\n\n🎁 Дӯстонро даъват кунед ва танга ҷамъ кунед!\n\n👥 Дӯст бақайдгирӣ шавад: **2,000 танга**\n💰 Дӯст ЭПИ код гирад: **17,500 танга**\n\n🎯 35,000 танга = **1 ЭПИ КОДИ РОЙГОН**",

        # Тангаҳо
        'balance_msg': "💎 **ҲИСОБИ ТАНГАҲОЯМ**\n\n💰 Балансии шумо: **{balance} танга**\n\n🎁 35,000 танга = 1 ЭПИ КОДИ РОЙГОН",

        # Иҷтимоӣ
        'social_msg': "📱 **ШАБАКАҲОИ ИҶТИМОӢ**\n\nМоро дар шабакаҳои иҷтимоӣ пайгирӣ кунед:",

        # Чат
        'chat_msg': "💬 **СӮҲБАТ**\n\nСаволи худро нависед, оператор ҷавоб медиҳад:",
        'chat_sent': "✅ Паёми шумо фиристода шуд! Ҷавобро интизор шавед.",
        'chat_continue': "✅ Паёми шумо фиристода шуд! Метавонед идома диҳед ё чатро анҷом диҳед.",
        'chat_ended': "✅ Чат анҷом ёфт. Ташаккур!",
        'btn_end_chat': "Анҷом додани чат",

        # Матнҳои тугмаҳо
        'btn_app_link': 'ЛИНКИ БОРГИРИИ БАРНОМА',
        'btn_app_guide': 'ДАСТУРИ ИСТИФОДАИ БАРНОМА',
        'btn_bonus_guide': 'ДАСТУРИ ГИРИФТАНИ БОНУС ТАВАССУТИ БАРНОМА',
        'btn_kgd_app': 'ДИДАН ТАВАССУТИ БАРНОМА',
        'btn_kgd_staff': 'ДИДАН ТАВАССУТИ КОРМАНДОН',
        'btn_download': 'Линки боргирӣ',
        'btn_guide_use': 'Дастури истифода',
        'btn_guide_kgd': 'Дастури дидани КГД',
        'btn_bonus_rule': 'Қоидаи гирифтани бонус',
        'btn_get_link': 'ЛИНКИ ХУДРО ГИРЕД ВА БА ДӮСТОН ФИРИСТЕД',
        'btn_bonus_info': 'ТАВЗЕҲОТ ДАР БОРАИ СИСТЕМАИ БОНУС',
        'btn_my_coins': 'ТАНГАҲОЯМ',
    },

    # =================================================
    # 8. TURKCHA (TURKISH)
    # =================================================
    'tr': {
        'start': "🇹🇷 Lütfen dil seçin:",
        'agreement': "⚠️ **Dikkat!**\nVerilerinizin gümrük makamları tarafından işlenmesini kabul ediyor musunuz?",
        'ask_phone': "📱 Lütfen aşağıdaki **'Numara Gönder'** düğmesine basın:",
        'registered': "✅ **Başarıyla kayıt oldunuz!**\nGerekli hizmeti seçin:",
        'enter_car': "🚛 Araç plakasını girin (Örnek: 01A777AA):",
        'autofill_found': "🤖 **Otomatik Doldurma Sistemi:**\n\nSayın sürücü, **{car}** aracı için önceki belgeleriniz (Ruhsat, Ehliyet) veritabanında mevcut.\n\n**Bunları kullanalım mı?** (Zaman kazanırsınız)",
        'autofill_used': "✅ **Eski belgeler yüklendi!**\n\nŞimdi sadece bu seferin yeni belgelerini (CMR, Yük Senedi) fotoğraflayıp gönderin.",
        'docs_header': "📸 **Belge Yükleme**\n\nAşağıdaki belgeleri net bir şekilde fotoğraflayıp gönderin:",
        'docs_list_at': "📄 **Ruhsat** (Ön-Arka)\n🪪 **Ehliyet** (Ön-Arka)\n🚛 **Dorse** (Ruhsat)\n📦 **CMR ve Fatura**\n📜 **Sertifikalar**\n⚖️ **Noter Belgeleri**",
        'docs_list_mb': "📄 **Ruhsat** (Ön-Arka)\n🪪 **Ehliyet** (Ön-Arka)",
        'docs_footer': "\n✅ Tüm fotoğrafları yükledikten sonra **'Tamam'** düğmesine basın.",
        'zero_photos': "⚠️ Henüz hiç fotoğraf yüklemediniz!",
        'select_post': "🏢 **Giriş (Sınır)** Gümrük Kapısını seçin:",
        'select_dest_post': "🏁 **Varış (TED)** Gümrük Kapısını seçin:",
        'select_viloyat': "🗺 **Hangi bölgeye gidiyorsunuz?**\n\nBölge seçin:",
        'finish': "✅ **Başvurunuz Admin'e gönderildi!**\n\n🆔 ID: `{code}`\n📄 Fotoğraf sayısı: {count}\n\n⏳ Admin yanıtını bekleyin...",
        'settings_title': "⚙️ **Ayarlar Bölümü:**\nBilgilerinizi değiştirmek veya adminle iletişime geçmek için seçin:",
        'cache_cleared': "✅ **Önbellek temizlendi!**\nArtık bot eski belgelerinizi hatırlamayacak.",
        'support_ask': "✍️ **Sorunuzu veya sorununuzu yazın:**\n\nOperatörlerimiz yakında yanıt verecek.",
        'support_sent': "✅ **Mesajınız admin'e gönderildi!**\nYanıtı burada bekleyin.",
        'my_apps_empty': "📭 Henüz başvurunuz yok.",
        'invoice_msg': "✅ **Başvurunuz onaylandı!**\n\n🆔 ID: `{code}`\n📦 Yük hacmi: **{tier}**\n💰 Ödeme tutarı: **{amount} sum**\n\nÖdeme yöntemini seçin:",
        'admin_broadcast': "🔔 **HABER (Admin):**\n\n{text}",

        # Düğmeler
        'btn_done': "Tamam",
        'btn_yes_auto': "Evet, kullanalım",
        'btn_no_auto': "Hayır, yeni yükleyeceğim",
        'btn_lang': "Dili Değiştir",
        'btn_phone': "Numarayı Değiştir",
        'btn_clear': "Önbelleği Temizle",
        'btn_support': "Admin ile İletişim",
        'btn_back': "Geri",
        'btn_cancel': "İptal",
        'btn_change_phone': "NUMARAYI DEĞİŞTİR",
        'btn_change_lang': "DİLİ DEĞİŞTİR",
        'btn_clear_cache': "ÖNBELLEĞİ TEMİZLE",
        'btn_admin_contact': "ADMİN İLE İLETİŞİM",
        'btn_search_app': "BAŞVURU ARA",
        'btn_my_apps': "BAŞVURULARIM",
        'btn_cash': "ACENTELER ARACILIĞIYLA NAKİT",

        # Adımlar
        'step_1': "Adım 1: Numara", 'step_2': "Adım 2: Belgeler", 'step_3': "Adım 3: Kapı", 'step_4': "Adım 4: Varış", 'step_5': "Bitiş",

        # Ana menü
        'menu_epi': 'EPİ KOD AT DEKLARASYON',
        'menu_mb': 'MB DEKLARASYON',
        'menu_contacts': 'GÜVEN TELEFONLARI',
        'menu_apps': 'BAŞVURULARIM',
        'menu_settings': 'AYARLAR',
        'menu_prices': 'FİYAT KATALOĞU',
        'menu_app': 'UYGULAMAYI İNDİR',
        'menu_kgd': 'KGD(E-TRANZİT) GÖRÜNTÜLE',
        'menu_gabarit': 'GABARİT İZNİ AL',
        'menu_sugurta': 'SİGORTA',
        'menu_navbat': 'ELEKTRONİK KUYRUK',
        'menu_yuklar': 'GÜVENİLİR YÜKLER ALIM-SATIM',
        'menu_bonus': 'BOT ARACILIĞIYLA BONUS',
        'menu_balance': 'JETONLARİM HESABI',
        'menu_social': 'SOSYAL MEDYA',
        'menu_chat': 'SOHBET',

        # EPI ve MB
        'epi_start': "📄 **EPİ KOD AT DEKLARASYON**\n\nSınır gümrük kapısını seçin:",
        'mb_start': "📋 **MB DEKLARASYON**\n\nSınır gümrük kapısını seçin:",
        'select_agent': "👨‍💼 **Acente Seçimi**\n\nAcentelerden birini seçin:",
        'enter_car_number': "🚛 **Araç plakasını girin:**\n\n(Örnek: 01A777AA)",
        'docs_epi': "📸 **Belgeleri yükleyin:**\n\n📄 Pasaport\n📄 Ruhsat\n📦 CMR; Fatura; Paketleme listesi\n📜 Diğer belgeler\n\n✅ Yükledikten sonra **'Tamam'**a basın.",
        'docs_mb': "📸 **Belgeleri yükleyin:**\n\n📄 Pasaport\n📄 Ruhsat\n\n✅ Yükledikten sonra **'Tamam'**a basın.",
        'waiting_admin': "⏳ **Başvurunuz adminlere gönderildi!**\n\n🆔 Başvuru kodu: `{code}`\n\nAdmin yanıtını bekleyin...",
        'price_set': "✅ **Başvuru onaylandı!**\n\n💰 Fiyat: **{price} sum**\n\nÖdeme türünü seçin:",

        # Güven telefonları
        'contacts_msg': "📞 **GÜVEN TELEFONLARI**\n\n📱 +998 91 702 00 99\n📱 +998 94 312 00 99\n\n📱 Telegram: @CARAVAN_TRANZIT, @caravan_tranzit1\n\n💬 WhatsApp: +998 91 702 00 99",

        # Fiyatlar
        'prices_catalog': "<b>🚛 CARAVAN TRANZIT — EPİ-KOD HİZMETİ</b>\n\nOnaylı fiyat listesi:\n\n➖➖➖➖➖➖➖➖➖➖➖\n<b>📦 Küçük partiler:</b>\n▪️ <b>1-2 parti:</b> 35.000 sum\n▪️ <b>3 parti:</b> 45.000 sum\n\n<b>📈 Büyük partiler:</b>\n▪️ <b>4 parti:</b> 60.000 sum\n▪️ <b>5 parti:</b> 75.000 sum\n▪️ <b>6 parti:</b> 105.000 sum\n▪️ <b>7 parti:</b> 126.000 sum\n▪️ <b>8 parti:</b> 144.000 sum\n▪️ <b>9 parti:</b> 180.000 sum\n➖➖➖➖➖➖➖➖➖➖➖",

        # Başvurularım
        'apps_menu': "🎫 **BAŞVURULARIM**\n\nSeçin:",
        'search_app_car': "🔍 **BAŞVURU ARA**\n\nAraç plakasını girin:",
        'app_found': "✅ **Başvuru bulundu!**\n\n🆔 Kod: `{code}`\n🚛 Araç: {car}\n📅 Tarih: {date}\n📊 Durum: {status}",
        'app_not_found': "❌ Bu araç plakasıyla başvuru bulunamadı.",
        'my_apps_list': "📂 **BAŞVURULARINIZ:**\n\n{apps}",
        'payment_methods': "💳 **Ödeme yöntemini seçin:**",

        # Ayarlar
        'settings_menu': "⚙️ **AYARLAR**\n\nSeçin:",
        'change_phone_msg': "📱 **Numarayı Değiştir**\n\nYeni numaranızı gönderin:",
        'change_lang_msg': "🌐 **Dili Değiştir**\n\nDil seçin:",
        'clear_cache_msg': "🗑 **Önbelleği Temizle**\n\nKaydedilen tüm belgeleriniz silinecek. Devam ediyor musunuz?",
        'cache_cleared_msg': "✅ Önbellek temizlendi!",
        'admin_contact_msg': "👨‍💼 **ADMİN İLE İLETİŞİM**\n\n📞 Telefon: +998917020099, +998943120099\n📱 Telegram: @CARAVAN_TRANZIT, @caravan_tranzit1\n💬 WhatsApp: +998917020099",

        # Fiyatlar
        'prices_msg': "💰 **FİYAT KATALOĞU**\n\nTüm fiyatları görüntülemek için linke gidin:",

        # Uygulama indirme
        'app_download_msg': "📱 **UYGULAMAYI İNDİR**\n\nSeçin:",
        'app_link_msg': "🔗 **Uygulama linki:**\n\nİndirmek için tıklayın",
        'app_guide_msg': "📖 **Kullanım kılavuzu:**\n\n1. Uygulamayı indirin\n2. Yükleyin\n3. Telefon numaranızla giriş yapın",
        'bonus_guide_msg': "🎁 **Bonus alma kılavuzu:**\n\n👥 Arkadaşınız kayıt olursa: **2.000 jeton**\n💰 Arkadaşınız kod satın alırsa: **17.500 jeton**\n🎯 Hedef: **35.000 jeton = 1 ÜCRETSİZ EPİ KOD**",

        # KGD
        'kgd_menu_msg': "🚚 **KGD (E-TRANZİT) GÖRÜNTÜLE**\n\nYöntemi seçin:",
        'kgd_app_msg': "📱 **Uygulama aracılığıyla görüntüle:**",
        'kgd_staff_car': "👥 **Personel aracılığıyla görüntüle**\n\nAraç plakasını girin:",
        'kgd_checking': "🔍 Kontrol ediliyor... Lütfen bekleyin.",

        # Gabarit
        'gabarit_msg': "📜 **GABARİT İZNİ AL**\n\nİzin almak için adminle iletişime geçin:\n\n📱 @CARAVAN_TRANZIT\n📱 @caravan_tranzit1\n\n✍️ \"GABARİT\" yazın",

        # Placeholder
        'coming_soon': "🚧 **YAKINDA**\n\nBu hizmet yakında kullanıma açılacak!",

        # Bonus
        'bonus_menu_msg': "🎁 **BOT ARACILIĞIYLA BONUS**\n\nSeçin:",
        'get_referral_link': "🔗 **Linkiniz:**\n\n`{link}`\n\nArkadaşlarınıza gönderin ve bonus toplayın!",
        'bonus_info': "ℹ️ **BONUS SİSTEMİ HAKKINDA:**\n\n🎁 Arkadaşlarınızı davet edin ve jeton toplayın!\n\n👥 Arkadaş kayıt olursa: **2.000 jeton**\n💰 Arkadaş EPİ kod alırsa: **17.500 jeton**\n\n🎯 35.000 jeton = **1 ÜCRETSİZ EPİ KOD**",

        # Jetonlar
        'balance_msg': "💎 **JETONLARIM HESABI**\n\n💰 Bakiyeniz: **{balance} jeton**\n\n🎁 35.000 jeton = 1 ÜCRETSİZ EPİ KOD",

        # Sosyal
        'social_msg': "📱 **SOSYAL MEDYA**\n\nBizi sosyal medyada takip edin:",

        # Sohbet
        'chat_msg': "💬 **SOHBET**\n\nSorunuzu yazın, operatör yanıt verecek:",
        'chat_sent': "✅ Mesajınız gönderildi! Yanıtı bekleyin.",
        'chat_continue': "✅ Mesajınız gönderildi! Yazmaya devam edebilir veya sohbeti bitirebilirsiniz.",
        'chat_ended': "✅ Sohbet sona erdi. Teşekkürler!",
        'btn_end_chat': "Sohbeti bitir",

        # Düğme metinleri
        'btn_app_link': 'UYGULAMA İNDİRME LİNKİ',
        'btn_app_guide': 'UYGULAMA KULLANIM KILAVUZU',
        'btn_bonus_guide': 'UYGULAMA ARACILIĞIYLA BONUS ALMA KILAVUZU',
        'btn_kgd_app': 'UYGULAMA ARACILIĞIYLA GÖRÜNTÜLE',
        'btn_kgd_staff': 'PERSONEL ARACILIĞIYLA GÖRÜNTÜLE',
        'btn_download': 'İndirme linki',
        'btn_guide_use': 'Kullanım kılavuzu',
        'btn_guide_kgd': 'KGD görüntüleme kılavuzu',
        'btn_bonus_rule': 'Bonus alma kuralı',
        'btn_get_link': 'LİNKİNİZİ ALIN VE ARKADAŞLARINIZA GÖNDERİN',
        'btn_bonus_info': 'BONUS SİSTEMİ HAKKINDA AÇIKLAMA',
        'btn_my_coins': 'JETONLARIM',
    },

    # =================================================
    # 9. TURKMANCHA (TURKMEN)
    # =================================================
    'tm': {
        'start': "🇹🇲 Dili saýlaň:",
        'agreement': "⚠️ **Üns beriň!**\nSiziň maglumatlaryňyzyň gümrük edaralary tarapyndan işlenmegine razylyk berýärsiňizmi?",
        'ask_phone': "📱 Aşakdaky **'Belgini iber'** düwmesine basyň:",
        'registered': "✅ **Üstünlikli hasaba alyndyňyz!**\nZerur hyzmaty saýlaň:",
        'enter_car': "🚛 Ulag belgisini ýazyň (Mysal: 01A777AA):",
        'autofill_found': "🤖 **Awtomatik doldurma ulgamy:**\n\nHormatly sürüji, **{car}** ulagyňyz üçin öňki resminamalaryňyz (Teh-pasport, Şahadatnama) bazada bar.\n\n**Olary ulanalyňmy?** (Wagtyňyz tygşytlanar)",
        'autofill_used': "✅ **Köne resminamalar ýüklendi!**\n\nIndi diňe bu reýsiň täze resminamalaryny (CMR, Ýük haty) surata düşürip iberiň.",
        'docs_header': "📸 **Resminamalary ýüklemek**\n\nAşakdaky resminamalary anyk surata düşürip iberiň:",
        'docs_list_at': "📄 **Teh-pasport** (Öň-Arka)\n🪪 **Şahadatnama** (Öň-Arka)\n🚛 **Tirkeş** (Teh-pasport)\n📦 **CMR we Inwoýs**\n📜 **Sertifikatlar**\n⚖️ **Notarial resminamalar**",
        'docs_list_mb': "📄 **Teh-pasport** (Öň-Arka)\n🪪 **Şahadatnama** (Öň-Arka)",
        'docs_footer': "\n✅ Ähli suratlary ýükläniňizden soň **'Boldy'** düwmesine basyň.",
        'zero_photos': "⚠️ Siz heniz hiç hili surat ýüklemediňiz!",
        'select_post': "🏢 **Giriş (Serhet)** postyny saýlaň:",
        'select_dest_post': "🏁 **Barmaly ýer (TIF)** postyny saýlaň:",
        'select_viloyat': "🗺 **Haýsy welaýata barýarsyňyz?**\n\nWelaýaty saýlaň:",
        'finish': "✅ **Arzaňyz Admine iberildi!**\n\n🆔 ID: `{code}`\n📄 Suratlar sany: {count}\n\n⏳ Admin jogabyna garaşyň...",
        'settings_title': "⚙️ **Sazlamalar bölümi:**\nMaglumatyňyzy üýtgetmek ýa-da admin bilen aragatnaşyk üçin saýlaň:",
        'cache_cleared': "✅ **Ýat arassalandy!**\nIndi bot köne resminamalaryňyzy ýatda saklamaz.",
        'support_ask': "✍️ **Soragyňyzy ýa-da meseläňizi ýazyň:**\n\nBiziň operatorlarymyz ýakyn wagtda jogap berer.",
        'support_sent': "✅ **Hatyňyz admine iberildi!**\nJogaba şu ýerde garaşyň.",
        'my_apps_empty': "📭 Sizde heniz arzalar ýok.",
        'invoice_msg': "✅ **Arzaňyz tassyklandy!**\n\n🆔 ID: `{code}`\n📦 Ýük göwrümi: **{tier}**\n💰 Töleg möçberi: **{amount} sum**\n\nTöleg usulyny saýlaň:",
        'admin_broadcast': "🔔 **HABAR (Admin):**\n\n{text}",

        # Düwmeler
        'btn_done': "Boldy",
        'btn_yes_auto': "Hawa, ulanalyň",
        'btn_no_auto': "Ýok, täzesini ýüklärin",
        'btn_lang': "Dili üýtgetmek",
        'btn_phone': "Belgini üýtgetmek",
        'btn_clear': "Ýady arassalamak",
        'btn_support': "Admin bilen aragatnaşyk",
        'btn_back': "Yza",
        'btn_cancel': "Ýatyrmak",
        'btn_change_phone': "BELGINI ÜÝTGETMEK",
        'btn_change_lang': "DILI ÜÝTGETMEK",
        'btn_clear_cache': "ÝADY ARASSALAMAK",
        'btn_admin_contact': "ADMIN BILEN ARAGATNAŞYK",
        'btn_search_app': "ARZA GÖZLE",
        'btn_my_apps': "ARZALARYM",
        'btn_cash': "AGENTLER ARKALY NAGT",

        # Ädimler
        'step_1': "1-nji ädim: Belgi", 'step_2': "2-nji ädim: Resminamalar", 'step_3': "3-nji ädim: Post", 'step_4': "4-nji ädim: Barmaly ýer", 'step_5': "Soňy",

        # Baş menýu
        'menu_epi': 'EPI KOD AT DEKLARASIÝA',
        'menu_mb': 'MB DEKLARASIÝA',
        'menu_contacts': 'YNAM TELEFONLARY',
        'menu_apps': 'ARZALARYM',
        'menu_settings': 'SAZLAMALAR',
        'menu_prices': 'BAHALAR KATALOGY',
        'menu_app': 'PROGRAMMANY ÝÜKLE',
        'menu_kgd': 'KGD(E-TRANZIT) GÖRMEK',
        'menu_gabarit': 'GABARIT RUGSAT ALMAK',
        'menu_sugurta': 'ÄTIÝAÇLANDYRYŞ',
        'menu_navbat': 'ELEKTRON NOBAT',
        'menu_yuklar': 'YGTYBARLY ÝÜKLER ALYŞ-SATYŞ',
        'menu_bonus': 'BOT ARKALY BONUS',
        'menu_balance': 'TEŇŇELERIM HASABY',
        'menu_social': 'SOSIAL TORLARY',
        'menu_chat': 'GÜRRÜŇLEŞMEK',

        # EPI we MB
        'epi_start': "📄 **EPI KOD AT DEKLARASIÝA**\n\nSerhet gümrük postyny saýlaň:",
        'mb_start': "📋 **MB DEKLARASIÝA**\n\nSerhet gümrük postyny saýlaň:",
        'select_agent': "👨‍💼 **Agent saýlamak**\n\nAgentleriň birini saýlaň:",
        'enter_car_number': "🚛 **Ulag belgisini giriziň:**\n\n(Mysal: 01A777AA)",
        'docs_epi': "📸 **Resminamalary ýükläň:**\n\n📄 Pasport\n📄 Teh-pasport\n📦 CMR; Inwoýs; Gaplamak sanawy\n📜 Beýleki resminamalar\n\n✅ Ýükläniňizden soň **'Boldy'**-a basyň.",
        'docs_mb': "📸 **Resminamalary ýükläň:**\n\n📄 Pasport\n📄 Teh-pasport\n\n✅ Ýükläniňizden soň **'Boldy'**-a basyň.",
        'waiting_admin': "⏳ **Arzaňyz adminlere iberildi!**\n\n🆔 Arza kody: `{code}`\n\nAdmin jogabyna garaşyň...",
        'price_set': "✅ **Arza tassyklandy!**\n\n💰 Bahasy: **{price} sum**\n\nTöleg görnüşini saýlaň:",

        # Ynam telefonlary
        'contacts_msg': "📞 **YNAM TELEFONLARY**\n\n📱 +998 91 702 00 99\n📱 +998 94 312 00 99\n\n📱 Telegram: @CARAVAN_TRANZIT, @caravan_tranzit1\n\n💬 WhatsApp: +998 91 702 00 99",

        # Bahalar
        'prices_catalog': "<b>🚛 CARAVAN TRANZIT — EPI-KOD HYZMATY</b>\n\nTassyklanan bahalar sanawy:\n\n➖➖➖➖➖➖➖➖➖➖➖\n<b>📦 Kiçi partiýalar:</b>\n▪️ <b>1-2 partiýa:</b> 35 000 sum\n▪️ <b>3 partiýa:</b> 45 000 sum\n\n<b>📈 Uly partiýalar:</b>\n▪️ <b>4 partiýa:</b> 60 000 sum\n▪️ <b>5 partiýa:</b> 75 000 sum\n▪️ <b>6 partiýa:</b> 105 000 sum\n▪️ <b>7 partiýa:</b> 126 000 sum\n▪️ <b>8 partiýa:</b> 144 000 sum\n▪️ <b>9 partiýa:</b> 180 000 sum\n➖➖➖➖➖➖➖➖➖➖➖",

        # Arzalarym
        'apps_menu': "🎫 **ARZALARYM**\n\nSaýlaň:",
        'search_app_car': "🔍 **ARZA GÖZLE**\n\nUlag belgisini giriziň:",
        'app_found': "✅ **Arza tapyldy!**\n\n🆔 Kod: `{code}`\n🚛 Ulag: {car}\n📅 Senesi: {date}\n📊 Ýagdaýy: {status}",
        'app_not_found': "❌ Bu ulag belgisi boýunça arza tapylmady.",
        'my_apps_list': "📂 **SIZIŇ ARZALARYŇYZ:**\n\n{apps}",
        'payment_methods': "💳 **Töleg usulyny saýlaň:**",

        # Sazlamalar
        'settings_menu': "⚙️ **SAZLAMALAR**\n\nSaýlaň:",
        'change_phone_msg': "📱 **Belgini üýtgetmek**\n\nTäze belgiňizi iberiň:",
        'change_lang_msg': "🌐 **Dili üýtgetmek**\n\nDili saýlaň:",
        'clear_cache_msg': "🗑 **Ýady arassalamak**\n\nÄhli saklanan resminamalaryňyz öçüriler. Dowam edýärsiňizmi?",
        'cache_cleared_msg': "✅ Ýat arassalandy!",
        'admin_contact_msg': "👨‍💼 **ADMIN BILEN ARAGATNAŞYK**\n\n📞 Telefon: +998917020099, +998943120099\n📱 Telegram: @CARAVAN_TRANZIT, @caravan_tranzit1\n💬 WhatsApp: +998917020099",

        # Bahalar
        'prices_msg': "💰 **BAHALAR KATALOGY**\n\nÄhli bahalary görmek üçin salgylanma geçiň:",

        # Programma ýüklemek
        'app_download_msg': "📱 **PROGRAMMANY ÝÜKLE**\n\nSaýlaň:",
        'app_link_msg': "🔗 **Programma salgysy:**\n\nÝüklemek üçin basyň",
        'app_guide_msg': "📖 **Ulanmak gollanmasy:**\n\n1. Programmany ýükläň\n2. Gurnaň\n3. Telefon belgiňiz bilen giriň",
        'bonus_guide_msg': "🎁 **Bonus almak gollanmasy:**\n\n👥 Dostuňyz hasaba alynsa: **2,000 teňňe**\n💰 Dostuňyz kod satyn alsa: **17,500 teňňe**\n🎯 Maksat: **35,000 teňňe = 1 MUGT EPI KOD**",

        # KGD
        'kgd_menu_msg': "🚚 **KGD (E-TRANZIT) GÖRMEK**\n\nUsuly saýlaň:",
        'kgd_app_msg': "📱 **Programma arkaly görmek:**",
        'kgd_staff_car': "👥 **Işgärler arkaly görmek**\n\nUlag belgisini giriziň:",
        'kgd_checking': "🔍 Barlanýar... Biraz garaşyň.",

        # Gabarit
        'gabarit_msg': "📜 **GABARIT RUGSAT ALMAK**\n\nRugsat almak üçin admin bilen aragatnaşyk saklanyň:\n\n📱 @CARAVAN_TRANZIT\n📱 @caravan_tranzit1\n\n✍️ \"GABARIT\" diýip ýazyň",

        # Placeholder
        'coming_soon': "🚧 **ÝAKYN WAGTDA**\n\nBu hyzmat ýakyn wagtda işe goýberiler!",

        # Bonus
        'bonus_menu_msg': "🎁 **BOT ARKALY BONUS**\n\nSaýlaň:",
        'get_referral_link': "🔗 **Siziň salgyňyz:**\n\n`{link}`\n\nDostlaryňyza iberiň we bonus ýygnaň!",
        'bonus_info': "ℹ️ **BONUS ULGAMY HAKYNDA:**\n\n🎁 Dostlaryňyzy çagyryň we teňňe ýygnaň!\n\n👥 Dost hasaba alynsa: **2,000 teňňe**\n💰 Dost EPI kod alsa: **17,500 teňňe**\n\n🎯 35,000 teňňe = **1 MUGT EPI KOD**",

        # Teňňeler
        'balance_msg': "💎 **TEŇŇELERIM HASABY**\n\n💰 Siziň balansyňyz: **{balance} teňňe**\n\n🎁 35,000 teňňe = 1 MUGT EPI KOD",

        # Sosial
        'social_msg': "📱 **SOSIAL TORLARY**\n\nBizi sosial torlarda yzarlaň:",

        # Gürrüňleşmek
        'chat_msg': "💬 **GÜRRÜŇLEŞMEK**\n\nSoragyňyzy ýazyň, operator jogap berer:",
        'chat_sent': "✅ Hatyňyz iberildi! Jogaba garaşyň.",
        'chat_continue': "✅ Hatyňyz iberildi! Ýazmagy dowam edip ýa-da söhbeti gutaryp bilersiňiz.",
        'chat_ended': "✅ Söhbet gutardy. Sag boluň!",
        'btn_end_chat': "Söhbeti gutarmak",

        # Düwme tekstleri
        'btn_app_link': 'PROGRAMMANY ÝÜKLEMEK SALGISY',
        'btn_app_guide': 'ULANMAK GOLLANMASY',
        'btn_bonus_guide': 'PROGRAMMA ARKALY BONUS ALMAK GOLLANMASY',
        'btn_kgd_app': 'PROGRAMMA ARKALY GÖRMEK',
        'btn_kgd_staff': 'IŞGÄRLER ARKALY GÖRMEK',
        'btn_download': 'Ýüklemek salgisy',
        'btn_guide_use': 'Ulanmak boýunça gollanma',
        'btn_guide_kgd': 'KGD görmek boýunça gollanma',
        'btn_bonus_rule': 'Bonus almak kadasy',
        'btn_get_link': 'SALGYŇYZY ALYŇ WE DOSTLARYŇYZA IBERIŇ',
        'btn_bonus_info': 'BONUS ULGAMY HAKYNDA DÜŞÜNDIRIŞ',
        'btn_my_coins': 'TEŇŇELERIM',
    },

    # =================================================
    # 10. XITOYCHA (CHINESE)
    # =================================================
    'zh': {
        'start': "🇨🇳 请选择语言:",
        'agreement': "⚠️ **注意！**\n您是否同意海关机关处理您的数据？",
        'ask_phone': "📱 请点击下方的 **'发送号码'** 按钮:",
        'registered': "✅ **注册成功！**\n请选择所需服务:",
        'enter_car': "🚛 输入车牌号 (例: 01A777AA):",
        'autofill_found': "🤖 **自动填充系统:**\n\n尊敬的司机，**{car}** 车辆的旧文件（行驶证、驾驶证）已在数据库中。\n\n**是否使用？**（节省时间）",
        'autofill_used': "✅ **旧文件已加载！**\n\n现在只需拍摄并发送本次行程的新文件（CMR、货运单）。",
        'docs_header': "📸 **上传文件**\n\n请清晰拍摄并发送以下文件:",
        'docs_list_at': "📄 **行驶证**（正反面）\n🪪 **驾驶证**（正反面）\n🚛 **挂车**（行驶证）\n📦 **CMR和发票**\n📜 **证书**\n⚖️ **公证文件**",
        'docs_list_mb': "📄 **行驶证**（正反面）\n🪪 **驾驶证**（正反面）",
        'docs_footer': "\n✅ 上传所有照片后，请点击 **'完成'** 按钮。",
        'zero_photos': "⚠️ 您还没有上传任何照片！",
        'select_post': "🏢 选择 **入境（边境）** 哨所:",
        'select_dest_post': "🏁 选择 **目的地（TIF）** 哨所:",
        'select_viloyat': "🗺 **您要去哪个地区？**\n\n请选择地区:",
        'finish': "✅ **您的申请已发送给管理员！**\n\n🆔 ID: `{code}`\n📄 照片数量: {count}\n\n⏳ 请等待管理员回复...",
        'settings_title': "⚙️ **设置部分:**\n选择更改您的信息或联系管理员:",
        'cache_cleared': "✅ **缓存已清除！**\n机器人将不再记住您的旧文件。",
        'support_ask': "✍️ **写下您的问题或疑问:**\n\n我们的客服人员将尽快回复。",
        'support_sent': "✅ **您的消息已发送给管理员！**\n请在此等待回复。",
        'my_apps_empty': "📭 您还没有申请。",
        'invoice_msg': "✅ **您的申请已确认！**\n\n🆔 ID: `{code}`\n📦 货物量: **{tier}**\n💰 付款金额: **{amount} 苏姆**\n\n请选择付款方式:",
        'admin_broadcast': "🔔 **通知（管理员）:**\n\n{text}",

        # 按钮
        'btn_done': "完成",
        'btn_yes_auto': "是，使用",
        'btn_no_auto': "否，上传新的",
        'btn_lang': "更改语言",
        'btn_phone': "更改号码",
        'btn_clear': "清除缓存",
        'btn_support': "联系管理员",
        'btn_back': "返回",
        'btn_cancel': "取消",
        'btn_change_phone': "更改号码",
        'btn_change_lang': "更改语言",
        'btn_clear_cache': "清除缓存",
        'btn_admin_contact': "联系管理员",
        'btn_search_app': "搜索申请",
        'btn_my_apps': "我的申请",
        'btn_cash': "通过代理现金",

        # 步骤
        'step_1': "步骤1: 号码", 'step_2': "步骤2: 文件", 'step_3': "步骤3: 哨所", 'step_4': "步骤4: 目的地", 'step_5': "完成",

        # 主菜单
        'menu_epi': 'EPI代码AT报关',
        'menu_mb': 'MB报关',
        'menu_contacts': '信任电话',
        'menu_apps': '我的申请',
        'menu_settings': '设置',
        'menu_prices': '价格目录',
        'menu_app': '下载应用',
        'menu_kgd': 'KGD(电子过境)查看',
        'menu_gabarit': '获取超限许可',
        'menu_sugurta': '保险',
        'menu_navbat': '电子排队',
        'menu_yuklar': '可靠货物买卖',
        'menu_bonus': '机器人奖励',
        'menu_balance': '我的金币账户',
        'menu_social': '社交媒体',
        'menu_chat': '聊天',

        # EPI和MB
        'epi_start': "📄 **EPI代码AT报关**\n\n选择边境海关哨所:",
        'mb_start': "📋 **MB报关**\n\n选择边境海关哨所:",
        'select_agent': "👨‍💼 **选择代理**\n\n选择一位代理:",
        'enter_car_number': "🚛 **输入车牌号:**\n\n（例: 01A777AA）",
        'docs_epi': "📸 **上传文件:**\n\n📄 护照\n📄 行驶证\n📦 CMR; 发票; 装箱单\n📜 其他文件\n\n✅ 上传后请点击 **'完成'**。",
        'docs_mb': "📸 **上传文件:**\n\n📄 护照\n📄 行驶证\n\n✅ 上传后请点击 **'完成'**。",
        'waiting_admin': "⏳ **您的申请已发送给管理员！**\n\n🆔 申请代码: `{code}`\n\n请等待管理员回复...",
        'price_set': "✅ **申请已确认！**\n\n💰 价格: **{price} 苏姆**\n\n选择付款方式:",

        # 信任电话
        'contacts_msg': "📞 **信任电话**\n\n📱 +998 91 702 00 99\n📱 +998 94 312 00 99\n\n📱 Telegram: @CARAVAN_TRANZIT, @caravan_tranzit1\n\n💬 WhatsApp: +998 91 702 00 99",

        # 价格
        'prices_catalog': "<b>🚛 CARAVAN TRANZIT — EPI代码服务</b>\n\n批准的价格表:\n\n➖➖➖➖➖➖➖➖➖➖➖\n<b>📦 小批量:</b>\n▪️ <b>1-2批:</b> 35,000 苏姆\n▪️ <b>3批:</b> 45,000 苏姆\n\n<b>📈 大批量:</b>\n▪️ <b>4批:</b> 60,000 苏姆\n▪️ <b>5批:</b> 75,000 苏姆\n▪️ <b>6批:</b> 105,000 苏姆\n▪️ <b>7批:</b> 126,000 苏姆\n▪️ <b>8批:</b> 144,000 苏姆\n▪️ <b>9批:</b> 180,000 苏姆\n➖➖➖➖➖➖➖➖➖➖➖",

        # 我的申请
        'apps_menu': "🎫 **我的申请**\n\n选择:",
        'search_app_car': "🔍 **搜索申请**\n\n输入车牌号:",
        'app_found': "✅ **找到申请！**\n\n🆔 代码: `{code}`\n🚛 车辆: {car}\n📅 日期: {date}\n📊 状态: {status}",
        'app_not_found': "❌ 未找到此车牌号的申请。",
        'my_apps_list': "📂 **您的申请:**\n\n{apps}",
        'payment_methods': "💳 **选择付款方式:**",

        # 设置
        'settings_menu': "⚙️ **设置**\n\n选择:",
        'change_phone_msg': "📱 **更改号码**\n\n发送您的新号码:",
        'change_lang_msg': "🌐 **更改语言**\n\n选择语言:",
        'clear_cache_msg': "🗑 **清除缓存**\n\n所有保存的文件将被删除。继续吗？",
        'cache_cleared_msg': "✅ 缓存已清除！",
        'admin_contact_msg': "👨‍💼 **联系管理员**\n\n📞 电话: +998917020099, +998943120099\n📱 Telegram: @CARAVAN_TRANZIT, @caravan_tranzit1\n💬 WhatsApp: +998917020099",

        # 价格
        'prices_msg': "💰 **价格目录**\n\n点击链接查看所有价格:",

        # 下载应用
        'app_download_msg': "📱 **下载应用**\n\n选择:",
        'app_link_msg': "🔗 **应用链接:**\n\n点击下载",
        'app_guide_msg': "📖 **使用指南:**\n\n1. 下载应用\n2. 安装\n3. 使用手机号登录",
        'bonus_guide_msg': "🎁 **奖励获取指南:**\n\n👥 朋友注册: **2,000 金币**\n💰 朋友购买代码: **17,500 金币**\n🎯 目标: **35,000 金币 = 1个免费EPI代码**",

        # KGD
        'kgd_menu_msg': "🚚 **KGD（电子过境）查看**\n\n选择方式:",
        'kgd_app_msg': "📱 **通过应用查看:**",
        'kgd_staff_car': "👥 **通过员工查看**\n\n输入车牌号:",
        'kgd_checking': "🔍 正在检查...请稍候。",

        # 超限
        'gabarit_msg': "📜 **获取超限许可**\n\n联系管理员获取许可:\n\n📱 @CARAVAN_TRANZIT\n📱 @caravan_tranzit1\n\n✍️ 写 \"超限\"",

        # 占位符
        'coming_soon': "🚧 **即将推出**\n\n此服务即将上线！",

        # 奖励
        'bonus_menu_msg': "🎁 **机器人奖励**\n\n选择:",
        'get_referral_link': "🔗 **您的链接:**\n\n`{link}`\n\n发送给朋友并收集奖励！",
        'bonus_info': "ℹ️ **关于奖励系统:**\n\n🎁 邀请朋友并收集金币！\n\n👥 朋友注册: **2,000 金币**\n💰 朋友获取EPI代码: **17,500 金币**\n\n🎯 35,000 金币 = **1个免费EPI代码**",

        # 金币
        'balance_msg': "💎 **我的金币账户**\n\n💰 您的余额: **{balance} 金币**\n\n🎁 35,000 金币 = 1个免费EPI代码",

        # 社交
        'social_msg': "📱 **社交媒体**\n\n在社交媒体上关注我们:",

        # 聊天
        'chat_msg': "💬 **聊天**\n\n写下您的问题，客服将回复:",
        'chat_sent': "✅ 消息已发送！等待回复。",
        'chat_continue': "✅ 消息已发送！您可以继续写或结束聊天。",
        'chat_ended': "✅ 聊天结束。谢谢！",
        'btn_end_chat': "结束聊天",

        # 按钮文本
        'btn_app_link': '下载应用链接',
        'btn_app_guide': '应用使用指南',
        'btn_bonus_guide': '应用奖励获取指南',
        'btn_kgd_app': '通过应用查看',
        'btn_kgd_staff': '通过员工查看',
        'btn_download': '下载链接',
        'btn_guide_use': '使用指南',
        'btn_guide_kgd': 'KGD查看指南',
        'btn_bonus_rule': '奖励获取规则',
        'btn_get_link': '获取您的链接并发送给朋友',
        'btn_bonus_info': '奖励系统说明',
        'btn_my_coins': '我的金币',
    }
}

# Kamchiliklarni to'ldirish (Agar biror tilda so'z qolib ketsa, O'zbekchadan oladi)
for lang in ['kg', 'tj', 'tr', 'tm', 'zh']:
    for key, val in TEXTS['uz'].items():
        if key not in TEXTS[lang]:
            TEXTS[lang][key] = val
