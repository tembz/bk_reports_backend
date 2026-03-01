from typing import ClassVar

from pydantic import BaseModel

class CodeInfo(BaseModel):
    code: int

class CodeResponse(BaseModel):
    path: ClassVar[str] = "auth/createCode"
    status: str
    data: CodeInfo