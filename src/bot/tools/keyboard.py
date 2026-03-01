from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_start_keyboard(user_type: str):
    kb_buttons = [[KeyboardButton(text="☀️ Дневной отчет")], [KeyboardButton(text="🌙 Ночной отчет")]]
    if user_type in ("director", "owner"):
        kb_buttons.append([KeyboardButton(text="📑 Сводная")])
    return ReplyKeyboardBuilder(kb_buttons).as_markup(resize_keyboard=True, one_time=True)

def cancel_keyboard():
    return ReplyKeyboardBuilder([[KeyboardButton(text="Отменить.")]]).as_markup(resize_keyboard=True, one_time=True)