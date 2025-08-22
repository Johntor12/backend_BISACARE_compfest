from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.db.connection import Base

class ClaimDocumentModel(Base):
    __tablename__ = "claim_documents"

    id = Column(Integer, primary_key=True, index=True)
    claim_id = Column(Integer, ForeignKey("claims.id"), nullable=False)
    document_name = Column(String, nullable=False)
    document_url = Column(String, nullable=False)
    uploaded_at = Column(DateTime, nullable=False)

    claim = relationship("ClaimModel", back_populates="documents")