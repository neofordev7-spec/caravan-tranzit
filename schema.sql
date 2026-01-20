-- =============================================
-- MYBOJXONA DATABASE SCHEMA
-- Customs Logistics Ecosystem
-- PostgreSQL 14+
-- =============================================

-- Drop existing tables (for fresh start)
DROP TABLE IF EXISTS referrals CASCADE;
DROP TABLE IF EXISTS transactions CASCADE;
DROP TABLE IF EXISTS applications CASCADE;
DROP TABLE IF EXISTS agents CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS customs_posts CASCADE;
DROP TABLE IF EXISTS saved_docs CASCADE;

-- =============================================
-- 1. CUSTOMS POSTS (Bojxona postlari)
-- =============================================
CREATE TABLE customs_posts (
    id SERIAL PRIMARY KEY,
    name JSONB NOT NULL,  -- Multi-language support: {"uz": "Yallama", "ru": "Яллама", "en": "Yallama"}
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for faster queries
CREATE INDEX idx_customs_posts_active ON customs_posts(is_active);

-- =============================================
-- 2. USERS (Foydalanuvchilar)
-- =============================================
CREATE TABLE users (
    telegram_id BIGINT PRIMARY KEY,
    full_name TEXT,
    phone_number TEXT,
    language TEXT DEFAULT 'uz',  -- uz, ru, en, zh, tr, ko, kz, kg, tj, uz_cyrl
    balance DECIMAL(10,2) DEFAULT 0.00,  -- Gamification coins
    referral_source BIGINT,  -- Who referred this user
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_users_referral ON users(referral_source);
CREATE INDEX idx_users_balance ON users(balance);

-- =============================================
-- 3. AGENTS (Deklarantlar/Agentlar)
-- =============================================
CREATE TABLE agents (
    id SERIAL PRIMARY KEY,
    full_name TEXT NOT NULL,
    telegram_id BIGINT UNIQUE,
    post_id INTEGER REFERENCES customs_posts(id) ON DELETE SET NULL,
    status TEXT DEFAULT 'offline',  -- 'online', 'offline'
    rating FLOAT DEFAULT 5.0,  -- 0.0 - 5.0
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_agents_post ON agents(post_id);
CREATE INDEX idx_agents_status ON agents(status);
CREATE INDEX idx_agents_rating ON agents(rating DESC);

-- =============================================
-- 4. APPLICATIONS (Arizalar)
-- =============================================
CREATE TABLE applications (
    id SERIAL PRIMARY KEY,
    app_code TEXT UNIQUE NOT NULL,
    user_id BIGINT REFERENCES users(telegram_id) ON DELETE CASCADE,
    agent_id INTEGER REFERENCES agents(id) ON DELETE SET NULL,
    post_id INTEGER REFERENCES customs_posts(id) ON DELETE SET NULL,
    vehicle_number TEXT,
    vehicle_type TEXT DEFAULT 'truck',  -- 'truck', 'car'
    status TEXT DEFAULT 'new',  -- 'new', 'priced', 'paid', 'completed', 'rejected', 'processing'
    price DECIMAL(10,2),
    admin_group_message_id BIGINT,
    files JSONB,  -- {"passport": "file_id", "tech_passport": "file_id", "invoice": "file_id"}
    metadata JSONB,  -- Additional data
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_applications_user ON applications(user_id);
CREATE INDEX idx_applications_agent ON applications(agent_id);
CREATE INDEX idx_applications_status ON applications(status);
CREATE INDEX idx_applications_code ON applications(app_code);
CREATE INDEX idx_applications_created ON applications(created_at DESC);

-- =============================================
-- 5. TRANSACTIONS (To'lovlar tarixi)
-- =============================================
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(telegram_id) ON DELETE CASCADE,
    application_id INTEGER REFERENCES applications(id) ON DELETE SET NULL,
    amount DECIMAL(10,2) NOT NULL,
    type TEXT NOT NULL,  -- 'card_payment', 'coins_payment', 'referral_bonus', 'service_purchase'
    status TEXT DEFAULT 'pending',  -- 'pending', 'completed', 'failed', 'cancelled'
    payment_provider TEXT,  -- 'click', 'payme', 'internal'
    payment_id TEXT,  -- External payment ID
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_transactions_user ON transactions(user_id);
CREATE INDEX idx_transactions_app ON transactions(application_id);
CREATE INDEX idx_transactions_status ON transactions(status);
CREATE INDEX idx_transactions_type ON transactions(type);

-- =============================================
-- 6. REFERRALS (Referral tizimi)
-- =============================================
CREATE TABLE referrals (
    id SERIAL PRIMARY KEY,
    referrer_id BIGINT REFERENCES users(telegram_id) ON DELETE CASCADE,
    referred_id BIGINT REFERENCES users(telegram_id) ON DELETE CASCADE UNIQUE,
    reward_given BOOLEAN DEFAULT FALSE,  -- 17,500 coins given when referred user makes first purchase
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_referrals_referrer ON referrals(referrer_id);
CREATE INDEX idx_referrals_referred ON referrals(referred_id);
CREATE INDEX idx_referrals_reward ON referrals(reward_given);

-- =============================================
-- 7. SAVED_DOCS (Auto-fill cache)
-- =============================================
CREATE TABLE saved_docs (
    user_id BIGINT,
    car_number TEXT,
    photos TEXT[],  -- Array of Telegram file IDs
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, car_number)
);

-- Index
CREATE INDEX idx_saved_docs_user ON saved_docs(user_id);

-- =============================================
-- SEED DATA: Customs Posts
-- =============================================
INSERT INTO customs_posts (name) VALUES
    ('{"uz": "Yallama", "ru": "Яллама", "en": "Yallama"}'),
    ('{"uz": "Olot", "ru": "Олот", "en": "Olot"}'),
    ('{"uz": "Doʻstlik (Andijon)", "ru": "Дустлик (Андижан)", "en": "Dustlik (Andijan)"}'),
    ('{"uz": "S. Najimov", "ru": "С. Наджимов", "en": "S. Najimov"}'),
    ('{"uz": "Dovut-ota", "ru": "Довут-ота", "en": "Dovut-ota"}'),
    ('{"uz": "Sirdaryo", "ru": "Сырдарья", "en": "Syrdarya"}'),
    ('{"uz": "Ayritom", "ru": "Айритом", "en": "Ayritom"}'),
    ('{"uz": "Jartepa", "ru": "Жартепа", "en": "Jartepa"}'),
    ('{"uz": "Oʻzbekiston", "ru": "Узбекистан", "en": "Uzbekistan"}'),
    ('{"uz": "Oybek", "ru": "Ойбек", "en": "Oybek"}');

-- =============================================
-- SEED DATA: Test Agents
-- =============================================
INSERT INTO agents (full_name, telegram_id, post_id, status, rating) VALUES
    ('Ali Valiyev', NULL, 1, 'online', 5.0),
    ('Sardor Karimov', NULL, 1, 'online', 4.8),
    ('Dilshod Toshev', NULL, 2, 'online', 4.9),
    ('Jahongir Rahimov', NULL, 3, 'offline', 4.7),
    ('Aziz Rahmatov', NULL, 4, 'online', 4.6),
    ('Bobur Alimov', NULL, 5, 'online', 4.9);

-- =============================================
-- USEFUL QUERIES (for reference)
-- =============================================

-- Get online agents for a specific post
-- SELECT * FROM agents WHERE post_id = 1 AND status = 'online' ORDER BY rating DESC;

-- Get user's balance and free services count
-- SELECT telegram_id, balance, FLOOR(balance / 35000) as free_services FROM users WHERE telegram_id = 123456789;

-- Get all applications for a user
-- SELECT * FROM applications WHERE user_id = 123456789 ORDER BY created_at DESC;

-- Get payment history for a user
-- SELECT * FROM transactions WHERE user_id = 123456789 ORDER BY created_at DESC;

-- Get referral statistics
-- SELECT referrer_id, COUNT(*) as referral_count, SUM(CASE WHEN reward_given THEN 1 ELSE 0 END) as completed_referrals
-- FROM referrals GROUP BY referrer_id;
