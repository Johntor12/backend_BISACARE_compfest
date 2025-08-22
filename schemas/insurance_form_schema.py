from typing import Optional, Literal
from domain.entities.insurance_form import InsuranceForm
from pydantic import BaseModel
from datetime import datetime

class InsuranceFormRequest(BaseModel):
    ktp_url: Optional[str]
    insurance_card_url: Optional[str]
    policy_number: str
    service_type: Literal["rawat_jalan", "rawat_inap", "igd", "lainnya"]
    other_service: Optional[str] = None
    phone_number: str
    complaint: Optional[str] = None


class InsuranceFormResponse(BaseModel):
    form_id: Optional[int]  # Accept None temporarily
    ktp_url: str
    insurance_card_url: str
    policy_number: str
    service_type: str
    other_service: str | None
    phone_number: str
    complaint: str
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True