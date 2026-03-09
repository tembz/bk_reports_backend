import os
import logging
import tempfile
from datetime import datetime
from typing import List

from fastapi import UploadFile
from aiogram.types import FSInputFile, InputMediaPhoto
from aiogram.enums import ParseMode

from src.api.config import config
from src.api.tools.formatting import format_nums, format_seconds

logger = logging.getLogger(__name__)

async def send_photos_to_chat(photos: List[UploadFile]):
    media_group = []
    temp_files = []
    
    for idx, photo in enumerate(photos):
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(photo.filename)[1]) as tmp:
            contents = await photo.read()
            tmp.write(contents)
            tmp_path = tmp.name
            temp_files.append(tmp_path)
        
        input_file = FSInputFile(tmp_path)
        media_group.append(InputMediaPhoto(media=input_file))
        
        if len(media_group) == 10 or idx == len(photos) - 1:
            await config.bot.send_media_group(chat_id=config.admin_chat_id, media=media_group)
            media_group = []
    
    for tmp_path in temp_files:
        try:
            os.remove(tmp_path)
        except Exception as e:
            logger.error("Ошибка при удалении %s: %s", tmp_path, e)

async def send_message_to_chat(data: dict, date: str, manager: str):
    report_type = "День" if data['report_type'] == "day" else "Ночь"

    text = f"<code>📂 {report_type} | {date}.\n"+\
    f"- Менеджер: {manager}\n"+\
    f"- Заработано: {format_nums(int(data['money']))} ₽\n"+\
    f"- Обслужено гостей: {data['checks']}\n"+\
    f"- ITPH: {data['itph']}\n"+\
    f"- Негативные отзывы: {data['guest_experience']}\n"+\
    f"- ГО за смену: {round(int(data['guest_experience'])/int(data['checks']) * 10000, 1)}\n"+\
    f"- Время обслуживания: {format_seconds(int(data['sos']))} | {format_seconds(int(data['sos_delivery']))}</code>\n\n"
    if data['comments']:
        text = text + f"<pre><code class='language-Комментарии'>{data['comments']}</code></pre>"

    await config.bot.send_message(chat_id=config.admin_chat_id, parse_mode=ParseMode.HTML, text=text)

async def send_credit_message_to_chat(data: dict):
    credit_type = "Взяли" if data["credit_type"] == "take" else "Дали"
    text = (
        f"<code>🔔 Долг | {data['date'].strftime('%d-%m-%Y')}\n"
        f"- Действие: {credit_type}\n"
        f"- Ресторан: {data['restaurant']}\n"
        f"- Предмет: {data['what_take']}\n"
        f"- Ед. Измерения: {data['measurement_unit']}\n"
        f"- Количество: {data['count']}\n"
        + (
            f"- Дата возвращения: {datetime.fromisoformat(data['repayment_date']).strftime('%d-%m-%Y')}\n"
            if not data['is_transfer']
            else ""
        )
        + f"- Трансфер: {'Да' if data['is_transfer'] else 'Нет'}</code>"
    )

    await config.bot.send_message(chat_id=config.credit_chat_id, parse_mode=ParseMode.HTML, text=text)