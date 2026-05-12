from pydantic import BaseModel
from typing import Optional


class DocumentResponse(BaseModel):
    id: int
    ca_id: int
    client_id: int
    file_name: str
    doc_type: str
    extracted_text: Optional[str] = None

    class Config:
        from_attributes = True