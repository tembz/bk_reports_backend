from typing import Optional, List
from datetime import datetime, timedelta

from fastapi import APIRouter, File, Request

from database.methods.report import get_db_reports, check_report, add_new_report
from database.methods.user import get_user
from tools.bot import send_photos_to_chat, send_message_to_chat
from tools.responses import *
from tools.schemas import NewReport

report_handler = APIRouter(prefix="/api/report")

@report_handler.get("/get")
async def get_reports(limit: int = 30, offset: int = 0):
    report_items = []
    reports = await get_db_reports(offset, limit)

    for report, short_name in reports:
        report_dict = report.__dict__.copy()
        report_dict.pop("comments", None)
        report_dict.update({
            "short_name": short_name,
            "report_type": "день" if report.report_type == "day" else "ночь",
            "comment": getattr(report, "comments", ""),
            "itph": float(report.itph)
        })
        report_items.append(report_dict)

    return HTTPSuccess({"items": report_items})


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