import time
from datetime import datetime

from sqlalchemy import text, select, func, String

from api.database.models import Report, User
from api.database.engine import db_session

async def get_db_reports(offset: int, limit: int, date: datetime = None, report_type: str = None):
    stmt = (
        select(Report, User.short_name)
        .join(User, User.id == Report.admin_id)
        .order_by(Report.timestamp.desc())
        .offset(offset)
        .limit(limit)
    )
    if date:
        stmt = stmt.where(Report.date == datetime.strptime(date, "%Y-%m-%d").date())
    if report_type:
        stmt = stmt.where(Report.report_type == report_type)

    async with db_session() as session:
        result = await session.execute(stmt)
        return result.all()

async def add_new_report(data: dict, date: str, admin_id: int):
    async with db_session() as session:
        report = Report(
            admin_id = admin_id,
            report_type=data['report_type'],
            date=date,
            timestamp=time.time(),
            checks=data['checks'],
            itph=data['itph'],
            money=data['money'],
            sos=data['sos'],
            sos_delivery=data['sos_delivery'],
            guest_experience=data['guest_experience'],
            comments=data["comments"]
        )
        session.add(report)
        await session.commit()

async def check_report(date: str, report_type: str):
    async with db_session() as session:
        report = await session.execute(
            select(Report)
            .where(Report.report_type == report_type, Report.date == date.date())
            )
        return report.scalar_one_or_none()
    
async def search_reports(q: str):
    async with db_session() as session:
        stmt = (
            select(Report, User.short_name)
            .join(User, User.id == Report.admin_id)
            .where(
                func.to_tsvector(
                    'simple',
                    func.concat_ws(
                        ' ',
                        Report.comments.cast(String),
                        Report.date.cast(String),
                        Report.report_type.cast(String),
                    )
                ).op("@@")(
                    func.plainto_tsquery('simple', q)
                )
            )
            .limit(30)
        )
        result = await session.execute(stmt)
        return result.all()