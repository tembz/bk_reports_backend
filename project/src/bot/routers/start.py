from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from src.bot.tools.keyboard import get_start_keyboard

start_router = Router()

@start_router.message(CommandStart())
async def command_start(m: Message, role: str):
    
    kb = get_start_keyboard(role)
    await m.answer('<tg-emoji emoji-id="5470092785094765546">☺️</tg-emoji>Привет! Жду твои отчёты.', reply_markup=kb)