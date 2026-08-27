"""
SQLite ma'lumotlar bazasi bilan asinxron ulanish va sozlash moduli.
"""

import aiosqlite
import logging
from bot.config import config
from bot.database.seed_data import SEED_CATEGORIES, SEED_PRODUCTS

logger = logging.getLogger(__name__)


async def get_db() -> aiosqlite.Connection:
    """Ma'lumotlar bazasiga ulanish ob'ektini qaytaradi."""
    db = await aiosqlite.connect(config.database_path)
    db.row_factory = aiosqlite.Row
    return db


async def init_db():
    """Jadvallarni yaratish va dastlabki ma'lumotlarni yuklash."""
    async with aiosqlite.connect(config.database_path) as db:
        # Kategoriyalar jadvali
        await db.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                icon TEXT,
                description TEXT
            );
        """)

        # Mahsulotlar va xizmatlar jadvali
        await db.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                code TEXT,
                standard TEXT,
                accuracy_class TEXT,
                measurement_range TEXT,
                price TEXT,
                description TEXT,
                is_service INTEGER DEFAULT 0,
                FOREIGN KEY (category_id) REFERENCES categories (id)
            );
        """)

        # Foydalanuvchilar jadvali
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                full_name TEXT,
                language TEXT DEFAULT 'uz',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Mavjud users jadvalida language ustuni bo'lmasa qo'shish
        cursor = await db.execute("PRAGMA table_info(users)")
        cols = [row[1] for row in await cursor.fetchall()]
        if "language" not in cols:
            await db.execute("ALTER TABLE users ADD COLUMN language TEXT DEFAULT 'uz'")

        # Foydalanuvchi Savatchasi (Cart) jadvali
        await db.execute("""
            CREATE TABLE IF NOT EXISTS cart (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, product_id),
                FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE
            );
        """)

        # Arizalar / Buyurtmalar jadvali
        await db.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                full_name TEXT NOT NULL,
                phone_number TEXT NOT NULL,
                item_name TEXT,
                item_type TEXT,
                notes TEXT,
                status TEXT DEFAULT 'yangi',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Qidiruvlar tarixi jadvali
        await db.execute("""
            CREATE TABLE IF NOT EXISTS search_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                query TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        await db.commit()

        # Upsert seed data (categories and products)
        # Insert categories if they do not exist
        for cat in SEED_CATEGORIES:
            await db.execute(
                "INSERT OR IGNORE INTO categories (id, name, icon, description) VALUES (?, ?, ?, ?)",
                (cat["id"], cat["name"], cat["icon"], cat["description"]))

        # Insert products if they do not exist
        for prod in SEED_PRODUCTS:
            # Check existence by category_id and name
            cursor = await db.execute(
                "SELECT id FROM products WHERE category_id = ? AND name = ?",
                (prod["category_id"], prod["name"]))
            exists = await cursor.fetchone()
            if not exists:
                await db.execute(
                    """INSERT INTO products (
                        category_id, name, code, standard, accuracy_class,
                        measurement_range, price, description, is_service
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        prod["category_id"],
                        prod["name"],
                        prod["code"],
                        prod["standard"],
                        prod["accuracy_class"],
                        prod["measurement_range"],
                        prod["price"],
                        prod["description"],
                        prod["is_service"]
                    ))
        await db.commit()
        logger.info("Seed data upsert completed.")
