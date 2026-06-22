from app.database.connection import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone


class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    loan_date = Column(DateTime, default=datetime.now(timezone.utc))
    return_date = Column(DateTime, nullable=True)
    status = Column(String(20), nullable=False, default="active")

    user = relationship("User", back_populates="loans")
    device = relationship("Device", back_populates="loans")
