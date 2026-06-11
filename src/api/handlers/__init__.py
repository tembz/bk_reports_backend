from .report import report_handler
from .credit import credit_handler
from .auth import auth_handler
from .user import user_handler
from .medbook import medbook_handler

routers = [report_handler, credit_handler, auth_handler, user_handler]