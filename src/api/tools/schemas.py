from typing import Literal
from datetime import datetime

from pydantic import BaseModel, field_validator


class NewReport(BaseModel):
    report_type: Literal["day", "night"]
    checks: int
    itph: float
    money: int
    sos: int
    sos_delivery: int
    guest_experience: int
    comments: str


class NewCredit(BaseModel):
    restaurant: int
    what_take: str
    measurement_unit: str
    repayment_date: datetime | None = None
    is_transfer: bool
    credit_type: Literal["give", "take", "дали", "взяли"]
    count: float

    @field_validator("repayment_date", mode="before")
    @classmethod
    def normalize_repayment_date(cls, value):
        if value in (None, "", "<null>", "null"):
            return None
        return value