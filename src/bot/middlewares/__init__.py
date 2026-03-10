from aiohttp.client_exceptions import ClientConnectionError

from .white_list import WhiteList
from .any_error import AnyErrorHandler

from .api_error import APIErrorHandler

from bot.schemas import APIError

middlewares = [WhiteList]
exc_handlers = [
    (APIErrorHandler, (APIError, ClientConnectionError)),
    (AnyErrorHandler, (Exception,))
]