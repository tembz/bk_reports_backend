from .start import start_router
from .report import report_router
from .code import code
from .inline import inline_router
from .email import email_router

routers = [start_router, report_router, code, inline_router, email_router]