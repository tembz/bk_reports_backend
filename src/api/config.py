import tomllib
from typing import Optional
from dataclasses import dataclass

from aiogram import Bot

@dataclass
class Config:
    token: str
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str
    admin_roles: list[str]
    admin_chat_id: int
    credit_chat_id: int
    secret_key: str
    bot: Optional[Bot] = None

    @classmethod
    def load(cls) -> "Config":
        with open("config.toml", "rb") as f:
            data = tomllib.load(f)

        return cls(
            token=data["telegram-bot"]["token"],
            db_host=data["database"]["host"],
            db_port=data["database"]["port"],
            db_user=data["database"]["user"],
            db_password=data["database"]["password"],
            db_name=data["database"]["dbname"],
            admin_roles=data["admin"]["admin_roles"],
            admin_chat_id=data["admin"]["admin_chat_id"],
            credit_chat_id=data["admin"]["credit_chat_id"],
            secret_key=data["server"]["secret_key"],
            bot=Bot(token=data["telegram-bot"]["token"])
        )

config = Config.load()