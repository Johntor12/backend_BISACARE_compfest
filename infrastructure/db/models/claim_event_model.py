from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.db.connection import Base

class ClaimEventModel(Base):
    __tablename__ = "claim_events"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    claim_id = Column(Integer, ForeignKey("claims.id"))
    event_type = Column(String, nullable=False)
    event_description = Column(String, nullable=False)
    event_date = Column(DateTime, nullable=False)

    claim = relationship("ClaimModel", back_populates="events")
