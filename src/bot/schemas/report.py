from typing import List, ClassVar

from pydantic import BaseModel

class ReportItems(BaseModel):
    report_id: str
    date: str
    checks: int
    money: int
    sos: int
    sos_delivery: int
    admin_id: int
    timestamp: float
    report_type: str
    itph: float
    guest_experience: int
    short_name: str
    comment: str

class ReportData(BaseModel):
    items: List[ReportItems]
    ok: bool

class ReportResponse(BaseModel):
    path: ClassVar[str] = "api/report/get"
    status: str
    data: ReportData