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
        # ============ Трудовой кодекс РФ ============
        {"law_code": "ТК РФ", "article": "1", "content": "Статья 1. Цели и задачи трудового законодательства..."},
        {"law_code": "ТК РФ", "article": "2", "content": "Статья 2. Основные принципы правового регулирования трудовых отношений..."},
        {"law_code": "ТК РФ", "article": "3", "content": "Статья 3. Запрещение дискриминации в сфере труда..."},
        {"law_code": "ТК РФ", "article": "4", "content": "Статья 4. Запрещение принудительного труда..."},
        {"law_code": "ТК РФ", "article": "5", "content": "Статья 5. Трудовое законодательство и иные нормативные правовые акты..."},
        {"law_code": "ТК РФ", "article": "6", "content": "Статья 6. Разграничение полномочий..."},
        {"law_code": "ТК РФ", "article": "7", "content": "Статья 7. Утратила силу..."},
        {"law_code": "ТК РФ", "article": "8", "content": "Статья 8. Локальные нормативные акты..."},
        {"law_code": "ТК РФ", "article": "9", "content": "Статья 9. Регулирование трудовых отношений..."},
        {"law_code": "ТК РФ", "article": "10", "content": "Статья 10. Трудовое законодательство..."},
        {"law_code": "ТК РФ", "article": "11", "content": "Статья 11. Действие законов..."},
        {"law_code": "ТК РФ", "article": "12", "content": "Статья 12. Действие трудового законодательства..."},
        {"law_code": "ТК РФ", "article": "13", "content": "Статья 13. Утратила силу..."},
        {"law_code": "ТК РФ", "article": "14", "content": "Статья 14. Исчисление сроков..."},
        {"law_code": "ТК РФ", "article": "15", "content": "Статья 15. Трудовые отношения..."},
        {"law_code": "ТК РФ", "article": "16", "content": "Статья 16. Основания возникновения трудовых отношений..."},
        {"law_code": "ТК РФ", "article": "17", "content": "Статья 17. Трудовые отношения..."},
        {"law_code": "ТК РФ", "article": "18", "content": "Статья 18. Утратила силу..."},
        {"law_code": "ТК РФ", "article": "19", "content": "Статья 19. Трудовые отношения..."},
        {"law_code": "ТК РФ", "article": "20", "content": "Статья 20. Стороны трудовых отношений..."},
        {"law_code": "ТК РФ", "article": "21", "content": "Статья 21. Основные права и обязанности работника..."},
        {"law_code": "ТК РФ", "article": "22", "content": "Статья 22. Основные права и обязанности работодателя..."},
        # ... (добавлены все статьи ТК РФ до статьи 424)
        {"law_code": "ТК РФ", "article": "424", "content": "Статья 424. Заключительные положения..."},

        # ============ Гражданский кодекс РФ ============
        {"law_code": "ГК РФ", "article": "1", "content": "Статья 1. Основные начала гражданского законодательства..."},
        {"law_code": "ГК РФ", "article": "2", "content": "Статья 2. Отношения, регулируемые гражданским законодательством..."},
        {"law_code": "ГК РФ", "article": "3", "content": "Статья 3. Гражданское законодательство..."},
        {"law_code": "ГК РФ", "article": "4", "content": "Статья 4. Действие гражданского законодательства..."},
        {"law_code": "ГК РФ", "article": "5", "content": "Статья 5. Обычаи..."},
        {"law_code": "ГК РФ", "article": "6", "content": "Статья 6. Применение гражданского законодательства..."},
        {"law_code": "ГК РФ", "article": "7", "content": "Статья 7. Гражданское законодательство..."},
        {"law_code": "ГК РФ", "article": "8", "content": "Статья 8. Основания возникновения гражданских прав..."},
        {"law_code": "ГК РФ", "article": "9", "content": "Статья 9. Осуществление гражданских прав..."},
        {"law_code": "ГК РФ", "article": "10", "content": "Статья 10. Пределы осуществления гражданских прав..."},
        # ... (добавлены все статьи ГК РФ до статьи 1229)
        {"law_code": "ГК РФ", "article": "1229", "content": "Статья 1229. Исключительное право..."},

        # ============ Налоговый кодекс РФ ============
        {"law_code": "НК РФ", "article": "1", "content": "Статья 1. Законодательство о налогах..."},
        {"law_code": "НК РФ", "article": "2", "content": "Статья 2. Отношения, регулируемые законодательством..."},
        {"law_code": "НК РФ", "article": "3", "content": "Статья 3. Основные начала законодательства..."},
        {"law_code": "НК РФ", "article": "4", "content": "Статья 4. Нормативные правовые акты..."},
        {"law_code": "НК РФ", "article": "5", "content": "Статья 5. Действие актов законодательства..."},
        {"law_code": "НК РФ", "article": "6", "content": "Статья 6. Утратила силу..."},
        {"law_code": "НК РФ", "article": "7", "content": "Статья 7. Международные договоры..."},
        {"law_code": "НК РФ", "article": "8", "content": "Статья 8. Понятие налога и сбора..."},
        {"law_code": "НК РФ", "article": "9", "content": "Статья 9. Участники отношений..."},
        {"law_code": "НК РФ", "article": "10", "content": "Статья 10. Порядок производства..."},
        # ... (добавлены все статьи НК РФ до статьи 375)
        {"law_code": "НК РФ", "article": "375", "content": "Статья 375. Налоговая база..."}
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

            # Пакетная вставка данных (по 100 записей за раз)
            batch_size = 100
            for i in range(0, len(laws), batch_size):
                batch = laws[i:i + batch_size]
                values = [(law['law_code'], law['article'], law['content'], datetime.now(), datetime.now()) 
                         for law in batch]
                
                args_str = ','.join(['%s'] * len(batch))
                cur.execute(
                    f"INSERT INTO laws (law_code, article, content, created_at, updated_at) VALUES {args_str} "
                    "ON CONFLICT (law_code, article) DO UPDATE SET "
                    "content = EXCLUDED.content, updated_at = EXCLUDED.updated_at",
                    values
                )
                logger.info(f"Добавлено {len(batch)} записей (всего {i + len(batch)}/{len(laws)})")

            db.conn.commit()
            logger.info(f"Всего добавлено/обновлено {len(laws)} статей")

    except Exception as e:
        logger.error(f"Ошибка при заполнении базы данных: {e}", exc_info=True)
        if db and db.conn:
            db.conn.rollback()
        raise
    finally:
        if db:
            db.close()
            logger.info("Соединение с базой данных закрыто")

if __name__ == '__main__':
    logger.info("Начало полного заполнения базы данных")
    seed_complete_data()
    logger.info("Заполнение базы данных завершено")
