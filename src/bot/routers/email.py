import logging
import os
from uuid import uuid4

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from bot.states import SendEmail
from bot.tools.emojis import Emojis
from bot.tools.tools import send_files_to_email
from bot.tools.api_client import api_client
from bot.schemas import UserResponse
from bot.tools.keyboard import cancel_keyboard, get_start_keyboard

email_router = Router()
logger = logging.getLogger(__name__)


@email_router.message(F.text == "📩 На почту")
async def start_send_media(m: Message, state: FSMContext):
    await state.set_state(SendEmail.files)
    await state.update_data(filenames=[])
    
    user = await api_client.get(UserResponse, user_id=m.from_user.id)
    await state.update_data(manager=user.data)
    logger.info(
        "email sending started | manager=%s user_id=%s",
        user.data.short_name,
        m.from_user.id
    )
    await m.answer(
        f"{Emojis.to_mail} Понял! Отправь мне все нужные файлы, после чего нажми кнопку готово.",
        reply_markup=cancel_keyboard(send_email_kb=True),
    )


@email_router.message(StateFilter(SendEmail.files), F.photo | F.video | F.document)
async def input_any_media(m: Message, state: FSMContext):
    filename = uuid4()

    file, name = (
        (m.photo[-1], f"src/downloads/{filename}.png") if m.photo else
        (m.video, f"src/downloads/{filename}.mp4") if m.video else
        (m.document, f"src/downloads/{m.document.file_name}")
    )

    logger.debug(
        "email attachment received | user_id=%s filename=%s",
        m.from_user.id,
        name,
    )

    await m.bot.download(file, name)

    filenames = (await state.get_data())['filenames']
    filenames.append(name)

    await state.update_data(filenames=filenames)
    logger.debug(
        "email attachment saved | user_id=%s filename=%s files=%s",
        m.from_user.id,
        name,
        len(filenames),
    )


@email_router.message(StateFilter(SendEmail.files), F.text == "✉️ Готово")
async def stop_input_media(m: Message, state: FSMContext):
    state_data = await state.get_data()
    await state.clear()

    message = await m.answer("🚀 Начинаю отправку...")
    await send_files_to_email(filenames=state_data['filenames'], manager_name=state_data['manager'])
    logger.debug(
        "email sending finished | manager=%s user_id=%s files=%s",
        state_data["manager"].short_name,
        m.from_user.id,
        len(state_data["filenames"]),
    )
    await m.bot.delete_message(m.chat.id, message_id=message.message_id)
    await m.answer(f"{Emojis.success} Готово! Файлы уже на почте", reply_markup=get_start_keyboard(state_data['manager'].role))
    
    for filename in state_data['filenames']:
        if os.path.isfile(filename):
            os.remove(filename)

@email_router.message(StateFilter(SendEmail.files), F.text == "Отменить.")
async def stop_input_proccess(m: Message, state: FSMContext):
    state_data = await state.get_data()

    if state_data['filenames']:
        for filename in state_data['filenames']:
            os.remove(filename)
    
    await m.answer(f"{Emojis.sad} Понял, прекращаю процесс.", reply_markup=get_start_keyboard(state_data['manager'].role))
    await state.clear()
