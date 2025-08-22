from pydantic import BaseModel
from datetime import datetime

class ClaimDocumentBase(BaseModel):
    claim_id: int
    document_name: str
    document_url: str
    uploaded_at: datetime

class ClaimDocumentCreate(ClaimDocumentBase):
    pass

class ClaimDocumentResponse(ClaimDocumentBase):
    id: int
    class Config:
        orm_mode = True