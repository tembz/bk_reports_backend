import time

from sqlalchemy import text, select

from src.database.models import Report, User
from src.database.engine import db_session

async def get_db_reports(offset: int, limit: int):
    stmt = (
        select(Report, User.short_name)
        .join(User, User.id == Report.admin_id)
        .order_by(Report.timestamp.desc())
        .offset(offset)
        .limit(limit)
    )

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