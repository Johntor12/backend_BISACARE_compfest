from typing import Optional, Literal
from pydantic import BaseModel
from datetime import datetime

class InsuranceFormRequest(BaseModel):
    policy_number: str
    rekening_type: Literal["BCA", "MANDIRI", "BNI", "BRI", "CIMB NIAGA", "PERMATA BANK", "BANK DANAMON", "BSI"] = "BCA"
    rekening_number: Optional[str]    
    service_type: Literal["rawat_jalan", "rawat_inap", "igd", "lainnya"]
    other_service: Optional[str] | None
    phone_number: str
    complaint: str
    created_at: datetime
    user_id: int


class InsuranceFormResponse(BaseModel):
    form_id: Optional[int]  # Accept None temporarily
    user_id: int
    ktp_url: Optional[str]
    insurance_card_url: Optional[str]
    policy_number: str
    rekening_type: Literal["BCA", "MANDIRI", "BNI", "BRI", "CIMB NIAGA", "PERMATA BANK", "BANK DANAMON", "BSI"] = "BCA"
    rekening_number: Optional[str]    
    service_type: Literal["rawat_jalan", "rawat_inap", "igd", "lainnya"]
    other_service: Optional[str] | None
    phone_number: str
    complaint: str
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True