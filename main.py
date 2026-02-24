from contextlib import asynccontextmanager

from fastapi import FastAPI

from tools.app_init import App

from handlers import routers
from middlewares import excs, middlewares

from config import config
from database.models.base import Base
from database.engine import engine

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
