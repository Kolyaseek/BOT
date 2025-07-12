import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import Config
from handlers import commands

# Настройка логирования
logging.basicConfig(level=logging.INFO)

async def main():
    # Инициализация бота
    bot = Bot(token=Config.TELEGRAM_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    
    # Включаем роутеры из handlers
    dp.include_router(commands.router)
    
    # Проверка подключения к БД
    from models.database import Database
    db = Database()
    logging.info("Database connection established")
    
    # Запуск бота
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
