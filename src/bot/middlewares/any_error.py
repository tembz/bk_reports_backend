import logging

from aiogram.handlers import ErrorHandler

from src.bot.tools.emojis import Emojis

logger = logging.getLogger(__name__)

class AnyErrorHandler(ErrorHandler):

    async def handle(self):
        upd = self.event.update
        text = f'{Emojis.cry} Произошла неизвестная ошибка, попробуйте позже.'

        logger.error(
            "Unhandled error: %s",
            self.event.exception
        )

        if upd.message:
            return await upd.message.answer(text)
        if upd.callback_query:
            return await upd.callback_query.message.answer(text)