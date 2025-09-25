from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AjuBanding(BaseModel):
    aju_banding_id: int | None = None
    aju_banding_url: str

    created_at: datetime = datetime.now()
    user_id: int