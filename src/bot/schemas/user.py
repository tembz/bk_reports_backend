from pydantic import BaseModel

class UserData(BaseModel):
    short_name: str
    full_name: str
    role: str

class UserResponse(BaseModel):
    status: str
    data: UserData