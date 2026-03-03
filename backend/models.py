import enum
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Enum, Boolean
from sqlalchemy.sql import func
from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Date


class LoanStatus(str, enum.Enum):
    UPCOMING = "UPCOMING"
    DUE = "DUE"
    OVERDUE = "OVERDUE"
    PAID = "PAID"
    PAID_LATE = "PAID_LATE"


class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    due_date = Column(Date, nullable=False)
    payment_date = Column(Date, nullable=True)
    paid_amount = Column(Integer, nullable=True)

    status = Column(
        Enum(LoanStatus, name="loan_status", native_enum=False),
        default=LoanStatus.UPCOMING,
        nullable=False,
        index=True,
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ----------------------------------
# USER MODEL (AGENT LOGIN)
# ----------------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

from sqlalchemy import ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class EmailLog(Base):
    __tablename__ = "email_logs"

    id = Column(Integer, primary_key=True, index=True)

    loan_id = Column(Integer, ForeignKey("loans.id"), nullable=False)

    recipient_email = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    body = Column(Text, nullable=False)

    status = Column(String, default="SENT")
    email_type = Column(String, nullable=False)
    sent_at = Column(DateTime(timezone=True), server_default=func.now())

    loan = relationship("Loan")

class LoanStatus(str, enum.Enum):
    UPCOMING = "UPCOMING"
    DUE = "DUE"
    OVERDUE = "OVERDUE"
    PAID = "PAID"
    PAID_LATE = "PAID_LATE"
    NEEDS_ATTENTION = "NEEDS_ATTENTION"   # 👈 ADD THIS