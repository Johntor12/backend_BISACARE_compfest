from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SlipCreate(BaseModel):
    slip_digital_url: Optional[str] = None
    aju_banding_url: Optional[str] = None
    slip_internal_url: Optional[str] = None
    slip_asuransi_url: Optional[str] = None

class SlipUpdate(BaseModel):
    slip_digital_url: Optional[str]
    aju_banding_url: Optional[str]
    slip_internal_url: Optional[str]
    slip_asuransi_url: Optional[str]

class SlipResponse(BaseModel):
    slip_id: int
    slip_digital_url: Optional[str]
    aju_banding_url: Optional[str]
    slip_internal_url: Optional[str]
    slip_asuransi_url: Optional[str]
    created_at: datetime
    user_id: int

    class Config:
        orm_mode = True
