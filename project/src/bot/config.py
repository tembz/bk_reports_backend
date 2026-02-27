import tomllib
from typing import Optional
from dataclasses import dataclass

@dataclass
class Config:
    token: str
    owner_tg_id: int
    api_url: str
    smtp_server: Optional[str] = None
    smtp_port: Optional[int] = None
    email_user: Optional[str] = None
    email_password: Optional[str] = None
    to_email: Optional[str] = None

    @classmethod
    def load(cls, path: str = "config.toml") -> "Config":
        with open(path, "rb") as f:
            data = tomllib.load(f)

        email = data.get("email", {})

        return cls(
            token=data["telegram-bot"]["token"],
            owner_tg_id=data["admin"]["owner_tg_id"],
            api_url=data["server"]["api_url"],
            smtp_server=email.get("smtp_server"),
            smtp_port=email.get("smtp_port"),
            email_user=email.get("email_user"),
            email_password=email.get("email_password"),
            to_email=email.get("to_email"),
        )

config = Config.load()