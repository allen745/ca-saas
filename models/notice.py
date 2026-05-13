from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from database import Base

class Notice(Base):
    __tablename__ = "notices"

    id = Column(Integer, primary_key=True, index=True)
    ca_id = Column(Integer, ForeignKey("cas.id"), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    notice_type = Column(String, nullable=False)
    notice_date = Column(String, nullable=False)
    deadline = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String, default="Received")
    created_at = Column(DateTime(timezone=True), server_default=func.now())