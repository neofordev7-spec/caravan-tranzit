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
        'registered': "✅ **Муваффақиятли!** Хизмат турини танланг:",
        'enter_car': "🚛 Машина рақамини ёзинг (Мисол: 01A777AA):",
        'autofill_found': "🤖 **Авто-Тўлдириш:**\n\nҲурматли ҳайдовчи, **{car}** машинаси учун эски ҳужжатларингиз базада бор.\n\n**Ўшаларни ишлатайми?**",
        'autofill_used': "✅ **Эски ҳужжатлар олинди!**\n\nФақат янги юк хатларини (CMR) ташланг.",
        'docs_header': "📸 **Ҳужжатларни юклаш**\n\nҚуйидагиларни расмга олиб ташланг:",
        'docs_list_at': "📄 **Тех-паспорт**\n🪪 **Права**\n🚛 **Тиркама**\n📦 **CMR ва Инвойс**\n📜 **Сертификатлар**\n⚖️ **Нотариал ҳужжатлар**",
        'docs_list_mb': "📄 **Тех-паспорт**\n🪪 **Права**",
        'docs_footer': "\n✅ Тугатгач **'Юклаб бўлдим'** тугмасини босинг.",
        'zero_photos': "⚠️ Сиз ҳали расм юкламадингиз!",
        'select_post': "🏢 **Кириш (Чегара)** постини танланг:",
        'select_dest_post': "🏁 **Манзил (ТИФ)** постини танланг:",
        'finish': "✅ **Аризангиз юборилди!**\n\n🆔 ID: `{code}`\n⏳ Админ жавобини кутинг...",
        'settings_title': "⚙️ **Созламалар:**",
        'cache_cleared': "✅ **Хотира тозаланди!**",
        'support_ask': "✍️ **Саволингизни ёзинг:**",
        'support_sent': "✅ **Хабар админга юборилди!**",
        'invoice_msg': "✅ **Ариза тасдиқланди!**\n\n🆔 ID: `{code}`\n💰 Тўлов: **{amount} сўм**",
        'admin_broadcast': "🔔 **ЯНГИЛИК (Админ):**\n\n{text}",
        'btn_done': "✅ Юклаб бўлдим", 'btn_yes_auto': "✅ Ҳа, ишлатамиз", 'btn_no_auto': "🔄 Йўқ, янги",
        'btn_lang': "🌐 Тил", 'btn_phone': "📞 Рақам", 'btn_clear': "🗑 Тозалаш", 'btn_support': "📞 Админ билан алоқа", 'btn_back': "⬅️ Орқага", 'btn_cancel': "❌ Бекор қилиш",
        'step_1': "1-қадам", 'step_2': "2-қадам", 'step_3': "3-қадам", 'step_4': "4-қадам", 'step_5': "Якунлаш"
    },

    # =================================================
    # 3. RUSCHA (РУССКИЙ)
    # =================================================
    'ru': {
        'start': "🇷🇺 Пожалуйста, выберите язык:",
        'agreement': "⚠️ **Внимание!**\nВы согласны на обработку данных таможенными органами?",
        'ask_phone': "📱 Пожалуйста, нажмите кнопку **'Отправить номер'**:",
        'registered': "✅ **Регистрация прошла успешно!** Выберите услугу:",
        'enter_car': "🚛 Введите номер авто (Пример: 01A777AA):",
        'autofill_found': "🤖 **Автозаполнение:**\n\nУважаемый водитель, для машины **{car}** есть сохраненные документы.\n\n**Использовать их?** (Это сэкономит время)",
        'autofill_used': "✅ **Старые документы добавлены!**\n\nТеперь отправьте только новые документы (CMR, Инвойс).",
        'docs_header': "📸 **Загрузка документов**\n\nСфотографируйте и отправьте следующие документы:",
        'docs_list_at': "📄 **Техпаспорт**\n🪪 **Права**\n🚛 **Прицеп**\n📦 **CMR и Инвойс**\n📜 **Сертификаты**\n⚖️ **Нотариальные док.**",
        'docs_list_mb': "📄 **Техпаспорт**\n🪪 **Права**",
        'docs_footer': "\n✅ Нажмите **'Загрузил'**, когда закончите.",
        'zero_photos': "⚠️ Вы еще не загрузили фото!",
        'select_post': "🏢 Выберите пост **Въезда**:",
        'select_dest_post': "🏁 Выберите пост **Назначения (ТЭД)**:",
        'finish': "✅ **Заявка отправлена!**\n\n🆔 ID: `{code}`\n📄 Фотографий: {count}\n\n⏳ Ждите ответа администратора...",
        'settings_title': "⚙️ **Настройки:**",
        'cache_cleared': "✅ **Память очищена!**",
        'support_ask': "✍️ **Напишите ваш вопрос или проблему:**",
        'support_sent': "✅ **Сообщение отправлено админу!**",
        'invoice_msg': "✅ **Заявка принята!**\n\n🆔 ID: `{code}`\n📦 Тип: **{tier}**\n💰 К оплате: **{amount} сум**",
        'admin_broadcast': "🔔 **ОПОВЕЩЕНИЕ (Админ):**\n\n{text}",
        'btn_done': "✅ Загрузил", 'btn_yes_auto': "✅ Да, использовать", 'btn_no_auto': "🔄 Нет, новые",
        'btn_lang': "🌐 Язык", 'btn_phone': "📞 Номер", 'btn_clear': "🗑 Очистить память", 'btn_support': "📞 Связь с админом", 'btn_back': "⬅️ Назад", 'btn_cancel': "❌ Отмена",
        'step_1': "Шаг 1", 'step_2': "Шаг 2", 'step_3': "Шаг 3", 'step_4': "Шаг 4", 'step_5': "Финиш"
    },

    # =================================================
    # 4. INGLIZCHA (ENGLISH)
    # =================================================
    'en': {
        'start': "🇺🇸 Please select your language:",
        'agreement': "⚠️ **Attention!**\nDo you agree to your data being processed by customs authorities?",
        'ask_phone': "📱 Please click the **'Send Number'** button below:",
        'registered': "✅ **Registration successful!** Choose a service:",
        'enter_car': "🚛 Enter vehicle number (Ex: 01A777AA):",
        'autofill_found': "🤖 **Auto-Fill:**\n\nDear driver, saved documents found for **{car}**.\n\n**Use them?** (Saves time)",
        'autofill_used': "✅ **Saved docs added!**\n\nNow upload only new shipment docs (CMR, Invoice).",
        'docs_header': "📸 **Upload Documents**\n\nPlease take photos of:",
        'docs_list_at': "📄 **Tech Passport**\n🪪 **License**\n🚛 **Trailer**\n📦 **CMR & Invoice**\n📜 **Certificates**",
        'docs_list_mb': "📄 **Tech Passport**\n🪪 **License**",
        'docs_footer': "\n✅ Click **'Done'** when finished.",
        'zero_photos': "⚠️ You haven't uploaded any photos!",
        'select_post': "🏢 Select **Entry** Post:",
        'select_dest_post': "🏁 Select **Destination** Post:",
        'finish': "✅ **Application Sent!**\n\n🆔 ID: `{code}`\n⏳ Wait for admin reply...",
        'settings_title': "⚙️ **Settings:**",
        'cache_cleared': "✅ **Cache cleared!**",
        'support_ask': "✍️ **Write your question:**",
        'support_sent': "✅ **Sent to admin!**",
        'invoice_msg': "✅ **Application Approved!**\n\n🆔 ID: `{code}`\n💰 Amount: **{amount} UZS**",
        'admin_broadcast': "🔔 **NOTIFICATION:**\n\n{text}",
        'btn_done': "✅ Done", 'btn_yes_auto': "✅ Yes, use saved", 'btn_no_auto': "🔄 No, upload new",
        'btn_lang': "🌐 Language", 'btn_phone': "📞 Phone", 'btn_clear': "🗑 Clear Cache", 'btn_support': "📞 Support", 'btn_back': "⬅️ Back", 'btn_cancel': "❌ Cancel",
        'step_1': "Step 1", 'step_2': "Step 2", 'step_3': "Step 3", 'step_4': "Step 4", 'step_5': "Finish"
    },

    # =================================================
    # 5. QOZOQCHA (QAZAQ)
    # =================================================
    'kz': {
        'start': "🇰🇿 Тілді таңдаңыз:",
        'agreement': "⚠️ **Назар аударыңыз!**\nДеректерді өңдеуге келісесіз бе?",
        'ask_phone': "📱 **'Телефон нөмірін жіберу'** түймесін басыңыз:",
        'registered': "✅ **Сәтті!** Қызметті таңдаңыз:",
        'enter_car': "🚛 Көлік нөмірін енгізіңіз (Мысалы: 01A777AA):",
        'autofill_found': "🤖 **Автотолтыру:**\n\n**{car}** үшін ескі құжаттар табылды.\n\n**Қолданамыз ба?**",
        'autofill_used': "✅ **Құжаттар қосылды!**\n\nТек жаңа CMR жіберіңіз.",
        'docs_header': "📸 **Құжаттарды жүктеу:**",
        'docs_list_at': "📄 Тех-паспорт, Куәлік, Тіркеме, CMR, Сертификаттар",
        'docs_list_mb': "📄 Тех-паспорт, Куәлік",
        'docs_footer': "\n✅ Болған соң **'Болды'** батырмасын басыңыз.",
        'zero_photos': "⚠️ Фото жоқ!",
        'select_post': "🏢 **Кіру** бекеті:",
        'select_dest_post': "🏁 **Бару** бекеті:",
        'finish': "✅ **Жіберілді!**\n\n🆔 ID: `{code}`",
        'settings_title': "⚙️ **Баптаулар:**",
        'cache_cleared': "✅ **Тазаланды!**",
        'support_ask': "✍️ **Сұрағыңызды жазыңыз:**",
        'support_sent': "✅ **Админге жіберілді!**",
        'invoice_msg': "✅ **Қабылданды!**\n\n🆔 ID: `{code}`\n💰 Төлем: **{amount} сум**",
        'admin_broadcast': "🔔 **ХАБАРЛАМА:**\n\n{text}",
        'btn_done': "✅ Болды", 'btn_yes_auto': "✅ Иә", 'btn_no_auto': "🔄 Жоқ",
        'btn_lang': "🌐 Тіл", 'btn_phone': "📞 Нөмір", 'btn_clear': "🗑 Тазалау", 'btn_support': "📞 Админ", 'btn_back': "⬅️ Артқа", 'btn_cancel': "❌ Бас тарту",
        'step_1': "1-қадам", 'step_2': "2-қадам", 'step_3': "3-қадам", 'step_4': "4-қадам", 'step_5': "Аяқтау"
    },

    # =================================================
    # 6. QIRG'IZCHA (KYRGYZ)
    # =================================================
    'kg': {
        'start': "🇰🇬 Тилди тандаңыз:",
        'agreement': "⚠️ Маалыматтарды иштетүүгө макулсузбу?",
        'ask_phone': "📱 Телефон номериңизди жөнөтүңүз:",
        'registered': "✅ Ийгиликтүү! Кызматты тандаңыз:",
        'enter_car': "🚛 Унаа номерин жазыңыз:",
        'autofill_found': "🤖 **Авто-Толтуруу:**\n**{car}** үчүн документтер бар. Колдонолубу?",
        'autofill_used': "✅ Документтер кошулду! Жаңы CMR жөнөтүңүз.",
        'docs_header': "📸 Документтерди сүрөткө тартыңыз:",
        'docs_list_at': "📄 Тех-паспорт, Права, Тиркеме, CMR",
        'docs_footer': "\n✅ Бүткөндө **'Бүттүм'** баскычын басыңыз.",
        'select_post': "🏢 Кирүү посту:",
        'finish': "✅ Жөнөтүлдү! ID: `{code}`",
        'btn_done': "✅ Бүттүм", 'btn_yes_auto': "✅ Ооба", 'btn_no_auto': "🔄 Жок",
        'btn_support': "📞 Админ менен байланыш", 'btn_back': "⬅️ Артына",
        'step_1': "1-кадам", 'step_2': "2-кадам", 'step_3': "3-кадам", 'step_4': "4-кадам", 'step_5': "Бүтүү"
    },

    # =================================================
    # 7. TOJIKCHA (TAJIK)
    # =================================================
    'tj': {
        'start': "🇹🇯 Забонро интихоб кунед:",
        'agreement': "⚠️ Оё шумо ба коркарди маълумот розиед?",
        'ask_phone': "📱 Рақами телефони худро фиристед:",
        'registered': "✅ Муваффақият! Хизматро интихоб кунед:",
        'enter_car': "🚛 Рақами мошинро ворид кунед:",
        'autofill_found': "🤖 Ҳуҷҷатҳои **{car}** ёфт шуданд. Истифода барем?",
        'autofill_used': "✅ Ҳуҷҷатҳо илова шуданд!",
        'docs_header': "📸 Сурати ҳуҷҷатҳоро фиристед:",
        'docs_list_at': "📄 Тех-паспорт, Права, Прицеп, CMR",
        'docs_footer': "\n✅ Тугмаи **'Тайёр'**-ро пахш кунед.",
        'finish': "✅ Фиристода шуд! ID: `{code}`",
        'btn_done': "✅ Тайёр", 'btn_yes_auto': "✅ Ҳа", 'btn_no_auto': "🔄 Не",
        'btn_support': "📞 Админ", 'btn_back': "⬅️ Бозгашт",
        'step_1': "Қадами 1", 'step_2': "Қадами 2", 'step_3': "Қадами 3", 'step_4': "Қадами 4", 'step_5': "Анҷом"
    },

    # =================================================
    # 8. TURKCHA (TURKISH)
    # =================================================
    'tr': {
        'start': "🇹🇷 Lütfen dil seçin:",
        'agreement': "⚠️ Veri işlemeyi kabul ediyor musunuz?",
        'ask_phone': "📱 Lütfen numaranızı gönderin:",
        'registered': "✅ Başarılı! Hizmeti seçin:",
        'enter_car': "🚛 Araç plakasını girin:",
        'autofill_found': "🤖 **{car}** için kayıtlı belgeler var. Kullanılsın mı?",
        'docs_header': "📸 Belgeleri yükleyin:",
        'docs_list_at': "📄 Ruhsat, Ehliyet, Dorse, CMR",
        'docs_footer': "\n✅ Bitince **'Tamam'**a basın.",
        'finish': "✅ Gönderildi! ID: `{code}`",
        'btn_done': "✅ Tamam", 'btn_yes_auto': "✅ Evet", 'btn_no_auto': "🔄 Hayır",
        'btn_support': "📞 Destek", 'btn_back': "⬅️ Geri",
        'step_1': "Adım 1", 'step_2': "Adım 2", 'step_3': "Adım 3", 'step_4': "Adım 4", 'step_5': "Bitiş"
    },

    # =================================================
    # 9. TURKMANCHA (TURKMEN)
    # =================================================
    'tm': {
        'start': "🇹🇲 Dili saýlaň:",
        'agreement': "⚠️ Maglumatlary işlemäge razylyk berýärsiňizmi?",
        'ask_phone': "📱 Telefon belgiňizi iberiň:",
        'registered': "✅ Üstünlikli! Hyzmaty saýlaň:",
        'enter_car': "🚛 Ulag belgisini ýazyň:",
        'autofill_found': "🤖 **{car}** üçin resminamalar bar. Ulanalyňmy?",
        'docs_header': "📸 Resminamalary ýükläň:",
        'docs_list_at': "📄 Teh-pasport, Şahadatnama, CMR",
        'finish': "✅ Iberildi! ID: `{code}`",
        'btn_done': "✅ Boldu", 'btn_yes_auto': "✅ Hawa", 'btn_no_auto': "🔄 Ýok",
        'btn_support': "📞 Admin", 'btn_back': "⬅️ Yza",
        'step_1': "1-nji ädim", 'step_2': "2-nji ädim", 'step_3': "3-nji ädim", 'step_4': "4-nji ädim", 'step_5': "Soňy"
    },

    # =================================================
    # 10. XITOYCHA (CHINESE)
    # =================================================
    'zh': {
        'start': "🇨🇳 请选择语言:",
        'agreement': "⚠️ 您同意数据处理吗？",
        'ask_phone': "📱 请发送您的电话号码:",
        'registered': "✅ 成功！选择服务:",
        'enter_car': "🚛 输入车牌号 (例: 01A777AA):",
        'autofill_found': "🤖 **自动填充:**\n\n发现 **{car}** 的保存文件。使用吗？",
        'autofill_used': "✅ **已添加文件！** 请仅发送新的 CMR。",
        'docs_header': "📸 **上传文件:**",
        'docs_list_at': "📄 行驶证, 驾驶证, 拖车证, CMR, 发票",
        'docs_list_mb': "📄 行驶证, 驾驶证",
        'docs_footer': "\n✅ 完成后点击 **完成**。",
        'select_post': "🏢 选择 **入境** 哨所:",
        'select_dest_post': "🏁 选择 **目的地** 哨所:",
        'finish': "✅ **已发送！**\n\n🆔 ID: `{code}`",
        'settings_title': "⚙️ **设置:**",
        'cache_cleared': "✅ **缓存已清除！**",
        'support_ask': "✍️ **写下您的问题:**",
        'support_sent': "✅ **已发送给管理员！**",
        'invoice_msg': "✅ **申请已批准！**\n\n🆔 ID: `{code}`\n💰 金额: **{amount} UZS**",
        'admin_broadcast': "🔔 **通知:**\n\n{text}",
        'btn_done': "✅ 完成", 'btn_yes_auto': "✅ 是的", 'btn_no_auto': "🔄 不，新的",
        'btn_lang': "🌐 语言", 'btn_phone': "📞 电话", 'btn_clear': "🗑 清除", 'btn_support': "📞 支持", 'btn_back': "⬅️ 返回", 'btn_cancel': "❌ 取消",
        'step_1': "步骤 1", 'step_2': "步骤 2", 'step_3': "步骤 3", 'step_4': "步骤 4", 'step_5': "结束"
    }
}

# Kamchiliklarni to'ldirish (Agar biror tilda so'z qolib ketsa, O'zbekchadan oladi)
for lang in ['kg', 'tj', 'tr', 'tm', 'zh']:
    for key, val in TEXTS['uz'].items():
        if key not in TEXTS[lang]:
            TEXTS[lang][key] = val
