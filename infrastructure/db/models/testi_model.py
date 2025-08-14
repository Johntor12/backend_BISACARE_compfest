from sqlalchemy import Column, Integer, String
from infrastructure.db.connection import Base  # Pastikan Base sudah ada di base.py

class TestiModel(Base):
    __tablename__ = "testi"

    testi_id = Column(Integer, primary_key=True, index=True)
    source_person = Column(String, nullable=False)
    image_person = Column(String, nullable=False)
    testi = Column(String, nullable=False)
