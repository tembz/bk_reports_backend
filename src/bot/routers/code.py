from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from src.bot.tools.api_client import api_client
from src.bot.schemas import CodeResponse, UserResponse, APIError
from src.bot.tools.keyboard import yes_or_no, get_approve_kb
from src.bot.config import config

code = Router()


@code.message(Command("code"))
async def get_code(m: Message):
    try:
        code = await api_client.post(CodeResponse, m.from_user.id)
        user = await api_client.get(UserResponse, m.from_user.id)
        await m.answer(f"Код для доступа к приложению - <code>{code.data.code}</code> (действует 5 минут).")
        await m.bot.send_message(config.owner_tg_id, f"Менеджер {user.data.short_name} запросил код для доступа к приложению.", reply_markup=get_approve_kb(m.from_user.id))
    except APIError as e:
        match e.response.error:
            case "session already exists":
                return await m.answer("Вы уже авторизованы в приложении. Удалить сессию?", reply_markup=yes_or_no())
            case "active code already exists":
                return await m.answer("У вас уже есть активный код, воспользуйся им, пока не поздно!")