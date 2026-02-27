from fastapi import Request
from fastapi.responses import JSONResponse

from pydantic import ValidationError

from src.api.exceptions import *
from src.api.tools.responses import HTTPError

async def auth_error_handler(request: Request, exc: AuthError):
    return JSONResponse(
        status_code=401,
        content=HTTPError("Unauthorized", 401)
    )

async def token_required_handler(request: Request, exc: TokenOrInitDataRequired):
    return JSONResponse(
        status_code=401,
        content=HTTPError("Token or InitData is required", 401)
    )

async def validation_error_handler(request: Request, exc: ValidationError):
    missing_errors = [e for e in exc.errors() if e["type"] == "missing"]

    if missing_errors:
        return JSONResponse(
            status_code=422,
            content=HTTPError(
                error_name="missing required fields",
                code=422,
                error_data=[{"param": e["loc"][0]} 
                            for e in missing_errors])
        )
    errors = exc.errors()

    if errors[0]["type"] == "literal_error":
        return JSONResponse(
            status_code=422,
            content=HTTPError(
                error_name="invalid type",
                code=422,
                error_data={"param": errors[0]["loc"][0], "available": errors[0]["ctx"]["expected"]}
            )
        )
    else:
        return JSONResponse(
            status_code=422,
            content=HTTPError(
                error_name="validation error",
                code=422,
            )
        )

async def internal_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=HTTPError("internal server error", 500)
    )

