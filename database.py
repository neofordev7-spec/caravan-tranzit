import os
import asyncpg
import json
import logging
from decimal import Decimal
from dotenv import load_dotenv

load_dotenv()

# Loglarni sozlash
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        """Baza bilan pool ulanishini hosil qilish"""
        if not self.pool:
            if not DATABASE_URL:
                logger.error("❌ DATABASE_URL topilmadi!")
                return False
            try:
                self.pool = await asyncpg.create_pool(
                    DATABASE_URL,
                    min_size=5,
                    max_size=20,
                    command_timeout=60
                )
                logger.info("✅ Railway Postgres bazasiga xavfsiz ulanish hosil qilindi.")
                await self.create_tables()
                return True
            except Exception as e:
                logger.error(f"❌ Baza ulanishida xatolik: {e}")
                return False

    async def close(self):
        """Database pool ni yopish"""
        if self.pool:
            await self.pool.close()
            self.pool = None

    async def create_tables(self):
        """Jadvallarni kiberxavfsizlikka muvofiq yaratish"""
        async with self.pool.acquire() as conn:
            # 1. Customs Posts
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS customs_posts (
                    id SERIAL PRIMARY KEY,
                    name JSONB NOT NULL,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            # 2. Users
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
            # 3. Agents
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
            # 4. Applications
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
            # 5. Transactions
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
                    create_time BIGINT,
                    perform_time BIGINT,
                    cancel_time BIGINT,
                    cancel_reason INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            # 6. Referrals
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS referrals (
                    id SERIAL PRIMARY KEY,
                    referrer_id BIGINT REFERENCES users(telegram_id),
                    referred_id BIGINT REFERENCES users(telegram_id) UNIQUE,
                    reward_given BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            # 7. Saved Docs
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS saved_docs (
                    user_id BIGINT,
                    car_number TEXT,
                    photos TEXT[],
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (user_id, car_number)
                )
            ''')
            logger.info("📊 Baza jadvallari kiberxavfsizlikka muvofiq yangilandi.")

    # --- MAIN.PY QIDIRAYOTGAN FUNKSIYALAR (QAYTARILDI) ---

    async def seed_customs_posts(self):
        """Bojxona postlarini bazaga kiritadi"""
        async with self.pool.acquire() as conn:
            count = await conn.fetchval('SELECT COUNT(*) FROM customs_posts')
            if count > 0:
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
                await conn.execute('INSERT INTO customs_posts (name) VALUES ($1)', json.dumps(post_name))
            logger.info("✅ Customs posts bazaga kiritildi!")

    async def seed_test_agents(self):
        """Test agentlarni bazaga kiritadi"""
        async with self.pool.acquire() as conn:
            count = await conn.fetchval('SELECT COUNT(*) FROM agents')
            if count > 0:
                return
            test_agents = [
                ("Ali Valiyev", None, 1, 'online'),
                ("Sardor Karimov", None, 1, 'online'),
                ("Dilshod Toshev", None, 2, 'online'),
                ("Jahongir Rahimov", None, 3, 'offline'),
            ]
            for agent in test_agents:
                await conn.execute(
                    'INSERT INTO agents (full_name, telegram_id, post_id, status) VALUES ($1, $2, $3, $4)',
                    agent[0], agent[1], agent[2], agent[3]
                )
            logger.info("✅ Test agents bazaga kiritildi!")

    # --- USER VA ARIZA METODLARI ---

    async def add_user(self, telegram_id, full_name, phone, lang, direction='IMPORT', referral_source=None):
        async with self.pool.acquire() as conn:
            await conn.execute('''
                INSERT INTO users (telegram_id, full_name, phone_number, language, direction, referral_source, is_verified)
                VALUES ($1, $2, $3, $4, $5, $6, TRUE)
                ON CONFLICT (telegram_id) DO UPDATE
                SET language = $4, phone_number = $3, full_name = $2, direction = $5, is_verified = TRUE
            ''', telegram_id, full_name, phone, lang, direction, referral_source)

    async def get_user(self, telegram_id):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow('SELECT * FROM users WHERE telegram_id = $1', telegram_id)

    async def create_application(self, app_code, user_id, app_type='EPI', car_number='', metadata=None):
        async with self.pool.acquire() as conn:
            files_data = metadata.get('photos', []) if metadata else []
            return await conn.fetchrow('''
                INSERT INTO applications
                (app_code, user_id, vehicle_number, vehicle_type, files, metadata, status)
                VALUES ($1, $2, $3, $4, $5, $6, 'new')
                RETURNING id
            ''', app_code, user_id, car_number, app_type, json.dumps(files_data), json.dumps(metadata or {}))

    async def get_application_by_code(self, app_code):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow('SELECT * FROM applications WHERE app_code = $1', app_code)

    async def get_application_by_id(self, app_id):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow('SELECT * FROM applications WHERE id = $1', app_id)

    async def update_application_status(self, app_code, status):
        async with self.pool.acquire() as conn:
            await conn.execute(
                'UPDATE applications SET status = $2, updated_at = CURRENT_TIMESTAMP WHERE app_code = $1',
                app_code, status
            )

    async def create_transaction(self, user_id, application_id, amount, trans_type,
                                payment_provider=None, payment_id=None, create_time=None):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow('''
                INSERT INTO transactions
                (user_id, application_id, amount, type, payment_provider, payment_id, status, create_time)
                VALUES ($1, $2, $3, $4, $5, $6, 'pending', $7)
                RETURNING *
            ''', user_id, application_id, amount, trans_type, payment_provider, payment_id, create_time)

    async def update_transaction_status(self, transaction_id, status, payment_id=None,
                                        perform_time=None, cancel_time=None, cancel_reason=None):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow('''
                UPDATE transactions
                SET status = $2,
                    payment_id = COALESCE($3, payment_id),
                    perform_time = COALESCE(perform_time, $4),
                    cancel_time = COALESCE(cancel_time, $5),
                    cancel_reason = COALESCE(cancel_reason, $6)
                WHERE id = $1
                RETURNING *
            ''', transaction_id, status, payment_id, perform_time, cancel_time, cancel_reason)

    async def get_transaction_by_payment_id(self, payment_id):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow('SELECT * FROM transactions WHERE payment_id = $1 ORDER BY created_at DESC LIMIT 1', payment_id)

    async def get_transactions_by_time_range(self, from_time: int, to_time: int):
        async with self.pool.acquire() as conn:
            return await conn.fetch('''
                SELECT t.*, a.app_code FROM transactions t
                LEFT JOIN applications a ON t.application_id = a.id
                WHERE t.payment_provider = 'payme' AND t.create_time >= $1 AND t.create_time <= $2
                ORDER BY t.create_time ASC
            ''', from_time, to_time)

db = Database()
