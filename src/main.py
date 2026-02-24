from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.tools.app_init import App

from src.handlers import routers
from src.middlewares import excs, middlewares

from src.config import config
from src.database.models.base import Base
from src.database.engine import engine

@asynccontextmanager
async def main(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

    await config.bot.session.close()


app = App(
    middlewares=middlewares,
    routers=routers,
    exc_handlers=excs,
    lifespan=main
).init()
