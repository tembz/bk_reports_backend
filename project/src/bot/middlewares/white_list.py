from cachetools import TTLCache

from aiogram import BaseMiddleware

from src.bot.schemas import UserResponse, APIError
from src.bot.tools.api_client import api_client

class WhiteList(BaseMiddleware):

    def __init__(self):
        self.cache = TTLCache(50, 300)

    async def __call__(self, handler, event, data):
        user = data.get("event_from_user")
        
        if user:
            if user.id in self.cache:
                return await handler(event, data)
            try:
                user_reponse = await api_client.get(UserResponse, user.id, "/get")
                self.cache[user.id] = user_reponse.data.role
                data["role"] = user_reponse.data.role
                return await handler(event, data)
            except APIError:
                return await event.bot.send_message(chat_id=user.id, text="❌ Вам недоступен функционал")

        
