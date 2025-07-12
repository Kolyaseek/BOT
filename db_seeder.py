import sys
import os
import logging
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent))
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from models.database import Database

def get_complete_laws_data():
    """Возвращает полный набор статей из ТК, ГК и НК РФ"""
    return [
        # Ваши данные...
    ]

def seed_complete_data():
    """Заполнение базы данных полным набором статей"""
    db = None
    try:
        db = Database()
        logger.info("Подключение к базе данных установлено")
        
        laws = get_complete_laws_data()

        with db.conn.cursor() as cur:
            # Проверка существования таблицы
            cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'laws');")
            if not cur.fetchone()[0]:
                logger.error("Таблица 'laws' не существует!")
                raise Exception("Таблица законов не найдена")

            # Пакетная вставка данных
            batch_size = 100
            for i in range(0, len(laws), batch_size):
                batch = laws[i:i + batch_size]
                args = [(law['law_code'], law['article'], law['content'], datetime.now(), datetime.now()) 
                       for law in batch]
                
                args_str = ','.join(['%s'] * len(batch))
                cur.execute(
                    f"INSERT INTO laws (law_code, article, content, created_at, updated_at) VALUES {args_str} "
                    "ON CONFLICT (law_code, article) DO UPDATE SET "
                    "content = EXCLUDED.content, updated_at = EXCLUDED.updated_at",
                    args
                )
                logger.info(f"Обработано {len(batch)} записей (всего {i + len(batch)}/{len(laws)})")

            db.conn.commit()
            logger.info(f"Всего добавлено/обновлено {len(laws)} статей")

    except Exception as e:
        logger.error(f"Ошибка при заполнении базы данных: {e}", exc_info=True)
        if db and hasattr(db, 'conn') and db.conn:
            db.conn.rollback()
        raise
    finally:
        if db:
            if hasattr(db, 'close'):
                db.close()
                logger.info("Соединение с базой данных закрыто")
            elif hasattr(db, 'conn') and db.conn:
                db.conn.close()
                logger.info("Соединение закрыто через conn.close()")

if __name__ == '__main__':
    logger.info("Начало полного заполнения базы данных")
    seed_complete_data()
    logger.info("Заполнение базы данных завершено")
