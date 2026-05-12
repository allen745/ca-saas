from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    ca_id = Column(Integer, ForeignKey("cas.id"), nullable=False)
    full_name = Column(String, nullable=False)
    pan_number = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    entity_type = Column(String, nullable=False)
    assessment_year = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())