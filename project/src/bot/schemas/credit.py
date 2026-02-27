from typing import List

from pydantic import BaseModel

class CreditItems(BaseModel):
    date: str
    what_take: str
    id: int
    repayment_date: str
    count: float
    case_count: str
    measurement_unit: str
    restaurant: int
    is_transfer: bool
    credit_type: str
    is_active: bool

class CreditData(BaseModel):
    items: List[CreditItems]
    ok: bool

class CreditResponse:
    status: str
    data: CreditData