from aiogram.fsm.state import State, StatesGroup

class ReportState(StatesGroup):
    money = State()
    itph = State()
    sos = State()
    guest_experience = State()
    comment = State()
    checks = State()
    photos = State()