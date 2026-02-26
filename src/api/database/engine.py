from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine, async_sessionmaker

from src.api.config import config

def get_engine() -> AsyncEngine:
    url = f"postgresql+asyncpg://{config.db_user}:{config.db_password}@{config.db_host}:{config.db_port}/{config.db_name}"
    return create_async_engine(url=url, echo=True)


engine = get_engine()
session_local = async_sessionmaker(engine, expire_on_commit=True)

@asynccontextmanager
async def db_session():
    async with AsyncSession(engine, expire_on_commit=True) as session:
        yield session