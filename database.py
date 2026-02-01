import os
import asyncpg
import json
from decimal import Decimal
from dotenv import load_dotenv

load_dotenv()

# Railway avtomat DATABASE_URL beradi.
# Agar u topilmasa, xatolik chiqmasligi uchun bo'sh string beriladi.
DATABASE_URL = os.getenv("DATABASE_URL")

class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        """Baza bilan pool ulanishini hosil qilish"""
        if not self.pool:
            if not DATABASE_URL:
                print("❌ XATO: DATABASE_URL topilmadi! Railway Variables bo'limini tekshiring.")
                return False

            try:
                # Railway Postgres bazasiga ulanish
                self.pool = await asyncpg.create_pool(DATABASE_URL)
                print("✅ Railway Postgres bazasiga muvaffaqiyatli ulandi!")

                # Jadvallarni tekshirish va yaratish
                await self.create_tables()
                return True
            except Exception as e:
                print(f"❌ Baza ulanishida xatolik: {e}")
                return False

    async def create_tables(self):
        """Kerakli jadvallarni yaratish (YANGILANGAN ARXITEKTURA)"""
        async with self.pool.acquire() as conn:
            # 1. CUSTOMS POSTS (Bojxona postlari)
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS customs_posts (
                    id SERIAL PRIMARY KEY,
                    name JSONB NOT NULL,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # 2. USERS (Foydalanuvchilar - Enhanced)
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    telegram_id BIGINT PRIMARY KEY,
                    full_name TEXT,
                    phone_number TEXT,
                    language TEXT DEFAULT 'uz',
                    direction TEXT DEFAULT 'IMPORT',
                    balance DECIMAL(10,2) DEFAULT 0.00,
                    referral_source BIGINT,
                    is_verified BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Migration: direction ustunini qo'shish (agar yo'q bo'lsa)
            try:
                await conn.execute('''
                    ALTER TABLE users ADD COLUMN IF NOT EXISTS direction TEXT DEFAULT 'IMPORT'
                ''')
            except Exception as e:
                print(f"⚠️ Migration warning (users.direction): {e}")

            # 3. AGENTS (Deklarantlar/Agentlar)
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS agents (
                    id SERIAL PRIMARY KEY,
                    telegram_id BIGINT UNIQUE,
                    full_name TEXT NOT NULL,
                    post_id INTEGER REFERENCES customs_posts(id),
                    status TEXT DEFAULT 'offline',
                    rating FLOAT DEFAULT 5.0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # 4. APPLICATIONS (Arizalar - Complete Workflow)
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS applications (
                    id SERIAL PRIMARY KEY,
                    app_code TEXT UNIQUE,
                    user_id BIGINT REFERENCES users(telegram_id),
                    agent_id INTEGER REFERENCES agents(id),
                    claimed_by BIGINT,
                    post_id INTEGER REFERENCES customs_posts(id),
                    vehicle_number TEXT,
                    vehicle_type TEXT DEFAULT 'truck',
                    status TEXT DEFAULT 'new',
                    price DECIMAL(10,2),
                    admin_group_message_id BIGINT,
                    files JSONB,
                    metadata JSONB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Migration: claimed_by ustunini qo'shish (agar yo'q bo'lsa)
            try:
                await conn.execute('''
                    ALTER TABLE applications ADD COLUMN IF NOT EXISTS claimed_by BIGINT
                ''')
            except Exception as e:
                print(f"⚠️ Migration warning (applications.claimed_by): {e}")

            # 5. TRANSACTIONS (To'lovlar tarixi)
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    id SERIAL PRIMARY KEY,
                    user_id BIGINT REFERENCES users(telegram_id),
                    application_id INTEGER REFERENCES applications(id),
                    amount DECIMAL(10,2) NOT NULL,
                    type TEXT NOT NULL,
                    status TEXT DEFAULT 'pending',
                    payment_provider TEXT,
                    payment_id TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # 6. REFERRALS (Referral tizimi)
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS referrals (
                    id SERIAL PRIMARY KEY,
                    referrer_id BIGINT REFERENCES users(telegram_id),
                    referred_id BIGINT REFERENCES users(telegram_id) UNIQUE,
                    reward_given BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Hujjatlar kesh jadvali (Auto-fill uchun) - O'zgarishsiz
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS saved_docs (
                    user_id BIGINT,
                    car_number TEXT,
                    photos TEXT[],
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (user_id, car_number)
                )
            ''')

            print("📊 Baza jadvallari tekshirildi/yaratildi (YANGI ARXITEKTURA).")

    # =============================================================
    # CUSTOMS POSTS METODLARI
    # =============================================================
    async def get_all_posts(self):
        """Barcha aktiv postlarni qaytaradi"""
        async with self.pool.acquire() as conn:
            return await conn.fetch('SELECT * FROM customs_posts WHERE is_active = TRUE ORDER BY id')

    async def get_post_by_id(self, post_id):
        """ID bo'yicha postni qaytaradi"""
        async with self.pool.acquire() as conn:
            return await conn.fetchrow('SELECT * FROM customs_posts WHERE id = $1', post_id)

    async def add_post(self, name_dict):
        """Yangi post qo'shadi (name_dict = {"uz": "Yallama", "ru": "Яллама"})"""
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(
                'INSERT INTO customs_posts (name) VALUES ($1) RETURNING id',
                json.dumps(name_dict)
            )

    # =============================================================
    # AGENTS METODLARI
    # =============================================================
    async def get_agents_by_post(self, post_id, online_only=True):
        """Postga biriktirilgan agentlarni qaytaradi"""
        async with self.pool.acquire() as conn:
            if online_only:
                return await conn.fetch(
                    'SELECT * FROM agents WHERE post_id = $1 AND status = $2 ORDER BY rating DESC',
                    post_id, 'online'
                )
            return await conn.fetch(
                'SELECT * FROM agents WHERE post_id = $1 ORDER BY rating DESC',
                post_id
            )

    async def get_agent_by_id(self, agent_id):
        """ID bo'yicha agentni qaytaradi"""
        async with self.pool.acquire() as conn:
            return await conn.fetchrow('SELECT * FROM agents WHERE id = $1', agent_id)

    async def add_agent(self, full_name, telegram_id, post_id):
        """Yangi agent qo'shadi"""
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(
                'INSERT INTO agents (full_name, telegram_id, post_id) VALUES ($1, $2, $3) RETURNING id',
                full_name, telegram_id, post_id
            )

    async def update_agent_status(self, agent_id, status):
        """Agent statusini o'zgartiradi (online/offline)"""
        async with self.pool.acquire() as conn:
            await conn.execute(
                'UPDATE agents SET status = $2 WHERE id = $1',
                agent_id, status
            )

    # =============================================================
    # USER METODLARI (Enhanced)
    # =============================================================
    async def add_user(self, telegram_id, full_name, phone, lang, direction='IMPORT', referral_source=None):
        """Yangi foydalanuvchi qo'shadi yoki yangilaydi"""
        async with self.pool.acquire() as conn:
            await conn.execute('''
                INSERT INTO users (telegram_id, full_name, phone_number, language, direction, referral_source, is_verified)
                VALUES ($1, $2, $3, $4, $5, $6, TRUE)
                ON CONFLICT (telegram_id) DO UPDATE
                SET language = $4, phone_number = $3, full_name = $2, direction = $5, is_verified = TRUE
            ''', telegram_id, full_name, phone, lang, direction, referral_source)

    async def get_user(self, telegram_id):
        """Foydalanuvchi ma'lumotlarini qaytaradi"""
        async with self.pool.acquire() as conn:
            return await conn.fetchrow('SELECT * FROM users WHERE telegram_id = $1', telegram_id)

    async def update_user_balance(self, telegram_id, amount):
        """Foydalanuvchi balansini yangilaydi"""
        async with self.pool.acquire() as conn:
            await conn.execute(
                'UPDATE users SET balance = balance + $2 WHERE telegram_id = $1',
                telegram_id, amount
            )

    async def get_user_balance(self, telegram_id):
        """Foydalanuvchi balansini qaytaradi"""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow('SELECT balance FROM users WHERE telegram_id = $1', telegram_id)
            return row['balance'] if row else Decimal('0.00')

    # =============================================================
    # APPLICATIONS METODLARI (Complete Workflow)
    # =============================================================
    async def create_application(self, app_code, user_id, app_type='EPI', car_number='', metadata=None):
        """Yangi ariza yaratadi (Soddalashtirilgan)"""
        async with self.pool.acquire() as conn:
            files_data = metadata.get('photos', []) if metadata else []
            return await conn.fetchrow('''
                INSERT INTO applications
                (app_code, user_id, vehicle_number, vehicle_type, files, metadata, status)
                VALUES ($1, $2, $3, $4, $5, $6, 'new')
                RETURNING id
            ''', app_code, user_id, car_number, app_type,
                json.dumps(files_data), json.dumps(metadata or {}))

    async def get_application_by_code(self, app_code):
        """Kod bo'yicha arizani qaytaradi"""
        async with self.pool.acquire() as conn:
            return await conn.fetchrow('SELECT * FROM applications WHERE app_code = $1', app_code)

    async def get_application_by_id(self, app_id):
        """ID bo'yicha arizani qaytaradi"""
        async with self.pool.acquire() as conn:
            return await conn.fetchrow('SELECT * FROM applications WHERE id = $1', app_id)

    async def get_user_apps(self, user_id):
        """Foydalanuvchining barcha arizalarini qaytaradi"""
        async with self.pool.acquire() as conn:
            return await conn.fetch(
                'SELECT * FROM applications WHERE user_id = $1 ORDER BY created_at DESC',
                user_id
            )

    async def update_application_status(self, app_code, status):
        """Ariza statusini yangilaydi"""
        async with self.pool.acquire() as conn:
            await conn.execute(
                'UPDATE applications SET status = $2, updated_at = CURRENT_TIMESTAMP WHERE app_code = $1',
                app_code, status
            )

    async def update_application_price(self, app_code, price):
        """Ariza narxini belgilaydi va statusni 'priced' ga o'zgartiradi"""
        async with self.pool.acquire() as conn:
            await conn.execute('''
                UPDATE applications
                SET price = $2, status = 'priced', updated_at = CURRENT_TIMESTAMP
                WHERE app_code = $1
            ''', app_code, price)

    async def update_admin_message_id(self, app_code, message_id):
        """Admin guruhidagi xabar ID sini saqlaydi"""
        async with self.pool.acquire() as conn:
            await conn.execute(
                'UPDATE applications SET admin_group_message_id = $2 WHERE app_code = $1',
                app_code, message_id
            )

    async def claim_application(self, code, admin_telegram_id):
        """Admin arizani qabul qiladi"""
        async with self.pool.acquire() as conn:
            res = await conn.execute('''
                UPDATE applications SET claimed_by = $2, status = 'processing'
                WHERE app_code = $1 AND claimed_by IS NULL
            ''', code, admin_telegram_id)
            return res == "UPDATE 1"

    async def get_app_by_code(self, app_code):
        """Kod bo'yicha arizani qaytaradi (compat)"""
        return await self.get_application_by_code(app_code)

    async def get_app_by_car_number(self, car_number):
        """Mashina raqami bo'yicha so'nggi arizani qaytaradi"""
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(
                'SELECT * FROM applications WHERE vehicle_number = $1 ORDER BY created_at DESC LIMIT 1',
                car_number
            )

    async def update_status(self, app_code, status):
        """Ariza statusini yangilaydi (compat)"""
        await self.update_application_status(app_code, status)

    # =============================================================
    # TRANSACTIONS & PAYMENTS
    # =============================================================
    async def create_transaction(self, user_id, application_id, amount, trans_type, payment_provider=None):
        """Yangi tranzaksiya yaratadi"""
        async with self.pool.acquire() as conn:
            return await conn.fetchrow('''
                INSERT INTO transactions
                (user_id, application_id, amount, type, payment_provider, status)
                VALUES ($1, $2, $3, $4, $5, 'pending')
                RETURNING id
            ''', user_id, application_id, amount, trans_type, payment_provider)

    async def update_transaction_status(self, transaction_id, status, payment_id=None):
        """Tranzaksiya statusini yangilaydi"""
        async with self.pool.acquire() as conn:
            await conn.execute(
                'UPDATE transactions SET status = $2, payment_id = $3 WHERE id = $1',
                transaction_id, status, payment_id
            )

    async def get_transaction_by_payment_id(self, payment_id):
        """Payme/Click payment ID bo'yicha tranzaksiyani topadi"""
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(
                'SELECT * FROM transactions WHERE payment_id = $1 ORDER BY created_at DESC LIMIT 1',
                payment_id
            )

    # =============================================================
    # REFERRALS & GAMIFICATION
    # =============================================================
    async def create_referral(self, referrer_id, referred_id):
        """Yangi referral yaratadi"""
        async with self.pool.acquire() as conn:
            try:
                await conn.execute('''
                    INSERT INTO referrals (referrer_id, referred_id)
                    VALUES ($1, $2)
                ''', referrer_id, referred_id)
                # Referral bonus berish (2000 coins)
                await self.update_user_balance(referrer_id, Decimal('2000.00'))
                return True
            except:
                return False

    async def mark_referral_reward(self, referred_id):
        """Referral reward berilganligini belgilaydi (17500 coins)"""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                'SELECT referrer_id FROM referrals WHERE referred_id = $1 AND reward_given = FALSE',
                referred_id
            )
            if row:
                await conn.execute(
                    'UPDATE referrals SET reward_given = TRUE WHERE referred_id = $1',
                    referred_id
                )
                await self.update_user_balance(row['referrer_id'], Decimal('17500.00'))
                return row['referrer_id']
            return None

    # =============================================================
    # AUTO-FILL METODLARI (Hujjatlarni eslab qolish)
    # =============================================================
    async def save_car_docs(self, user_id, car, photos):
        """Mashina hujjatlarini saqlaydi (Auto-Fill uchun)"""
        async with self.pool.acquire() as conn:
            await conn.execute('''
                INSERT INTO saved_docs (user_id, car_number, photos, updated_at)
                VALUES ($1, $2, $3, CURRENT_TIMESTAMP)
                ON CONFLICT (user_id, car_number) DO UPDATE SET photos = $3, updated_at = CURRENT_TIMESTAMP
            ''', user_id, car, photos)

    async def get_saved_docs(self, user_id, car):
        """Saqlangan hujjatlarni qaytaradi"""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow('SELECT photos FROM saved_docs WHERE user_id = $1 AND car_number = $2', user_id, car)
            return row['photos'] if row else None

    async def clear_user_cache(self, user_id):
        """Foydalanuvchining barcha saqlangan hujjatlarini o'chiradi"""
        async with self.pool.acquire() as conn:
            await conn.execute('DELETE FROM saved_docs WHERE user_id = $1', user_id)

    # =============================================================
    # SEED DATA - MA'LUMOTLARNI TO'LDIRISH
    # =============================================================
    async def seed_customs_posts(self):
        """Bojxona postlarini bazaga kiritadi"""
        async with self.pool.acquire() as conn:
            # Mavjud postlar sonini tekshiramiz
            count = await conn.fetchval('SELECT COUNT(*) FROM customs_posts')
            if count > 0:
                print("⏩ Customs posts allaqachon mavjud.")
                return

            posts_data = [
                {"uz": "Yallama", "ru": "Яллама", "en": "Yallama"},
                {"uz": "Olot", "ru": "Олот", "en": "Olot"},
                {"uz": "Doʻstlik (Andijon)", "ru": "Дустлик (Андижан)", "en": "Dustlik (Andijan)"},
                {"uz": "S. Najimov", "ru": "С. Наджимов", "en": "S. Najimov"},
                {"uz": "Dovut-ota", "ru": "Довут-ота", "en": "Dovut-ota"},
                {"uz": "Sirdaryo", "ru": "Сырдарья", "en": "Syrdarya"},
                {"uz": "Ayritom", "ru": "Айритом", "en": "Ayritom"},
                {"uz": "Jartepa", "ru": "Жартепа", "en": "Jartepa"},
                {"uz": "Oʻzbekiston", "ru": "Узбекистан", "en": "Uzbekistan"},
                {"uz": "Oybek", "ru": "Ойбек", "en": "Oybek"},
            ]

            for post_name in posts_data:
                await conn.execute(
                    'INSERT INTO customs_posts (name) VALUES ($1)',
                    json.dumps(post_name)
                )

            print("✅ Customs posts bazaga kiritildi!")

    async def seed_test_agents(self):
        """Test agentlarni bazaga kiritadi"""
        async with self.pool.acquire() as conn:
            count = await conn.fetchval('SELECT COUNT(*) FROM agents')
            if count > 0:
                print("⏩ Agents allaqachon mavjud.")
                return

            # Har bir post uchun 2-3 ta test agent qo'shamiz
            test_agents = [
                ("Ali Valiyev", None, 1, 'online'),  # Yallama
                ("Sardor Karimov", None, 1, 'online'),  # Yallama
                ("Dilshod Toshev", None, 2, 'online'),  # Olot
                ("Jahongir Rahimov", None, 3, 'offline'),  # Doʻstlik
            ]

            for agent in test_agents:
                await conn.execute(
                    'INSERT INTO agents (full_name, telegram_id, post_id, status) VALUES ($1, $2, $3, $4)',
                    agent[0], agent[1], agent[2], agent[3]
                )

            print("✅ Test agents bazaga kiritildi!")

db = Database()
