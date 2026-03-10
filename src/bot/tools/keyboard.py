from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from bot.tools.emojis import Emojis

def get_start_keyboard(user_type: str):
    kb_buttons = [[KeyboardButton(text="☀️ Дневной отчет")], [KeyboardButton(text="🌙 Ночной отчет")]]
    if user_type in ("director", "owner"):
        kb_buttons.append([KeyboardButton(text="📑 Сводная")])
    return ReplyKeyboardBuilder(kb_buttons).as_markup(resize_keyboard=True, one_time=True)

def cancel_keyboard():
    return ReplyKeyboardBuilder([[KeyboardButton(text="Отменить.")]]).as_markup(resize_keyboard=True, one_time=True)

def get_approve_kb(user_id: int):
    kb_buttons = [[InlineKeyboardButton(text=f"Удалить сессию", callback_data=f"delete:session:{user_id}", icon_custom_emoji_id=Emojis.go_away_id)]]
    return InlineKeyboardBuilder(kb_buttons).as_markup()

def yes_or_no():
    kb_buttons = [[InlineKeyboardButton(text="🗑️ Удалить", callback_data=f"delete:token")], [InlineKeyboardButton(text="↩️ Оставить", callback_data=f"delete:message")]]
    return InlineKeyboardBuilder(kb_buttons).as_markup()