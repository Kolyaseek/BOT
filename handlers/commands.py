from aiogram import Router, types, F
from aiogram.filters import Command
from models.database import Database
from services.gigachat import GigaChatService
from utils.formatters import format_laws
from utils.nlp_utils import extract_keywords  # Функция для извлечения ключевых слов
import logging

router = Router()
giga = GigaChatService()

@router.message(Command("start", "help"))
async def cmd_start(message: types.Message):
    welcome_text = (
        "👨⚖️ Добро пожаловать в юридический помощник!\n\n"
        "Я могу помочь вам найти информацию по:\n"
        "- Трудовому кодексу\n"
        "- Гражданскому кодексу\n"
        "- Налоговому кодексу\n\n"
        "Просто напишите ваш вопрос, например:\n"
        "'Какие права у работника при увольнении?'"
    )
    await message.answer(welcome_text)

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = (
        "📚 Помощь по использованию бота:\n\n"
        "1. Задайте вопрос простыми словами\n"
        "2. Укажите, если возможно, номер статьи или кодекса\n"
        "3. Бот найдет соответствующую информацию\n\n"
        "Примеры запросов:\n"
        "- 'Статья 81 ТК РФ'\n"
        "- 'Права потребителя при возврате товара'\n"
        "- 'Сроки уплаты НДФЛ'"
    )
    await message.answer(help_text)

@router.message()
async def handle_all_messages(message: types.Message):
    try:
        # Сначала ищем в базе данных
        db = Database()
        keywords = extract_keywords(message.text)
        laws = db.search_laws(keywords)
        
        if laws:
            await message.answer(format_laws(laws))
        else:
            # Если в БД нет ответа - используем GigaChat
            try:
                ai_response = await giga.ask(message.text)
                await message.answer(ai_response)
            except Exception as ai_error:
                logging.error(f"GigaChat error: {ai_error}")
                await message.answer("⚠️ Не удалось найти  ответ. Попробуйте позже.")
                
    except Exception as e:
        logging.error(f"Error processing message: {e}")
        await message.answer("⚠️ Произошла ошибка при обработке запроса")
