from datetime import timedelta, datetime

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from src.bot.states import ReportState
from src.bot.filters import IsAdmin, SosTimeFilter
from src.bot.tools.api_client import api_client
from src.bot.tools.keyboard import cancel_keyboard, get_start_keyboard
from src.bot.schemas import ReportResponse, APIOK

from src.bot.tools.emojis import Emojis

report_router = Router()


@report_router.message(F.text == "Отменить.")
async def cancel_state(m: Message, state: FSMContext, role: str):
    await state.clear()
    await m.answer(f'{Emojis.sad} Понял, отменяю процесс.', reply_markup=get_start_keyboard(role))


@report_router.message(IsAdmin(), F.text == "🌙 Ночной отчет")
@report_router.message(IsAdmin(), F.text == "☀️ Дневной отчет")
async def start_create_report(m: Message, state: FSMContext):
    report_type = "night" if m.text == "🌙 Ночной отчет" else "day"

    current_date = datetime.now().date()
    
    if report_type == "night":
        current_date = current_date - timedelta(days=1)

    reports = await api_client.get(ReportResponse, m.from_user.id, date=current_date.strftime("%Y-%m-%d"), report_type=report_type)
    if reports.data.items:
        return await m.answer(f'{Emojis.sassy} Отчёт такого типа за сегодня уже был создан менеджером {reports.data.items[0].short_name}')
    
    await state.set_state(ReportState.money)
    await state.update_data(report_type=report_type)

    await m.answer(text="Отлично, начнём! Отправь мне товарооборот за смену.", reply_markup=cancel_keyboard())


@report_router.message(StateFilter(ReportState.money), F.text.isdigit())
async def set_state_money(m: Message, state: FSMContext):
    await state.update_data(money=int(m.text))
    await state.set_state(ReportState.itph)
    
    await m.answer("Сохранил! Теперь отправь мне ITPH.")


@report_router.message(StateFilter(ReportState.itph))
async def set_state_itph(m: Message, state: FSMContext):
    itph = float(m.text.replace(",", "."))
    
    await state.update_data(itph=itph)
    await state.set_state(ReportState.guest_experience)

    await m.answer("Сохранил! Далее отправь ГО.")


@report_router.message(StateFilter(ReportState.guest_experience), F.text.isdigit())
async def set_state_ge(m: Message, state: FSMContext):
    await state.update_data(guest_experience=int(m.text))
    await state.set_state(ReportState.checks)

    await m.answer("Сохранил! Далее отправь мне количество чеков за смену.")


@report_router.message(StateFilter(ReportState.checks), F.text.isdigit())
async def set_state_checks(m: Message, state: FSMContext):
    await state.update_data(checks=int(m.text))
    await state.set_state(ReportState.sos)

    await m.answer("Сохранил! Далее отправь SOS и SOS доставки через запятую.\n"
                   "<blockquote><b>Важно! Отправляй показатели именно в этом порядке.</b></blockquote>")


@report_router.message(StateFilter(ReportState.sos), SosTimeFilter())
async def set_state_sos(m: Message, state: FSMContext):
    sos, sos_delivery = (
        sum(int(x) * 60 ** (1 - i) for i, x in enumerate(t.split(':')))
        for t in m.text.replace(" ", "").split(",")
    )
    
    await state.update_data(sos=sos, sos_delivery=sos_delivery, photos=[])
    await state.set_state(ReportState.photos)
    await m.answer("Сохранил! Теперь отправь фотографии.\n"
                   "<blockquote><b>Важно, после отправки фотографий отправь мне слово 'готово'</b></blockquote>")


@report_router.message(StateFilter(ReportState.photos), F.photo)
async def set_state_photos(m: Message, state: FSMContext):
    file_id = m.photo[-1].file_id  
    photos = (await state.get_data())["photos"]
    photos.append(file_id)
    await state.update_data(photos=photos)


@report_router.message(StateFilter(ReportState.photos, F.text.lower() == "готово"))
async def done_photos(m: Message, state: FSMContext):
    await m.answer('Сохранил! Отправь комментарии к смене.')
    await state.set_state(ReportState.comment)


@report_router.message(StateFilter(ReportState.comment))
async def final_create_report(m: Message, state: FSMContext, role: str):
    data = await state.get_data()

    await api_client.post(APIOK, user_id=m.from_user.id, path="report/create", bot=m.bot, comments=m.text, **data)
    await m.answer(f'{Emojis.success} Успешно!', reply_markup=get_start_keyboard(role))
    await state.clear()
    