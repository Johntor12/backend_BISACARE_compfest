from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, func
from infrastructure.db.connection import Base
import enum

class RekeningTypeEnum(str, enum.Enum):
    BCA = "BCA",
    MANDIRI = "MANDIRI",
    BNI = "BNI",
    BRI = "BRI",
    CIMB_NIAGA = "CIMB NIAGA",
    PERMATA_BANK = "PERMATA BANK",
    BANK_DANAMON = "BANK DANAMON"

class InsuranceFormModel(Base):
    __tablename__ = "insurance_forms"

    form_id = Column(Integer, primary_key=True, index=True)
    ktp_url = Column(String, nullable=True)
    insurance_card_url = Column(String, nullable=True)
    policy_number = Column(String, nullable=False)
    rekening_type = Column(Enum(RekeningTypeEnum), default=RekeningTypeEnum.BCA, nullable=True)
    rekening_number = Column(String, nullable=True)
    service_type = Column(String, nullable=False)
    other_service = Column(String, nullable=True, default=None)
    phone_number = Column(String, nullable=False)
    complaint = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
