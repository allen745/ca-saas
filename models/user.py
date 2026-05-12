from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

class CA(Base):
    __tablename__ = "cas"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    firm_name = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())