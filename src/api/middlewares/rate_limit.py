import logging

from cachetools import TTLCache

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from api.exceptions import RateLimit
from api.tools.responses import HTTPError

logger = logging.getLogger(__name__)

class RateLimitMiddleware(BaseHTTPMiddleware):

    def __init__(self, app, dispatch = None):
        super().__init__(app)
        self.cache = TTLCache(maxsize=10000, ttl=60)

    async def dispatch(self, request, call_next):
        try:
            user_ip = request.client.host if request.client else "unknown"
            request_path = request.url.path
            self.cache[user_ip] = self.cache.get(user_ip, 0) + 1
            count = self.cache[user_ip]

            if request_path == "/auth/createToken":
                if count > 5:
                    raise RateLimit
            elif count > 20:
                raise RateLimit

            return await call_next(request)
        except RateLimit:
            logger.warning(
                "rate limit exceeded | path=%s method=%s ip=%s count=%s",
                request_path,
                request.method,
                user_ip,
                count,
            )
            return HTTPError("too many requests", 429)
