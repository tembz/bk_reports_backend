from typing import Optional, List
from datetime import datetime, timedelta

from fastapi import APIRouter, UploadFile, File, Request

from database.methods.report import get_db_reports, check_report, add_new_report
from database.methods.user import get_user
from tools.bot import send_photos_to_chat, send_message_to_chat

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
            "report_type": "день" if report.report_type == "day" else "ночь" if report.report_type == "night" else report.report_type,
            "comment": getattr(report, "comments", ""),
            "itph": float(report.itph)
        })
        report_items.append(report_dict)

    return {
        "status": "success",
        "data": {
            "items": report_items,
            "ok": True
        }
    }


@report_handler.post("/create")
async def create_new_report(request: Request):
    current_date = datetime.now()
    admin_id = request.state.admin_id
    content_type = request.headers.get("content-type", "")
    
    if "multipart/form-data" in content_type:
        form = await request.form()
        data = {
            "report_type": form.get("report_type"),
            "checks": int(form.get("checks", 0)),
            "itph": float(form.get("itph", 0)),
            "money": int(form.get("money", 0)),
            "sos": int(form.get("sos", 0)),
            "sos_delivery": int(form.get("sos_delivery", 0)),
            "guest_experience": int(form.get("guest_experience", 0)),
            "comments": form.get("comments", "")
        }
        photos: List[UploadFile] = [file for key, file in form.multi_items() if key.startswith("photo")]
    else:
        json_data = await request.json()
        data = {
            "report_type": json_data.get("report_type"),
            "checks": int(json_data.get("checks", 0)),
            "itph": float(json_data.get("itph", 0)),
            "money": int(json_data.get("money", 0)),
            "sos": int(json_data.get("sos", 0)),
            "sos_delivery": int(json_data.get("sos_delivery", 0)),
            "guest_experience": int(json_data.get("guest_experience", 0)),
            "comments": json_data.get("comments", "")
        }
        photos = []
    
    report_type = data["report_type"]
    if report_type == "night":
        current_date = datetime.now() - timedelta(days=1)
    
    report = await check_report(current_date, report_type)
    if report:
        return {"status": "success", "data": {"ok": False, "items": [], "msg": "Отчёт такого типа за сегодня уже существует."}}
    
    manager = await get_user(admin_id)
    

    if photos:
        await send_photos_to_chat(photos)
    await send_message_to_chat(data=data, date=current_date.strftime('%d.%m.%Y'), manager=manager.short_name)
    await add_new_report(data, date=current_date, admin_id=admin_id)
    
    return {"status": "success", "data": {"ok": True}}