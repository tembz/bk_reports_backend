from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from bot.filters import IsAdmin
from bot.tools.keyboard import get_start_keyboard

from bot.tools.emojis import Emojis

start_router = Router()

@start_router.message(CommandStart(), IsAdmin())
async def command_start(m: Message, role: str):

    kb = get_start_keyboard(role)
    await m.answer(f'{Emojis.love} Привет! Жду твои отчёты.', reply_markup=kb)