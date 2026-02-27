from typing import Optional, TypeVar, Type, List, Union
from io import BytesIO

from aiogram import Bot
from pydantic import BaseModel
from aiohttp import ClientSession, FormData

from src.bot.config import config
from src.bot.tools.tools import encode
from src.bot.schemas.error import ErrorResponse, APIError


T = TypeVar("T", bound=BaseModel)

class APIClient:

    def __init__(self):
        
        self.session: Optional[ClientSession] = None
        self.api_url = config.api_url

    async def get(self,
                  model: Type[T],
                  user_id: int, 
                  path: str,
                  **params) -> T:
        secret_key = encode(user_id)
        headers = {"SecretKey": secret_key}

        async with self.session.get(path, headers=headers, params=params) as resp:
            data = await resp.json()
            if not resp.ok:
                raise APIError(ErrorResponse.model_validate(data))
            return model.model_validate(data)

    async def post(self,
                   model: Type[T],
                   user_id: int, 
                   path: str,
                   photos: Optional[List[str]] = None, # photo_file_id
                   bot: Optional[Bot] = None,
                   **params) -> T:
        secret_key = encode(user_id)
        headers = {"SecretKey": secret_key}
        form = await self.create_form(photos, bot, **params)

        async with self.session.post(path, headers=headers, data=form) as resp:
            data = await resp.json()
            if not resp.ok:
                raise APIError(ErrorResponse.model_validate(data))
            return model.model_validate(data)
        
    async def create_form(self, photos: Optional[List[str]] = None, bot: Optional[Bot] = None, **params) -> Union[FormData, dict]:
        if photos:
            form = FormData()
            for key, value in params.items():
                form.add_field(key, str(value))
            for i, file_id in enumerate(photos):
                file = await bot.get_file(file_id)
                buffer = BytesIO()
                await bot.download_file(file.file_path, buffer)
                form.add_field(f"photo{i}", buffer.getvalue(), filename=f"photo{i}.jpg", content_type="image/jpeg")
            body = form
        else:
            body = params

        return body
        
    async def start(self):
        self.session = ClientSession(config.api_url)

    async def stop(self):
        if self.session:
            await self.session.close()


api_client = APIClient()