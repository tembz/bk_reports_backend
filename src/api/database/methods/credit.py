from sqlalchemy import select, update, not_

from api.database.models.credit import Credit
from api.database.engine import db_session
from api.tools.formatting import parse_date

async def get_db_credits(offset: int, limit: int):
    stmt = (
        select(Credit)
        .order_by(
            Credit.is_active.desc(),
            Credit.date.desc(),
            Credit.id.desc(),
        )
        .offset(offset)
        .limit(limit)
    )
    async with db_session() as session:
        result = await session.execute(stmt)
        return result.scalars().all()

async def update_credit_status(credit_id: int):
    async with db_session() as session:
        result = await session.execute(
            update(Credit)
            .values(is_active=not_(Credit.is_active))
            .returning(Credit.is_active)
            .where(Credit.id == credit_id)
        )
        await session.commit()
        return result.scalar_one()
        
async def add_new_credit(data: dict):
    credit = Credit(
        date=parse_date(data["date"]),
        restaurant=data["restaurant"],
        what_take=data["what_take"],
        measurement_unit=data["measurement_unit"],
        repayment_date=parse_date(data["repayment_date"]),
        is_transfer=data["is_transfer"],
        credit_type=data["credit_type"],
        count=data["count"],
        is_active=True,
        case_count=""
    )
    async with db_session() as session:
        session.add(credit)
        await session.commit()
    
