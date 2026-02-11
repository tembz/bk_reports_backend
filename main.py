from aiogram import Bot
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from handlers import routers
from database.engine import engine
from database.models.base import Base

from config import config
from exceptions import *

app = FastAPI()

@app.exception_handler(AuthError)
async def auth_exc_handler(request: Request, exc: AuthError):
    return JSONResponse(content={"code": 401, "error": "Unauthorized", "status": "error"}, status_code=401)

@app.exception_handler(TokenOrInitDataRequired)
async def auth_param_exc_handler(request: Request, exc: TokenOrInitDataRequired):
    return JSONResponse(content={"code": 401, "error": "Token or InitData is required", "status": "error"}, status_code=401)

async def main():
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()
    config.bot = Bot(config.token)

    for router in routers:
        app.include_router(router)

    
    