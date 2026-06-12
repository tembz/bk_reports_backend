from sqlalchemy import select, update, not_, func, String

from api.database.models.credit import Credit
from api.database.methods.filters import apply_credit_filters
from api.database.engine import db_session
from api.tools.formatting import parse_date

async def get_db_credits(offset: int, limit: int, filters: dict | None = None):
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
    if filters:
        stmt = apply_credit_filters(stmt, filters)
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
    
async def search_credits(q: str, filters: dict | None = None):
    async with db_session() as session:
        stmt = (
            select(Credit)
            .where(
                func.to_tsvector(
                    'simple',
                    func.concat_ws(
                        ' ',
                        Credit.what_take.cast(String),
                        Credit.restaurant.cast(String),
                        Credit.measurement_unit.cast(String),
                        Credit.repayment_date.cast(String),
                    )
                ).op("@@")(
                    func.plainto_tsquery('simple', q)
                )
            )
            .limit(30)
        )
        if filters:
            stmt = apply_credit_filters(stmt, filters)
        result = await session.execute(stmt)
        return result.scalars().all()