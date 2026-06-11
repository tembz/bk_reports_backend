from datetime import datetime

from sqlalchemy import BigInteger, String, Date, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

class MedBook(Base):

    __tablename__ = "medbooks"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    inspect_end: Mapped[str] = mapped_column(Date, nullable=True)
    fluorography_end: Mapped[str] = mapped_column(Date, nullable=True)
    reference: Mapped[bool] = mapped_column(Boolean, nullable=False)