from fastapi import HTTPException

class AuthError(HTTPException):
    def __init__(self):
        super().__init__(status_code=401)

class TokenOrInitDataRequired(HTTPException):
    def __init__(self):
        super().__init__(status_code=401)