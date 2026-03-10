from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from pydantic import ValidationError

from api.exceptions import *
from api.tools.responses import HTTPError

async def auth_error_handler(request: Request, exc: AuthError):
    return HTTPError("Unauthorized", 401)

async def token_required_handler(request: Request, exc: TokenOrInitDataRequired):
    return HTTPError("Token or InitData is required", 401)

async def validation_error_handler(request: Request, exc: ValidationError):
    missing_errors = [e for e in exc.errors() if e["type"] == "missing"]

    if missing_errors:
        return HTTPError(
                error_name="missing required fields",
                code=422,
                error_data=[{"param": e["loc"][0]} 
                            for e in missing_errors])
    errors = exc.errors()

    if errors[0]["type"] == "literal_error":
        return HTTPError(
            error_name="invalid type",
            code=422,
            error_data={"param": errors[0]["loc"][0], "available": errors[0]["ctx"]["expected"]}
        )
    else:
        return HTTPError(
                error_name="validation error",
                code=422,
            )

async def request_validation_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    if errors[0]["type"] == "literal_error":
        return HTTPError(
            error_name="invalid type",
            code=422,
            error_data={"param": errors[0]["loc"][0], "available": errors[0]["ctx"]["expected"]}
        )
    return HTTPError(
        error_name="invalid query params",
        code=422,
        error_data=[{"param": e["loc"][-1], "msg": e["msg"]} for e in errors]
    )

async def internal_error_handler(request: Request, exc: Exception):
    return HTTPError("internal server error", 500)


