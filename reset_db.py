import asyncio
from database import db

async def reset():
    print("⏳ Bazaga ulanmoqda...")
    await db.connect()
    print("🗑 Tozalanmoqda...")
    await db.pool.execute("DROP TABLE IF EXISTS applications CASCADE;")
    await db.pool.execute("DROP TABLE IF EXISTS users CASCADE;")
    print("✅ Baza tozalandi. Restart bering.")

if __name__ == "__main__":
    asyncio.run(reset())
