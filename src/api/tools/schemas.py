from typing import Literal
from datetime import datetime

from pydantic import BaseModel


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
    repayment_date: datetime = datetime.min
    is_transfer: bool
    credit_type: Literal["give", "take"]
    count: float
