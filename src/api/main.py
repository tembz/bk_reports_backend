import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.tools.app_init import App

from api.handlers import routers
from api.middlewares import excs, middlewares

from api.config import config
from api.database.methods.user import create_owner_if_not_exists
from api.database.engine import engine
from api.database.models import base

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

@asynccontextmanager
async def main(app: FastAPI):
    await create_owner_if_not_exists()
    yield
    await config.bot.session.close()


app = App(
    middlewares=middlewares,
    routers=routers,
    exc_handlers=excs,
    lifespan=main
).init()
