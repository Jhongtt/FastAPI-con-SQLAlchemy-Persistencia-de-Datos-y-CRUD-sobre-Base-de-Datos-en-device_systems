from app.database.connection import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    serial_number = Column(String(50), unique=True, nullable=False)
    device_type = Column(String(30), nullable=False)
    brand = Column(String(50), nullable=True)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    loans = relationship("Loan", back_populates="device")
