import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
import os

from config import Config
from handlers import commands
from models.database import Database

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def on_startup(bot: Bot):
    """Действия при запуске"""
    webhook_url = f"https://{os.getenv('RAILWAY_STATIC_URL')}/webhook"
    await bot.set_webhook(webhook_url)
    logger.info(f"Webhook установлен: {webhook_url}")

    # Инициализация БД
    try:
        db = Database()
        logger.info("✅ База данных подключена")
    except Exception as e:
        logger.error(f"❌ Ошибка БД: {e}")

async def main():
    bot = Bot(token=Config.TELEGRAM_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    
    # Регистрация обработчиков
    dp.include_router(commands.router)
    dp.startup.register(on_startup)

    # Настройка веб-сервера
    app = web.Application()
    webhook_handler = SimpleRequestHandler(dp, bot)
    webhook_handler.register(app, path="/webhook")
    setup_application(app, dp, bot=bot)

    # Запуск
    port = int(os.getenv("PORT", 8000))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host="0.0.0.0", port=port)
    
    logger.info(f"🚀 Бот запущен на порту {port}")
    await site.start()
    
    # Бесконечный цикл
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Бот остановлен")
    except Exception as e:
        logger.error(f"🔥 Критическая ошибка: {e}")
