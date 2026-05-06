from aiogram.fsm.state import State, StatesGroup

class SendEmail(StatesGroup):
    files = State()