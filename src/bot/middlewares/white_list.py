from cachetools import TTLCache

from aiogram import BaseMiddleware

from src.bot.schemas import UserResponse, APIError
from src.bot.tools.api_client import api_client
from src.bot.config import config

class WhiteList(BaseMiddleware):

    def __init__(self):
        self.cache = TTLCache(50, 300)

    async def __call__(self, handler, event, data):
        user = data.get("event_from_user")
        
        if user:
            if user.id in self.cache:
                data["role"] = self.cache[user.id]
                return await handler(event, data)
            try:
                user_response = await api_client.get(UserResponse, user.id)
                self.cache[user.id] = user_response.data.role
                data["role"] = user_response.data.role
                return await handler(event, data)
            except APIError:
                return

        
