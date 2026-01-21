# CARAVAN TRANZIT - Customs Logistics Ecosystem 🚛

A comprehensive Telegram Bot ecosystem for customs declarations at border posts, connecting Drivers, Customs Agents, and Administrators.

## 🌟 Key Features

### For Drivers (Users)
- 📱 **Multi-language Support**: 10 languages (Uzbek, Russian, English, Chinese, Turkish, Korean, Kazakh, Kyrgyz, Tajik, Turkmen)
- 📄 **Web App Interface**: Beautiful 3-screen wizard for submitting declarations
- 🚛 **Smart Vehicle Detection**: Auto-formatting for vehicle numbers (01 A 777 AA)
- 💾 **Auto-Fill System**: Saves documents for repeat submissions
- 💰 **Multiple Payment Options**: Click/Payme integration + internal coin system
- 🎁 **Referral Program**: Earn coins by inviting friends

### For Agents (Declarants)
- 📍 **Location-Based Assignment**: Agents linked to specific customs posts
- 🟢 **Online/Offline Status**: Smart routing to available agents
- ⭐ **Rating System**: Track agent performance
- 💰 **Flexible Pricing**: Set custom prices per application

### For Administrators
- 🔔 **Admin Group Integration**: Centralized application management
- 💵 **Pricing Control**: Quick or custom price setting
- 📊 **Transaction Tracking**: Complete payment history
- 🎯 **Status Management**: Track application lifecycle

## 🏗️ Architecture

### Database Schema (PostgreSQL)

```
customs_posts (id, name[JSONB], is_active)
    └── agents (id, full_name, telegram_id, post_id, status, rating)

users (telegram_id, full_name, phone_number, language, balance, referral_source)
    ├── applications (id, app_code, user_id, agent_id, post_id, vehicle_number, vehicle_type, status, price, files[JSONB])
    ├── transactions (id, user_id, application_id, amount, type, status)
    └── referrals (id, referrer_id, referred_id, reward_given)

saved_docs (user_id, car_number, photos[])  -- Auto-fill cache
```

### Project Structure

```
CARAVAN_TRANZIT/
├── main.py                  # Bot entry point
├── database.py              # Database layer (AsyncPG)
├── handlers.py              # Main bot handlers
├── web_app_handlers.py      # Web App data processing
├── admin_handlers.py        # Admin group workflow
├── payment_handlers.py      # Payment processing
├── keyboards.py             # Reply & Inline keyboards
├── strings.py               # Multi-language text (10 languages)
├── states.py                # FSM states
├── schema.sql               # Database schema
├── requirements.txt         # Python dependencies
└── webapp/
    ├── index.html          # Web App UI (TailwindCSS)
    └── app.js              # Web App logic
```

## 🚀 Setup Instructions

### 1. Prerequisites

- Python 3.11+
- PostgreSQL 14+
- Telegram Bot Token (from @BotFather)
- Railway.app account (or other PostgreSQL hosting)

### 2. Environment Variables

Create a `.env` file:

```env
# Telegram Bot
BOT_TOKEN=your_bot_token_here

# Database (Railway provides this automatically)
DATABASE_URL=postgresql://user:pass@host:port/dbname

# Payment Provider (Click/Payme)
PAYMENT_PROVIDER_TOKEN=your_payment_token_here
```

### 3. Database Setup

Option A: Using schema.sql
```bash
psql -U postgres -d your_database -f schema.sql
```

Option B: Automatic (via code)
```bash
# The bot will automatically create tables and seed data on first run
python main.py
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Web App URL

Update `keyboards.py` line 114:
```python
webapp_url = "https://your-domain.com/webapp/index.html"
```

Host the `webapp/` folder on:
- Railway.app Static Files
- GitHub Pages
- Netlify
- Any static hosting service

### 6. Run the Bot

```bash
python main.py
```

## 🎯 User Flow

### Phase 1: Onboarding
1. `/start` → Language selection (10 options)
2. Privacy agreement acceptance
3. Phone number verification

### Phase 2: Declaration Submission (Web App)
1. **Screen 1**: Select customs post → Select online agent
2. **Screen 2**: Enter vehicle number → Choose type (Truck/Car)
3. **Screen 3**: Upload documents (Passport, Tech Passport, Invoice, etc.)
4. Submit → Data sent to bot

### Phase 3: Admin Processing
1. Application card appears in Admin Group
2. Admin reviews documents
3. Admin sets price (Quick: 35k, 45k, 60k or Custom)
4. Invoice sent to user

### Phase 4: Payment & Delivery
1. User pays via Click/Payme or coins (35,000 coins = 1 service)
2. Payment confirmed
3. Application status updated
4. EPI Code (PDF) delivered to user

## 💰 Gamification System

### Coin Economy
- **35,000 coins** = 1 free customs declaration
- Users earn coins through:
  - Referrals: +2,000 coins per invited friend
  - Purchase bonus: +17,500 coins when referred friend makes first purchase

### Referral System
Share your link: `https://t.me/YOUR_BOT_USERNAME?start=YOUR_TELEGRAM_ID`

## 🔧 Configuration

### Admin Group
Set `ADMIN_GROUP_ID` in handler files:
```python
ADMIN_GROUP_ID = -1003463212374  # Your admin group chat ID
```

To get your chat ID:
1. Add bot to group
2. Make bot admin
3. Send a message
4. Check bot logs for chat_id

### Payment Integration

#### Click/Payme Setup
1. Register at [Click](https://click.uz) or [Payme](https://payme.uz)
2. Get merchant credentials
3. Set `PAYMENT_PROVIDER_TOKEN` in `.env`

#### Telegram Payments API
```python
# payment_handlers.py line 18
PAYMENT_PROVIDER_TOKEN = "your_click_or_payme_token"
```

## 📱 Supported Languages

1. 🇺🇿 O'zbekcha (Lotin)
2. 🇺🇿 Ўзбекча (Kirill)
3. 🇷🇺 Русский
4. 🇺🇸 English
5. 🇨🇳 中文
6. 🇹🇷 Türkçe
7. 🇰🇿 Қазақша
8. 🇰🇬 Кыргызча
9. 🇹🇯 Тоҷикӣ
10. 🇹🇲 Turkmençe

## 📊 Database Queries

### Get online agents for a post
```sql
SELECT * FROM agents WHERE post_id = 1 AND status = 'online' ORDER BY rating DESC;
```

### Check user's coins and free services
```sql
SELECT telegram_id, balance, FLOOR(balance / 35000) as free_services
FROM users WHERE telegram_id = 123456789;
```

### Get application history
```sql
SELECT * FROM applications WHERE user_id = 123456789 ORDER BY created_at DESC;
```

### Referral statistics
```sql
SELECT referrer_id, COUNT(*) as referral_count,
       SUM(CASE WHEN reward_given THEN 1 ELSE 0 END) as completed
FROM referrals GROUP BY referrer_id;
```

## 🚢 Deployment (Railway.app)

### 1. Push to GitHub
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

### 2. Deploy on Railway
1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Add PostgreSQL service
5. Set environment variables (BOT_TOKEN)
6. Deploy!

### 3. Host Web App
- Upload `webapp/` folder to Railway Static Files or GitHub Pages
- Update `webapp_url` in `keyboards.py`

## 🔐 Security Notes

- ✅ Never commit `.env` file
- ✅ Use environment variables for all secrets
- ✅ Validate all user inputs
- ✅ Implement rate limiting for production
- ✅ Use HTTPS for Web App hosting
- ✅ Regularly update dependencies

## 🐛 Troubleshooting

### Database Connection Failed
```
❌ XATO: DATABASE_URL topilmadi!
```
**Solution**: Set `DATABASE_URL` in `.env` or Railway environment variables

### Web App Not Loading
```
❌ Invalid app URL
```
**Solution**: Ensure `webapp_url` in `keyboards.py` is a valid HTTPS URL

### Payment Not Working
```
❌ Invalid payment provider token
```
**Solution**: Get correct token from Click/Payme and update `PAYMENT_PROVIDER_TOKEN`

## 📈 Future Enhancements

- [ ] Real-time agent notifications via WebSocket
- [ ] OCR for automatic document parsing
- [ ] Multi-currency support
- [ ] Agent mobile app
- [ ] Analytics dashboard
- [ ] SMS notifications
- [ ] Voice messages support
- [ ] Blockchain-based document verification

## 👥 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit pull request

## 📄 License

This project is proprietary software. All rights reserved.

## 🤝 Support

For support and inquiries:
- 📧 Email: support@caravantranzit.uz
- 💬 Telegram: @caravan_tranzit_support
- 📞 Phone: +998 XX XXX XX XX

## 🎉 Credits

Built with ❤️ by the CARAVAN TRANZIT Team

**Tech Stack**:
- [Aiogram 3.x](https://github.com/aiogram/aiogram) - Modern Telegram Bot framework
- [AsyncPG](https://github.com/MagicStack/asyncpg) - Fast PostgreSQL driver
- [TailwindCSS](https://tailwindcss.com) - Utility-first CSS framework
- [Railway.app](https://railway.app) - Cloud platform

---

**Version**: 1.0.0
**Last Updated**: 2026-01-09
**Status**: Production Ready ✅
