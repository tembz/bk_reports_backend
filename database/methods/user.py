from typing import Optional
from sqlalchemy import select

from database.engine import db_session
from database.models import User, Token


async def get_user(user_id: int) -> Optional[User]:
    async with db_session() as session:
        user = await session.execute(select(User).where(User.id == user_id))
        return user.scalar_one_or_none()
    

async def check_token(token: str) -> Optional[int]:
    async with db_session() as session:
        check = await session.execute(select(Token).where(Token.token == token))
        result = check.scalar_one_or_none()
        if result:
            return result.user_id
        return result