from sqlalchemy import select

from database.models.credit import Credit
from database.engine import db_session

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
