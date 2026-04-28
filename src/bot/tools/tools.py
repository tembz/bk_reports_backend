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

def format_inline_text(code, time, money, itph, sos, sos_d, ge):
    text = f"<code>📊 {time} (#{code})\n" +\
            f"⨯ ТО: {money}\n" +\
            f"⨯ ITPH: {itph}\n" +\
            f"⨯ SOS: {sos} / {sos_d}\n" +\
            f"⨯ ГО - {ge}\n</code>"
    return text