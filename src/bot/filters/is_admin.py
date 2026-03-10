from aiogram.filters import BaseFilter

from bot.config import config

class IsAdmin(BaseFilter):

    async def __call__(self, event, role: str = None):
        return role in config.admin_roles