import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Настройки Telegram бота
    TELEGRAM_TOKEN = "8175032447:AAEj_Mzr8ZFiO3N6v0gD68zRPGYbLHd1opc"  # Можно вынести в .env
    
    # Настройки базы данных
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'legal_bot')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD')  # Обязательно в .env
    SALT = os.getenv('SALT', 'default_salt_for_hashing')
    
    # Настройки GigaChat API
    GIGACHAT_AUTH_KEY = "ZTlhZDI2ZmItYjQwZS00NzBhLTk0OTAtOTM5ODdhMWRhN2M3OjBjYTVkZmY2LTM2YzYtNDg0OS1iYzI3LWQ3YWU0MGFiMjgxYg=="  # Полный ключ
    GIGACHAT_SCOPE = os.getenv("GIGACHAT_SCOPE", "GIGACHAT_API_PERS")
    GIGACHAT_RqUID = os.getenv("GIGACHAT_RqUID", "252bff8a-bd1f-4ed3-bf59-bc3f5f19ef15")
