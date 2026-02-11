from datetime import datetime
from sqlalchemy import (String, 
                        Boolean, 
                        BigInteger, 
                        Integer, 
                        Date, 
                        Float)
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

class Credit(Base):
    __tablename__ = "credits"

    id: Mapped[int] = mapped_column(BigInteger, autoincrement=True, primary_key=True)              
    date: Mapped[str] = mapped_column(Date, nullable=False, default=datetime.date())
    restaurant: Mapped[int] = mapped_column(BigInteger, nullable=False)
    what_take: Mapped[str] = mapped_column(String, nullable=False)
    measurement_unit: Mapped[str] = mapped_column(String, nullable=False)
    repayment_date: Mapped[str] = mapped_column(Date, nullable=True)
    is_transfer: Mapped[bool] = mapped_column(Boolean, nullable=False)
    credit_type: Mapped[str] = mapped_column(String, nullable=False)
    count: Mapped[float] = mapped_column(Float, nullable=False)
    case_count: Mapped[str] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)