from typing import ClassVar

from pydantic import BaseModel

class UserData(BaseModel):
    short_name: str
    full_name: str
    role: str

class UserResponse(BaseModel):
    path: ClassVar[str] = "api/user/get"
    status: str
    data: UserData