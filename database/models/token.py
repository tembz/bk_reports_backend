from sqlalchemy import String, BigInteger, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

class Token(Base):
    __tablename__ = "tokens"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    token: Mapped[str] = mapped_column(String, nullable=True)
    code: Mapped[int] = mapped_column(Integer, nullable=True)