from datetime import datetime

from aiogram.filters import Filter
from aiogram.types import Message

class SosTimeFilter(Filter):

    async def __call__(self, m: Message):
        times = m.text.replace(" ", "").split(",")
        for time in times:
            try:
                datetime.strptime(time, "%M:%S")
            except:
                await m.answer("Указан неверный формат. Пожалуйста, пришли мне SOS в формате:\n"
                "<blockquote><b>MM:СС, MM:СС</b></blockquote>")
                return False
        return True