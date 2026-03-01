import asyncio
import logging

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.bot.routers import routers
from src.bot.config import config
from src.bot.tools.api_client import api_client
from src.bot.middlewares import middlewares, exc_handlers
from src.bot.tools.bot_init import TGBot

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s | %(levelname)s | %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

async def on_startup():
    await api_client.start()

async def on_shutdown():
    await api_client.stop()

async def main():

    bot = Bot(config.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp = TGBot(middlewares, routers, exc_handlers, on_startup, on_shutdown).init()
    await dp.start_polling(bot)    

asyncio.run(main())