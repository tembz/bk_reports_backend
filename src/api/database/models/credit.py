import uuid
from datetime import datetime
from sqlalchemy import (String, 
                        Boolean, 
                        BigInteger, 
                        Date, 
                        Float,
                        text)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from .base import Base

class Credit(Base):
    __tablename__ = "credits"

    credit_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("uuid_generate_v4()")  # uuid-ossp
    )
    id: Mapped[int] = mapped_column(BigInteger, autoincrement=True)              
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False, default=datetime.today)
    restaurant: Mapped[int] = mapped_column(BigInteger, nullable=False)
    what_take: Mapped[str] = mapped_column(String, nullable=False)
    measurement_unit: Mapped[str] = mapped_column(String, nullable=False)
    repayment_date: Mapped[str] = mapped_column(Date, nullable=True)
    is_transfer: Mapped[bool] = mapped_column(Boolean, nullable=False)
    credit_type: Mapped[str] = mapped_column("type", String, nullable=False)
    count: Mapped[float] = mapped_column(Float, nullable=False)
    case_count: Mapped[str] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)

    def __repr__(self):
        return (
            f"Credit(id={self.id}, date={self.date}, restaurant={self.restaurant}, "
            f"what_take={self.what_take}, measurement_unit={self.measurement_unit}, "
            f"repayment_date={self.repayment_date}, is_transfer={self.is_transfer}, "
            f"credit_type={self.credit_type}, count={self.count}, "
            f"case_count={self.case_count}, is_active={self.is_active})"
        )