from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from typing import Optional

class AjuBandingRequest(BaseModel):
    aju_banding_url: str

class AjuBandingResponse(BaseModel):
    id: int
    aju_banding_url: str
    user_id: int
    created_at: datetime