from typing import Optional, Literal
from datetime import datetime, timedelta

from fastapi import APIRouter, Request, Query
from fastapi.encoders import jsonable_encoder

from src.api.database.methods.report import get_db_reports, check_report, add_new_report
from src.api.database.methods.user import get_user
from src.api.tools.bot import send_photos_to_chat, send_message_to_chat
from src.api.tools.responses import *
from src.api.tools.schemas import NewReport

report_handler = APIRouter(prefix="/api/report")

@report_handler.get("/get")
async def get_reports(limit: int = Query(default=30, ge=1, le=100), offset: int = Query(default=0, ge=0), date: Optional[str] = None, report_type: Optional[Literal["day", "night"]] = None):
    report_items = []
    reports = await get_db_reports(offset, limit, date, report_type)

    for report, short_name in reports:
        report_dict = report.__dict__.copy()
        report_dict.pop("_sa_instance_state", None)
        report_dict.pop("comments", None)
        report_dict.update({
            "short_name": short_name,
            "report_type": "день" if report.report_type == "day" else "ночь",
            "comment": getattr(report, "comments", ""),
            "itph": float(report.itph)
        })
        report_items.append(report_dict)

    return HTTPSuccess(jsonable_encoder({"items": report_items}))


@report_handler.post("/create")
async def create_new_report(request: Request):
    current_date = datetime.now()
    admin_id = request.state.admin_id
    content_type = request.headers.get("content-type", "")
    
    if "multipart/form-data" in content_type:
        source = await request.form()
        photos = [file for key, file in source.multi_items() if key.startswith("photo")]
        data = NewReport.model_validate(dict(source))
    else:
        source = await request.json()
        photos = []
        data = NewReport.model_validate(source)
    
    if data.report_type == "night":
        current_date = datetime.now() - timedelta(days=1)
    
    report = await check_report(current_date, data.report_type)
    if report:
        return HTTPError("report with this type already exists for today", 409)

    manager = await get_user(admin_id)

    if photos:
        await send_photos_to_chat(photos)
    await send_message_to_chat(data=data.model_dump(), date=current_date.strftime('%d.%m.%Y'), manager=manager.short_name)
    await add_new_report(data.model_dump(), date=current_date, admin_id=admin_id)

    return HTTPSuccess()