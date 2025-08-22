from dataclasses import dataclass
from typing import Optional, Literal
from datetime import datetime
from pydantic import BaseModel

class InsuranceForm(BaseModel):
    ktp_url: Optional[str]
    insurance_card_url: Optional[str]
    policy_number: str
    service_type: Literal["rawat_jalan", "rawat_inap", "igd", "lainnya"]
    other_service: Optional[str] = None
    phone_number: str
    complaint: Optional[str]
    created_at: datetime = datetime.now()