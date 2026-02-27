import asyncio

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.bot.routers import routers
from src.bot.config import config
from src.bot.tools.api_client import api_client
from src.bot.middlewares.white_list import WhiteList

dp = Dispatcher()

async def main():
    bot = Bot(config.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp.include_routers(*routers)
    dp.message.middleware(WhiteList())
    
    await api_client.start()
    await dp.start_polling(bot)

asyncio.run(main())