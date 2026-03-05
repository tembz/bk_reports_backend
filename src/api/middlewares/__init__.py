from .auth import AuthMiddleware
from .rate_limit import RateLimitMiddleware
from .exc_handlers import (
    auth_error_handler,
    token_required_handler,
    validation_error_handler,
    request_validation_handler,
    internal_error_handler,
    AuthError,
    TokenOrInitDataRequired,
    ValidationError,
    RequestValidationError
)

excs = [[AuthError, auth_error_handler], 
        [TokenOrInitDataRequired, token_required_handler], 
        [ValidationError, validation_error_handler], 
        [Exception, internal_error_handler],
        [RequestValidationError, request_validation_handler]]

middlewares = [RateLimitMiddleware, AuthMiddleware,]