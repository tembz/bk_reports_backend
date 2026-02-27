from sqlalchemy import String, BigInteger, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

class Token(Base):
    __tablename__ = "tokens"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    token: Mapped[str] = mapped_column(String, nullable=True)
    code: Mapped[int] = mapped_column(Integer, nullable=True)
    created_at: Mapped[float] = mapped_column(Float, nullable=True)

    def __repr__(self):
        return (
            f"Token(user_id={self.user_id}, token={self.token}, "
            f"code={self.code}, created_at={self.created_at})"
        )