from pydantic import BaseModel
from typing import Optional

class NoticeCreate(BaseModel):
    client_id: int
    notice_type: str
    notice_date: str
    deadline: str
    description: Optional[str] = None

class NoticeUpdate(BaseModel):
    notice_type: Optional[str] = None
    notice_date: Optional[str] = None
    deadline: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class NoticeResponse(BaseModel):
    id: int
    ca_id: int
    client_id: int
    notice_type: str
    notice_date: str
    deadline: str
    description: Optional[str] = None
    status: str

    class Config:
        from_attributes = True