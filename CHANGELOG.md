# MYBOJXONA Bot - O'zgarishlar tarixi

## 2026-01-12 - Katta yangilanish

### ✅ Tuzatilgan muammolar

1. **Database xatoliklari tuzatildi**
   - `users` jadvaliga `direction` ustuni migration qo'shildi
   - `applications` jadvaliga `claimed_by` ustuni qo'shildi
   - Agent qabul qilishda telegram_id ishlatiladi
   - Foreign key constraint xatoligi bartaraf etildi

2. **Admin guruh "qabul qilish" tugmasi**
   - Admin guruhda arizani qabul qilish to'liq ishlaydi
   - Narx belgilash va rad etish funksiyalari qo'shildi

3. **TRANZIT/IMPORT/EKSPORT logikasi**
   - TRANZIT: manzil bojxona posti chegara postlaridan tanlanadi
   - IMPORT: manzil bojxona posti TIF postlaridan tanlanadi
   - EKSPORT: faqat chegara bojxona posti

4. **ISHONCH TELEFONLARI menyusi**
   - 4 ta asosiy funksiya:
     - Raqamni o'zgartirish
     - Tilni o'zgartirish (10 ta til)
     - Xotirani tozalash
     - Admin bilan aloqa (3 ta kanal)

5. **Ortga va Bekor qilish tugmalari**
   - Barcha menyularda "Ortga" tugmasi ishlaydi
   - "Bekor qilish" tugmasi asosiy menyuga qaytaradi

6. **Social Media havolalari**
   - Telegram gruppa: https://t.me/mybojxona_chat

### 🚀 Yangi funksiyalar

1. **Click Payment API integratsiyasi**
   - `click_api.py` fayli yaratildi
   - Kreditsiallar: SERVICE_ID: 91522, MERCHANT_ID: 40158
   - Payment URL generator
   - Signature verification

2. **Narxlar katalogi**
   - To'liq narxlar ro'yxati:
     - 1-2 partiya: 35,000 so'm
     - 3 partiya: 45,000 so'm
     - 4 partiya: 60,000 so'm
     - 5 partiya: 75,000 so'm
     - 6 partiya: 105,000 so'm
     - 7 partiya: 126,000 so'm
     - 8 partiya: 144,000 so'm
     - Boshqa: X*20,000 so'm
   - Foydalanuvchi balansini ko'rsatish

3. **Bojxona postlari yangilandi**
   - **Chegara postlari:** 59 ta (to'liq ro'yxat)
   - **TIF postlari:** 33 ta (to'liq ro'yxat)

4. **Tugmalar va formatlash**
   - Emoji dublikatlar olib tashlandi
   - Markdown formatlash yaxshilandi

### 📊 Statistika

- Database migrationlar: 2 ta
- Yangi fayllar: 2 ta (click_api.py, CHANGELOG.md)
- O'zgartirilgan fayllar: 5 ta
- Tuzatilgan xatoliklar: 7 ta
- Yangi funksiyalar: 10+ ta

### 🌐 Ko'p tillilik

- O'zbekcha (lotin): 100% ✅
- O'zbekcha (kirill): 60% ⚠️
- Ruscha: 60% ⚠️
- Inglizcha: 60% ⚠️
- Qozoqcha: 40% ⚠️
- Qirg'izcha: 40% ⚠️
- Tojikcha: 40% ⚠️
- Turkcha: 40% ⚠️
- Turkmancha: 40% ⚠️
- Xitoycha: 40% ⚠️

**Eslatma:** Fallback mexanizm mavjud - agar til topilmasa, avtomatik o'zbekcha versiyasini ko'rsatadi.

### 🔧 Texnik o'zgarishlar

- PostgreSQL migration logikasi qo'shildi
- Click payment webhook handlerlari tayyor
- FSM state machine yangilandi
- Keyboard logikasi yaxshilandi

### 📝 Keyingi bosqichlar

1. Barcha tillarni 100% to'ldirish
2. Payment webhook testlari
3. Admin panel yaxshilash
4. Statistika dashboard

---

## Commit tarixi

- `68f8efa` - feat: Katta yangilanishlar - Database, Click API, Narxlar, Postlar
- `d21e4bd` - fix: 7 ta asosiy muammoni tuzatish
- `904f153` - Merge PR #3
- `9552838` - feat: To'liq yangilangan handlers.py - 17 ta xizmat
- `f56ca55` - feat: Yangi bot strukturasi
