import aiohttp
import logging
from config import Config
from typing import Optional


class GigaChatService:
    def __init__(self):
        self.auth_url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        self.api_url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
        self.access_token: Optional[str] = None
        self.session: Optional[aiohttp.ClientSession] = None
        self.logger = logging.getLogger(__name__)

    async def initialize(self):
        """Инициализация асинхронной сессии"""
        self.session = aiohttp.ClientSession()

    async def close(self):
        """Корректное закрытие сессии"""
        if self.session and not self.session.closed:
            await self.session.close()

    async def _get_access_token(self) -> None:
        """Получение токена доступа"""
        try:
            self.logger.info("⌛ Получаем токен GigaChat...")
            
            if not self.session:
                await self.initialize()

            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json',
                'RqUID': Config.GIGACHAT_RqUID,
                'Authorization': f'Basic {Config.GIGACHAT_AUTH_KEY}'
            }

            async with self.session.post(
                self.auth_url,
                headers=headers,
                data={'scope': Config.GIGACHAT_SCOPE},
                ssl=False
            ) as response:
                response.raise_for_status()
                self.access_token = (await response.json())['access_token']
                self.logger.info("✅ Токен успешно получен")

        except Exception as e:
            self.logger.error(f"❌ Ошибка получения токена: {e}")
            raise

    async def ask(self, question: str) -> str:
        """Запрос к GigaChat API"""
        try:
            if not self.session:
                await self.initialize()

            if not self.access_token:
                await self._get_access_token()

            headers = {
                'Accept': 'application/json',
                'Authorization': f'Bearer {self.access_token}'
            }

            payload = {
                "model": "GigaChat",
                "messages": [
                    {
                        "role": "system",
                        "content": "Ты юридический ассистент. Давай точные ответы со ссылками на законы РФ."
                    },
                    {
                        "role": "user",
                        "content": question
                    }
                ],
                "temperature": 0.7  # Добавляем параметр для более детерминированных ответов
            }

            async with self.session.post(
                self.api_url,
                headers=headers,
                json=payload,
                ssl=False
            ) as response:
                response.raise_for_status()
                data = await response.json()
                return data['choices'][0]['message']['content']

        except aiohttp.ClientError as e:
            self.logger.error(f"Ошибка соединения с GigaChat: {e}")
            return "Ошибка соединения с нейросетью. Попробуйте позже."
        except Exception as e:
            self.logger.error(f"Ошибка GigaChat API: {e}", exc_info=True)
            return "Не удалось обработать ваш запрос. Пожалуйста, уточните вопрос."

    async def __aenter__(self):
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
