from sqlalchemy import Column, Integer, String, Float, DateTime
from app.utils.database import Base
from datetime import datetime

class Receipt(Base):
    __tablename__ = "receipt"

    id = Column(Integer, primary_key=True, index=True)
    purchased_at = Column(DateTime, nullable=True)
    merchant_name = Column(String, nullable=True)
    total_amount = Column(Float, nullable=True)
    file_path = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)