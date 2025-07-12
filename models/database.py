import psycopg2
from psycopg2 import sql, extras
from psycopg2.errors import DuplicateTable, UndefinedTable
from config import Config
import logging
from typing import List, Tuple, Optional

# Настройка логгирования
logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        """Инициализация подключения к базе данных и создание таблиц"""
        self.conn = None
        try:
            self.conn = psycopg2.connect(
                host=Config.DB_HOST,
                port=Config.DB_PORT,
                dbname=Config.DB_NAME,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                connect_timeout=5
            )
            self.create_tables()
            logger.info("Database connection established and tables verified")
        except psycopg2.OperationalError as e:
            logger.error(f"Failed to connect to database: {e}")
            raise

    def __enter__(self):
        """Поддержка контекстного менеджера"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Гарантированное закрытие соединения"""
        self.close()

    def close(self):
        """Закрытие соединения с базой данных"""
        if self.conn and not self.conn.closed:
            self.conn.close()
            logger.info("Database connection closed")

    def create_tables(self):
        """Создание таблиц и индексов"""
        with self.conn.cursor() as cur:
            try:
                # Таблица законов
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS laws (
                        id SERIAL PRIMARY KEY,
                        law_code VARCHAR(50) NOT NULL,
                        article VARCHAR(20) NOT NULL,
                        content TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT NOW(),
                        updated_at TIMESTAMP DEFAULT NOW(),
                        CONSTRAINT unique_law_article UNIQUE (law_code, article)
                    );
                """)

                # Таблица запросов пользователей
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS user_queries (
                        id SERIAL PRIMARY KEY,
                        user_hash VARCHAR(64) NOT NULL,
                        query TEXT NOT NULL,
                        response TEXT,
                        response_time_ms INTEGER,
                        created_at TIMESTAMP DEFAULT NOW()
                    );
                """)

                # Индексы
                cur.execute("""
                    CREATE INDEX IF NOT EXISTS laws_content_idx ON laws 
                    USING gin(to_tsvector('russian', content));
                """)
                
                # Индекс для быстрого поиска по коду закона и статье
                cur.execute("""
                    CREATE INDEX IF NOT EXISTS laws_code_article_idx ON laws (law_code, article);
                """)

                self.conn.commit()
                logger.info("Tables and indexes created/verified")
            except (DuplicateTable, UndefinedTable) as e:
                self.conn.rollback()
                logger.warning(f"Table creation warning: {e}")
            except Exception as e:
                self.conn.rollback()
                logger.error(f"Error creating tables: {e}")
                raise

    def search_laws(self, keywords: List[str], limit: int = 3) -> List[Tuple]:
        """Поиск законов по ключевым словам"""
        try:
            with self.conn.cursor(cursor_factory=extras.DictCursor) as cur:
                query = sql.SQL("""
                    SELECT law_code, article, content,
                           ts_rank(to_tsvector('russian', content), 
                           plainto_tsquery('russian', %s)) as rank
                    FROM laws 
                    WHERE to_tsvector('russian', content) @@ plainto_tsquery('russian', %s)
                    ORDER BY rank DESC
                    LIMIT %s;
                """)
                keywords_str = ' '.join(keywords)
                cur.execute(query, (keywords_str, keywords_str, limit))
                return cur.fetchall()
        except Exception as e:
            logger.error(f"Search error: {e}")
            return []

    def log_query(self, user_id: str, query_text: str, found: bool, 
                 response_time_ms: Optional[int] = None) -> None:
        """Логирование пользовательского запроса"""
        import hashlib

        try:
            user_hash = hashlib.sha256(f"{user_id}{Config.SALT}".encode()).hexdigest()
            response_status = "found" if found else "not_found"

            with self.conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO user_queries (user_hash, query, response, response_time_ms) 
                    VALUES (%s, %s, %s, %s);
                """, (user_hash, query_text, response_status, response_time_ms))
                self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to log query: {e}")
            self.conn.rollback()

    def add_law(self, law_code: str, article: str, content: str) -> bool:
        """Добавление новой статьи закона"""
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO laws (law_code, article, content)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (law_code, article) 
                    DO UPDATE SET 
                        content = EXCLUDED.content,
                        updated_at = NOW()
                    RETURNING id;
                """, (law_code, article, content))
                self.conn.commit()
                return bool(cur.fetchone())
        except Exception as e:
            logger.error(f"Failed to add law: {e}")
            self.conn.rollback()
            return False

    def get_law(self, law_code: str, article: str) -> Optional[dict]:
        """Получение конкретной статьи закона"""
        try:
            with self.conn.cursor(cursor_factory=extras.DictCursor) as cur:
                cur.execute("""
                    SELECT law_code, article, content
                    FROM laws
                    WHERE law_code = %s AND article = %s;
                """, (law_code, article))
                result = cur.fetchone()
                return dict(result) if result else None
        except Exception as e:
            logger.error(f"Failed to get law: {e}")
            return None
