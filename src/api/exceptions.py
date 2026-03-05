from fastapi import HTTPException

class AuthError(HTTPException):
    def __init__(self):
        super().__init__(status_code=401)

class TokenOrInitDataRequired(HTTPException):
    def __init__(self):
        super().__init__(status_code=401)

class AccessDenied(HTTPException):
    def __init__(self):
        super().__init__(status_code=403)

class RateLimit(HTTPException):
    def __init__(self):
        super().__init__(status_code=429)