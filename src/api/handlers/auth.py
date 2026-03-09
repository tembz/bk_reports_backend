import time
from secrets import token_hex, randbelow

from fastapi import APIRouter, Request

from src.api.database.methods.token import get_user_id_by_code, set_token, set_code, delete_code, get_token_by_user_id
from src.api.tools.responses import *

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
        await delete_code(code)
        return HTTPError("code expired", 410)

    token = token_hex(16)
    await set_token(code_info.user_id, token=token)

    return HTTPSuccess({"token": token, "user_id": code_info.user_id})

@auth_handler.post("/auth/createCode")
async def create_code(request: Request):

    user_id = request.state.admin_id
    token = await get_token_by_user_id(user_id)
    if token:
        return HTTPError("session already exists", 409)
    
    code = randbelow(9000) + 1000
    req = await set_code(user_id, code)

    if not req:
        return HTTPError("active code already exists", 409)


    return HTTPSuccess({"code": code})
