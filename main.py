import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import Config
from handlers import commands
import time

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    try:
        # Инициализация бота
        bot = Bot(token=Config.TELEGRAM_TOKEN)
        dp = Dispatcher(storage=MemoryStorage())
        
        # Подключение роутеров
        dp.include_router(commands.router)
        
        # Удаляем вебхук (важно для PythonAnywhere)
        await bot.delete_webhook(drop_pending_updates=True)
        
        logger.info("Бот запущен в режиме polling")
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        raise

if __name__ == '__main__':
    # Бесконечный цикл с перезапуском при ошибках
    while True:
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            logger.info("Бот остановлен вручную")
            break
        except Exception as e:
            logger.error(f"Критическая ошибка: {e}")
            logger.info("Перезапуск через 60 секунд...")
            time.sleep(60)
