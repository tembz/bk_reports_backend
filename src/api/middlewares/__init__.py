from .auth import AuthMiddleware
from .exc_handlers import (
    auth_error_handler,
    token_required_handler,
    validation_error_handler,
    internal_error_handler,
    AuthError,
    TokenOrInitDataRequired,
    ValidationError,
)

excs = [[AuthError, auth_error_handler], 
        [TokenOrInitDataRequired, token_required_handler], 
        [ValidationError, validation_error_handler], 
        [Exception, internal_error_handler]]

middlewares = [AuthMiddleware,]