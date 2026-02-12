from contextlib import asynccontextmanager

from aiogram import Bot
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from handlers import routers
from middlewares.auth import AuthMiddleware
from database.engine import engine
from database.models.base import Base

from config import config
from exceptions import *


@asynccontextmanager
async def main(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    config.bot = Bot(config.token)

    yield

    await config.bot.session.close()

app = FastAPI(lifespan=main)

app.add_middleware(AuthMiddleware)

for router in routers:
    app.include_router(router)

    