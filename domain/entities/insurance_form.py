from dataclasses import dataclass
from typing import Optional, Literal
from datetime import datetime
from pydantic import BaseModel

class InsuranceForm(BaseModel):
    form_id: Optional[int]
    ktp_url: Optional[str] = None
    insurance_card_url: Optional[str] = None
    policy_number: str
    rekening_type: Literal["BCA", "MANDIRI", "BNI", "BRI", "CIMB NIAGA", "PERMATA BANK", "BANK DANAMON", "BSI"] = "BCA"
    rekening_number: Optional[str] =  "0123456789"    
    service_type: Literal["rawat_jalan", "rawat_inap", "igd", "lainnya"]
    other_service: Optional[str] | None = None
    phone_number: str
    complaint: str
    created_at: datetime = datetime.now()
    user_id: int