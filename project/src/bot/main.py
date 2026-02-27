import asyncio

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.bot.routers import routers
from src.bot.config import config

dp = Dispatcher()

async def main():
    bot = Bot(config.token, default=DefaultBotProperties(ParseMode.HTML))

    dp.include_routers(*routers)
    dp.start_polling(bot)

asyncio.run(main())