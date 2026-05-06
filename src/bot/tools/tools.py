import hmac, base64, hashlib, datetime, mimetypes, os, logging
from email.message import EmailMessage

import aiofiles, aiosmtplib

from bot.config import config

logger = logging.getLogger(__name__)

def encode(user_id) -> str:
    sig = hmac.new(config.secret_key.encode(), str(user_id).encode(), hashlib.sha256).hexdigest()
    raw = f"{user_id}:{sig}"
    return base64.urlsafe_b64encode(raw.encode()).decode()

def round_time(dt=None):
    if dt is None:
        dt = datetime.datetime.now()
    
    hour = dt.hour
    minute = 30 if dt.minute >= 30 else 0
    
    return f"{hour:02d}:{minute:02d}"

def format_nums(num: int):
    return f"{num:,}".replace(",", ".")

def format_inline_text(code, time, money, itph, sos, sos_d, ge):
    text = f"📌 <b>{code}</b>\n" +\
            f"⏰ <b>{time}</b>\n" +\
            f"╔ ТО - <b>{format_nums(int(money))}</b> ₽\n" +\
            f"╠ ITPH - <b>{itph}</b>\n" +\
            f"╠ SOS - <b>{sos}</b>\n" +\
            f"╠ SOS дост - <b>{sos_d}</b>\n" +\
            f"╚ ГО - <b>{ge}</b>"
    return text


async def send_files_to_email(
    filenames: list[str],
    manager_name: str
):
    msg = EmailMessage()
    msg["From"] = config.email_user
    msg["To"] = config.to_email
    msg["Subject"] = "Отправка вложений."
    msg.set_content("Привет! Сообщение отправлено ботом, вложения приложены.\n\n✩ tembz")

    for file_path in filenames:
        if not os.path.isfile(file_path):
            logger.warning(
                "email attachment skipped: file not found | manager=%s filename=%s",
                manager_name,
                os.path.basename(file_path),
            )
            continue

        ctype, encoding = mimetypes.guess_type(file_path)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"

        maintype, subtype = ctype.split("/", 1)

        async with aiofiles.open(file_path, "rb") as file:
            payload = await file.read()

        msg.add_attachment(
            payload,
            maintype=maintype,
            subtype=subtype,
            filename=os.path.basename(file_path),
        )


    await aiosmtplib.send(
        msg,
        hostname=config.smtp_server,
        port=config.smtp_port,
        username=config.email_user,
        password=config.email_password,
        use_tls=False,
        start_tls=True
    )
    
