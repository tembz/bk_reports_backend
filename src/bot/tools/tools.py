import hmac, base64, hashlib

from src.bot.config import config

def encode(user_id) -> str:
    sig = hmac.new(config.secret_key.encode(), str(user_id).encode(), hashlib.sha256).hexdigest()
    raw = f"{user_id}:{sig}"
    return base64.urlsafe_b64encode(raw.encode()).decode()