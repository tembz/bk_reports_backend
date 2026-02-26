from pydantic import BaseModel

class OKData(BaseModel):
    ok: bool

class APIOK(BaseModel):
    status: str
    data: OKData