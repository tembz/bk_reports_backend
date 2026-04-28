from typing import Optional
from sqlalchemy import select

from api.database.engine import db_session
from api.database.models import User, Token
from api.config import config


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
    
async def create_owner_if_not_exists() -> None:
    async with db_session() as session:
        result = await session.execute(select(User).where(User.id == config.owner_tg_id))
        if result.scalar_one_or_none():
            return
        
        owner = User(
            id=config.owner_tg_id,
            short_name="owner",
            full_name="Owner",
            role="owner"
        )
        session.add(owner)
        await session.commit()