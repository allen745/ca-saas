from pydantic import BaseModel
from typing import Optional

class ClientCreate(BaseModel):
    full_name: str
    pan_number: str
    email: Optional[str] = None
    phone: Optional[str] = None
    entity_type: str
    assessment_year: Optional[str] = None

class ClientUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    entity_type: Optional[str] = None
    assessment_year: Optional[str] = None

class ClientResponse(BaseModel):
    id: int
    ca_id: int
    full_name: str
    pan_number: str
    email: Optional[str] = None
    phone: Optional[str] = None
    entity_type: str
    assessment_year: Optional[str] = None

    class Config:
        from_attributes = True