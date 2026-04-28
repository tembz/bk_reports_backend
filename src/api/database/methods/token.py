import time
from typing import Optional

from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError

from api.database.models import Token
from api.database.engine import db_session

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
        return True

async def set_code(user_id: int, code: int) -> bool:
    async with db_session() as session:
        try:
            new = Token(user_id=user_id, code=code, created_at=time.time())
            session.add(new)
            await session.commit()
            return True
        except IntegrityError:
            return False
        
async def delete_code(code: int) -> None:
    async with db_session() as session:
        await session.execute(
            delete(Token)
            .where(Token.code == code)
        )
        await session.commit()


async def get_token_by_user_id(user_id: int) -> Optional[Token]:
    async with db_session() as session:
        token = await session.execute(
            select(Token)
            .where(Token.user_id == user_id)
        )
        return token.scalar_one_or_none()
    
async def delete_token(user_id: int) -> None:
    async with db_session() as session:
        await session.execute(
            delete(Token)
            .where(Token.user_id == user_id)
        )
        await session.commit()