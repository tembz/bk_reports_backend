import random
import time
from secrets import token_hex

from fastapi import APIRouter, Request

from src.database.methods.token import get_user_id_by_code, set_token, set_code, delete_code
from src.tools.tools import decode_secret
from src.tools.responses import *

auth_handler = APIRouter()

@auth_handler.post("/auth/createToken")
async def create_token(request: Request):
    form = await request.json()
    code = form.get("code")
    
    try:
        code = int(code)
    except (TypeError, ValueError):
        return HTTPError("code must be int", 400)
    
    code_info = await get_user_id_by_code(code)
    if not code_info:
        return HTTPError("invalid code", 401)
    
    if time.time() - code_info.created_at >= 300:
        await delete_code
        return HTTPError("code expired", 410)

    token = token_hex(16)
    await set_token(code_info.user_id, token=token)

    return HTTPSuccess({"token": token, "user_id": code_info.user_id})

@auth_handler.post("/auth/createCode")
async def create_code(request: Request):
    form = await request.json()

    secret = form.get("secret_key", "")
    user_id = decode_secret(secret)

    if not user_id:
        return HTTPError("Unauthorized", 401)
    code = random.randint(1111, 9999)
    req = await set_code(user_id, code)

    if not req:
        return HTTPError("active code already exists", 409)

    return HTTPSuccess({"code": code})
