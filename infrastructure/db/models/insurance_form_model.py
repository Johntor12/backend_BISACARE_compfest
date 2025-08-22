from sqlalchemy import Column, Integer, String, Text, DateTime, func
from infrastructure.db.connection import Base

class InsuranceFormModel(Base):
    __tablename__ = "insurance_forms"

    form_id = Column(Integer, primary_key=True, index=True)
    ktp_url = Column(String, nullable=True)
    insurance_card_url = Column(String, nullable=True)
    policy_number = Column(String, nullable=False)
    service_type = Column(String, nullable=False)
    other_service = Column(String, nullable=True)
    phone_number = Column(String, nullable=False)
    insurance_form = Column(String, nullable=True)
    complaint = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
