from .report import report_handler
from .credit import credit_handler
from .token import token_handler

routers = [report_handler, credit_handler, token_handler]