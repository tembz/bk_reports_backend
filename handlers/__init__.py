from .report import report_handler
from .credit import credit_handler
from .auth import auth_handler

routers = [report_handler, credit_handler, auth_handler]