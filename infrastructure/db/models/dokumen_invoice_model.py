from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, func
from sqlalchemy.orm import relationship
from infrastructure.db.connection import Base

class DokumenInvoiceModel(Base):
    __tablename__ = "dokumen_invoices"

    dokumen_invoice_id = Column(Integer, primary_key=True, autoincrement=True)
    dokumen_invoice_url = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("UserModel", back_populates="dokumen_invoices")