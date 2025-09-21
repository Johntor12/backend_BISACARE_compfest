from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, func
from sqlalchemy.orm import relationship
from infrastructure.db.connection import Base

class SlipModel(Base):
    __tablename__ = "slips"

    slip_id = Column(Integer, primary_key=True, autoincrement=True)
    slip_digital_url = Column(String, nullable=True)
    aju_banding_url = Column(String, nullable=True)
    slip_internal_url = Column(String, nullable=True)
    slip_asuransi_url = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("UserModel", back_populates="slips")