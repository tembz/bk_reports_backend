import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.tools.app_init import App

from src.api.handlers import routers
from src.api.middlewares import excs, middlewares

from src.api.config import config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

@asynccontextmanager
async def main(app: FastAPI):
    yield

    await config.bot.session.close()


app = App(
    middlewares=middlewares,
    routers=routers,
    exc_handlers=excs,
    lifespan=main
).init()
