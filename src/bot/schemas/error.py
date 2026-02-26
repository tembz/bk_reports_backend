from typing import Optional, Any

from pydantic import BaseModel

class ErrorResponse(BaseModel):
    status: str
    code: int
    error: str
    details: Optional[Any] = None

class APIError(Exception):
    def __init__(self, response: ErrorResponse):
        self.response = response
        super().__init__(response.error)