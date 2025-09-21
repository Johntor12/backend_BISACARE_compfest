from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Slip(BaseModel):
    slip_id: int
    slip_digital_url: Optional[str] | None = None
    aju_banding_url: Optional[str] | None = None
    slip_internal_url: Optional[str] | None = None
    slip_pihak_asuransi: Optional[str] | None = None

    created_at: datetime = datetime.now()

    user_id: int