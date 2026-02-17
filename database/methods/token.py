from typing import Optional

from sqlalchemy import select, update

from database.models import Token
from database.engine import db_session

async def get_user_id_by_code(code: int) -> Optional[Token]:
    async with db_session() as session:
        token = await session.execute(
            select(Token)
            .where(Token.code == code)
        )
        return token.scalar_one_or_none()
    
async def set_token(user_id: int, token: str) -> bool:
    async with db_session() as session:
        stmt = (
            update(Token)
            .where(Token.user_id == user_id)
            .values(
                token=token,
                code=None
            )
        )
        await session.execute(stmt)
        await session.commit()