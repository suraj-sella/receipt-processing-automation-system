from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.utils.database import Base
from datetime import datetime

class ReceiptFile(Base):
    __tablename__ = "receipt_file"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    is_valid = Column(Boolean, default=False)
    invalid_reason = Column(String, nullable=True)
    is_processed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)