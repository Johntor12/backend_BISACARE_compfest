from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from infrastructure.db.connection import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    # Relasi ke Claim
    claims = relationship("ClaimModel", back_populates="user")
