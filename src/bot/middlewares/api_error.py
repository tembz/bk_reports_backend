import logging

from aiogram.handlers import ErrorHandler

logger = logging.getLogger(__name__)

class APIErrorHandler(ErrorHandler):

    async def handle(self):
        upd = self.event.update
        text = '<tg-emoji emoji-id="5471921818392600919">😭</tg-emoji> Произошла ошибка при запросе к API, попробуйте позже.'

        logger.error(
            "API request failed. Error: %s",
            self.event.exception
        )

        if upd.message:
            return await upd.message.answer(text)
        if upd.callback_query:
            return await upd.callback_query.message.answer(text)