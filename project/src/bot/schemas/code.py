from pydantic import BaseModel

class CodeInfo(BaseModel):
    code: int

class CodeResponse(BaseModel):
    status: str
    data: CodeInfo