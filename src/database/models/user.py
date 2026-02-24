from sqlalchemy import BigInteger, String, UUID
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

class User(Base):
    
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    short_name: Mapped[str] = mapped_column(String)
    full_name: Mapped[str] = mapped_column(String)
    role: Mapped[str] = mapped_column(String)

    def __repr__(self):
        return (
            f"User(id={self.id}, short_name={self.short_name}, full_name={self.full_name}, role={self.role})"
        )