from datetime import date, datetime
from typing import Any


def parse_date(value: Any) -> date | None:
    if value in (None, "", "<null>", "null"):
        return None

    if isinstance(value, datetime):
        return value.date()

    if isinstance(value, date):
        return value

    if isinstance(value, str):
        return datetime.fromisoformat(value).date()

    raise TypeError(f"Unsupported date value type: {type(value).__name__}")


def format_date(value: Any, fmt: str = "%d-%m-%Y") -> str:
    parsed_date = parse_date(value)
    if parsed_date is None:
        return ""

    return parsed_date.strftime(fmt)


def format_seconds(seconds: int) -> str:
    seconds = int(seconds)
    minutes = seconds // 60
    sec = seconds % 60
    return f"{minutes}:{sec:02d}"

def format_nums(num: int):
    return f"{num:,}".replace(",", ".")
