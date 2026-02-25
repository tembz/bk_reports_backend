from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from aiogram.utils.web_app import safe_parse_webapp_init_data

from src.config import config
from src.exceptions import AuthError, TokenOrInitDataRequired, AccessDenied
from src.database.methods.user import get_user, check_token

class AuthMiddleware(BaseHTTPMiddleware):

    def __init__(self, app, dispatch = None):
        super().__init__(app)

    async def dispatch(self, request, call_next):
        try:
            if request.url.path == "/auth/createToken":
                return await call_next(request)
            init_data_result = await self.check_init_data(request)
            if init_data_result:
                check_user = await get_user(init_data_result)
                if check_user.role not in config.admin_roles:
                    raise AccessDenied
                if not check_user:
                    raise AuthError
                request.state.admin_id = init_data_result
                return await call_next(request)
            
            token_result = await self.check_token(request)
            if token_result is False:
                raise AuthError
            if token_result:
                request.state.admin_id = token_result
                return await call_next(request)
            
            raise TokenOrInitDataRequired
        except AuthError:
            return JSONResponse(content={"code": 401, "error": "Unauthorized", "status": "error"}, status_code=401)
        except TokenOrInitDataRequired:
            return JSONResponse(content={"code": 401, "error": "Token or InitData is required", "status": "error"}, status_code=401)
        except AccessDenied:
            return JSONResponse(content={"code": 403, "error": "access deniend", "status": "error"}, status_code=403)
        
    async def check_token(self, request: Request) -> int | bool | None:
        token = None

        if request.method == "POST":
            auth = request.headers.get("Authorization")
            if auth and auth.startswith("Bearer "):
                token = auth.split("Bearer ")[1]
        else:
            token = request.query_params.get("token")
        if not token:
            return False
        
        check_token_result = await check_token(token=token)
        if check_token_result:
            return check_token_result
        else:
            return False

    async def check_init_data(self, request: Request) -> int | bool:
        init_data = None

        if request.method == "POST":
            init_data = request.headers.get("InitData")
            if not init_data:
                return False
        else:
            init_data = request.query_params.get("init_data")

        if not init_data:
            return False
        try:
            parse_init_data = await safe_parse_webapp_init_data(config.token, init_data)
            return parse_init_data.user.id
        except ValueError:
            return False