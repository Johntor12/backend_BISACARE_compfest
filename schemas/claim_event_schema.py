from pydantic import BaseModel
from datetime import datetime

class ClaimEventBase(BaseModel):
    claim_id: int
    event_type: str
    event_description: str
    event_date: datetime

class ClaimEventCreate(ClaimEventBase):
    pass

class ClaimEventResponse(ClaimEventBase):
    id: int
    class Config:
        orm_mode = True