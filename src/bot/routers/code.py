from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from bot.tools.api_client import api_client
from bot.schemas import CodeResponse, UserResponse, APIError, APIOK
from bot.tools.keyboard import yes_or_no, get_approve_kb
from bot.config import config

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
            

@code.callback_query(F.data.startswith("delete:"))
async def delete_any(cb: CallbackQuery):
    parts = cb.data.split(":")
    delete_type = parts[1]

    if delete_type == "message":
        return await cb.message.delete()

    if delete_type == "token":
        await api_client.post(APIOK, user_id=cb.from_user.id, path="auth/deleteSession", session_user_id=cb.from_user.id)
    elif delete_type == "session":
        user_id = parts[2]
        await api_client.post(APIOK, user_id=cb.from_user.id, path="auth/deleteSession", session_user_id=user_id)

    await cb.message.delete()