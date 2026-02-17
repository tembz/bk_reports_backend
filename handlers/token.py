from secrets import token_hex

from fastapi import APIRouter, Request

from database.methods.token import get_user_id_by_code, set_token

token_handler = APIRouter()

@token_handler.post("/auth/createToken")
async def create_token(request: Request):
    form = await request.json()

    code = form.get("code")
    try:
        code = int(code)
    except (TypeError, ValueError):
        return {"status": "error", "code": 400, "error": "code must be int"}
    code_info = await get_user_id_by_code(code)
    if not code_info:
        return {"status": "error", "code": 401, "error": "invalid code"}
    token = token_hex(10)

    await set_token(code_info.user_id, token=token)

    return {"status": "success", "data": {"ok": True, "user_id": code_info.user_id, "token": token}}