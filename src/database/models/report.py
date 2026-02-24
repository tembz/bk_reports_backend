import uuid
from sqlalchemy import text
from sqlalchemy import BigInteger, Float, String, JSON, Date
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from .base import Base

class Report(Base):
    __tablename__ = "reports"

    report_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("uuid_generate_v4()")  # uuid-ossp
    )
    admin_id: Mapped[int] = mapped_column(BigInteger)
    report_type: Mapped[int] = mapped_column(String)
    date: Mapped[str] = mapped_column(Date)
    timestamp: Mapped[float] = mapped_column(Float)
    checks: Mapped[int] = mapped_column(BigInteger)
    itph: Mapped[float] = mapped_column(Float)
    money: Mapped[int] = mapped_column(BigInteger)
    sos: Mapped[int] = mapped_column(BigInteger)
    sos_delivery: Mapped[int] = mapped_column(BigInteger)
    guest_experience: Mapped[int] = mapped_column(BigInteger)
    comments: Mapped[str] = mapped_column(String, nullable=True, default=None)

    def __repr__(self):
        return (
            f"Report(report_id={self.report_id}, admin_id={self.admin_id},"
            f"report_type={self.report_type}, date={self.date}, timestamp={self.timestamp},"
            f"checks={self.checks}, itph={self.itph}, money={self.money}, sos={self.sos},"
            f"sos_dilivery={self.sos_delivery}, guest_experience={self.guest_experience}, comments={self.comments})"
        )