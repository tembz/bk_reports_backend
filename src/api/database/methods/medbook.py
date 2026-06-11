from sqlalchemy import select

from api.database.engine import db_session
from api.database.models import MedBook

async def get_medbooks(offset: int, limit: int):
    async with db_session() as session:
        stmt = (select(MedBook)
                .offset(offset)
                .limit(limit))
        result = await session.execute(stmt)
        return result.scalars().all()
    
async def add_new_book(name: str, inspect_end: str, fluorography_end: str, reference: bool):
    async with db_session() as session:
        book = MedBook(
            full_name = name,
            inspect_end = inspect_end,
            fluorography_end = fluorography_end,
            reference = reference
        )
        session.add(book)
        await session.execute()
        