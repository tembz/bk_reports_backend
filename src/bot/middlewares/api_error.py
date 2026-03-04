import logging

from aiogram.handlers import ErrorHandler

from src.bot.tools.emojis import Emojis

logger = logging.getLogger(__name__)

class APIErrorHandler(ErrorHandler):

    async def handle(self):
        upd = self.event.update
        text = f'{Emojis.cry} Произошла ошибка при запросе к API, попробуйте позже.'

        logger.error(
            "API request failed. Error: %s (details %s)",
            self.event.exception,
            self.event.exception.details or "no details"
        )

        if upd.message:
            return await upd.message.answer(text)
        if upd.callback_query:
            return await upd.callback_query.message.answer(text)