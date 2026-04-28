import logging

from typing import Optional, Literal
from datetime import datetime, timedelta

from fastapi import APIRouter, Request, Query
from fastapi.encoders import jsonable_encoder

from api.database.methods.report import get_db_reports, check_report, add_new_report, get_db_monthly_averages
from api.database.methods.user import get_user
from api.tools.bot import send_photos_to_chat, send_message_to_chat
from api.tools.responses import *
from api.tools.schemas import NewReport

logger = logging.getLogger(__name__)

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

    logger.info(
        "creating report | admin_id=%s report_type=%s date=%s photos=%s",
        admin_id,
        data.report_type,
        current_date.date(),
        len(photos),
    )

    report = await check_report(current_date, data.report_type)
    if report:
        logger.warning(
            "report already exists | admin_id=%s report_type=%s date=%s",
            admin_id,
            data.report_type,
            current_date.date(),
        )
        return HTTPError("report with this type already exists for today", 409)

    manager = await get_user(admin_id)

    if photos:
        logger.info(
            "sending report photos to telegram | admin_id=%s report_type=%s photos=%s",
            admin_id,
            data.report_type,
            len(photos),
        )
        await send_photos_to_chat(photos)
        logger.info(
            "report photos sent to telegram | admin_id=%s report_type=%s photos=%s",
            admin_id,
            data.report_type,
            len(photos),
        )

    logger.info(
        "sending report message to telegram | admin_id=%s report_type=%s date=%s",
        admin_id,
        data.report_type,
        current_date.date(),
    )
    await send_message_to_chat(data=data.model_dump(), date=current_date.strftime('%d.%m.%Y'), manager=manager.short_name)
    logger.info(
        "report message sent to telegram | admin_id=%s report_type=%s date=%s",
        admin_id,
        data.report_type,
        current_date.date(),
    )

    logger.info(
        "saving report to database | admin_id=%s report_type=%s date=%s",
        admin_id,
        data.report_type,
        current_date.date(),
    )
    await add_new_report(data.model_dump(), date=current_date, admin_id=admin_id)
    logger.info(
        "report saved | admin_id=%s report_type=%s date=%s",
        admin_id,
        data.report_type,
        current_date.date(),
    )

    return HTTPSuccess()

@report_handler.get("/monthly-averages")
async def get_monthly_averages(limit: int = Query(default=30, ge=1, le=100), offset: int = Query(default=0, ge=0), admin_id: Optional[int] = None):
    if admin_id is not None:
        manager = await get_user(admin_id)
        if not manager:
            return HTTPError("admin not found", 404)

    reports = await get_db_monthly_averages(offset, limit, admin_id)
    return HTTPSuccess()
