from pydantic import BaseModel
from datetime import datetime

class ClaimBase(BaseModel):
    user_id: int
    status: str

class ClaimCreate(ClaimBase):
    pass

class ClaimResponse(ClaimBase):
    id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True