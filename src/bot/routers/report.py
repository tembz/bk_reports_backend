from datetime import timedelta, datetime

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from src.bot.states import ReportState
from src.bot.tools.api_client import api_client
from src.bot.tools.keyboard import cancel_keyboard
from src.bot.schemas import ReportResponse

report_router = Router()


@report_router.message(F.text == "🌙 Ночной отчет")
@report_router.message(F.text == "☀️ Дневной отчет")
async def start_create_report(m: Message, state: FSMContext):
    report_type = "night" if m.text == "🌙 Ночной отчет" else "day"

    current_date = datetime.now().date()
    
    if report_type == "night":
        current_date = current_date - timedelta(days=1)

    reports = await api_client.get(ReportResponse, m.from_user.id, date=current_date.strftime("%Y-%m-%d"), report_type=report_type)
    if reports.data.items:
        return await m.answer(f'<tg-emoji emoji-id="5471975131821648150">🙂‍↔️</tg-emoji> Отчёт такого типа за сегодня уже был создан менеджером {reports.data.items[0].short_name}')
    
    await state.set_state(ReportState.money)
    await state.update_data(report_type=report_type)

    await m.answer(text="Отлично, начнём! Отправь мне товарооборот за смену.", reply_markup=cancel_keyboard())
