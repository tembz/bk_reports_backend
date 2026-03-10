from fastapi import APIRouter, Request

from api.database.methods.user import get_user
from api.tools.responses import HTTPSuccess, HTTPError


user_handler = APIRouter(prefix="/api/user")


@user_handler.get("/get")
async def get_user_info(request: Request):
    user_id = request.state.admin_id

    user = await get_user(user_id)
    if not user:
        return HTTPError("user not found", 404)
    
    return HTTPSuccess(data={
        "full_name": user.full_name,
        "short_name": user.short_name,
        "role": user.role,
        "tg_id": user.id
    })