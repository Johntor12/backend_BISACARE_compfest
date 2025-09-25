from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, func
from sqlalchemy.orm import relationship
from infrastructure.db.connection import Base

class AjuBandingModel(Base):
    __tablename__ = "aju_bandings"

    aju_banding_id = Column(Integer, primary_key=True, autoincrement=True)
    aju_banding_url = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("UserModel", back_populates="aju_bandings")