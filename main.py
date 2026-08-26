"""
Standart va Metrologiya Telegram Botining asosiy ishga tushirish fayli (Entrypoint).
"""

import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import BotCommand, BotCommandScopeDefault

from bot.config import config
from bot.database import init_db
from bot.handlers import all_routers

# Logging sozlash
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


async def set_bot_commands(bot: Bot):
    """Bot menyusidagi asosiy buyruqlarni o'rnatish."""
    commands = [
        BotCommand(command="start", description="🚀 Botni ishga tushirish / Запуск"),
        BotCommand(command="lang", description="🌐 Tilni o'zgartirish / Сменить язык"),
        BotCommand(command="cart", description="🛒 Savatcha / Корзина"),
        BotCommand(command="ai", description="🤖 AI Metrolog Maslahatchi / AI Консультант"),
        BotCommand(command="search", description="🔍 Mahsulot qidirish / Поиск"),
        BotCommand(command="catalog", description="📦 Mahsulotlar katalogi / Каталог"),
        BotCommand(command="help", description="ℹ️ Qo'llanma / Помощь"),
        BotCommand(command="admin", description="⚙️ Admin paneli / Админ панель")
    ]
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())


async def main():
    """Botni ishga tushiruvchi asosiy asinxron funksiya."""
    logger.info("Bot ishga tushmoqda...")

    # Token tekshiruvi
    if not config.token or config.token == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
        logger.error(
            "\n"
            "===============================================================\n"
            "XATOLIK: BOT_TOKEN o'rnatilmagan!\n"
            "Iltimos, .env faylini oching va Telegram @BotFather dan olgan\n"
            "tokeningizni 'BOT_TOKEN=...' qatoriga kiriting.\n"
            "===============================================================\n"
        )
        return

    # Ma'lumotlar bazasini initsializatsiya qilish
    logger.info("Ma'lumotlar bazasi tayyorlanmoqda...")
    await init_db()
    logger.info("Ma'lumotlar bazasi muvaffaqiyatli ishga tushirildi.")

    # Bot va Dispatcher obyektlarini yaratish
    bot = Bot(
        token=config.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # Barcha routerlarni ulash
    for router in all_routers:
        dp.include_router(router)

    # Buyruqlar menyusini o'rnatish
    try:
        await set_bot_commands(bot)
    except Exception as e:
        logger.warning(f"Bot buyruqlarini o'rnatishda ogohlantirish: {e}")

    # Polling boshlash
    logger.info("Bot muvaffaqiyatli ishga tushdi va xabarlarni qabul qilmoqda!")
    try:
        # Eski o'qilmagan xabarlarni chetlab o'tish (drop pending updates)
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        logger.info("Bot to'xtatildi.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot to'xtatildi.")
