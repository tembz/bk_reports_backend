from secrets import token_hex

from aiogram import Router
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent

from bot.tools.api_client import api_client
from bot.schemas.user import UserResponse
from bot.tools.tools import round_time, format_inline_text

inline_router = Router()

@inline_router.inline_query()
async def parse_data(query: InlineQuery):

    user = await api_client.get(UserResponse, query.from_user.id)
    if not user:
        return await query.answer([
            InlineQueryResultArticle(
                id=token_hex(8),
                title=f"Функционал недоступен",
                input_message_content=InputTextMessageContent(
                    message_text=f"Функционал недоступен. За помощью обращаться к @tembzz",
                    disable_web_page_preview=True
                )
            )
        ])
    text = query.query
    code, money, itph, sos, sos_d, ge = text.split(",")
    time = round_time()
    text = format_inline_text(code, time, money, itph, sos, sos_d, ge)
    await query.answer([
        InlineQueryResultArticle(
            id=token_hex(8),
            title=f"Отчёт #{code} на {time}",
            input_message_content=InputTextMessageContent(
                message_text=text,
                disable_web_page_preview=True
            )
        )
    ])
