import hmac, base64, hashlib, datetime

from bot.config import config

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

