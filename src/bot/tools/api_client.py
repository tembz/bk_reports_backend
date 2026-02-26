from typing import Optional, TypeVar, Type

from pydantic import BaseModel
from aiohttp import ClientSession

from src.bot.config import config

T = TypeVar("T", bound=BaseModel)

class APIClient:

    def __init__(self):
        
        self.session: Optional[ClientSession] = None
        self.api_url = config.api_url