import base64
import hmac
import hashlib
import json
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

def parse_filter(filters: str, type: str) -> Optional[dict]:
    report_available_field_names = ["day", "night"]
    credit_available_field_names = []

    try:
        data = json.loads(filters)
        allowed = report_available_field_names if type == "report" else credit_available_field_names
        return {k: v for k, v in data.items() if k in allowed}
    except:
        return None