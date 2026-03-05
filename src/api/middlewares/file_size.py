from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from src.api.tools.responses import HTTPError

class FileSizeMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, dispatch = None):
        super().__init__(app)

    async def dispatch(self, request, call_next):
        if request.method == "POST":
            content_length = request.headers.get("content-length")
            if content_length and int(content_length) > 50 * 1024 * 1024:
                return HTTPError("file too large", 413)
        return await call_next(request)