import base64
import hmac
import hashlib
from typing import Optional

from api.config import config

def decode_secret(secret: str) -> Optional[int]:
    try:
        raw = base64.urlsafe_b64decode(secret.encode()).decode()
        user_id, sig = raw.rsplit(":", 1)
        expected_sig = hmac.new(config.secret_key.encode(), str(user_id).encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig, expected_sig):
            return None
        return user_id
    except:
        return None

