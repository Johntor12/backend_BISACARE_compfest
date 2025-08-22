from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship, mapped_column
from infrastructure.db.connection import Base

class ChatSessionModel(Base):
    __tablename__ = "chat_sessions"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(Integer, nullable=False, index=True)
    title = mapped_column(String, nullable=True)
    created_at = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    last_active_at = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    chat_metadata = mapped_column(JSON, nullable=True)  # store model name, purpose, ttl, etc

    messages = relationship("ChatMessageModel", back_populates="session", cascade="all, delete-orphan")

class ChatMessageModel(Base):
    __tablename__ = "chat_messages"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id = mapped_column(Integer, ForeignKey("chat_sessions.id", ondelete="CASCADE"), index=True, nullable=False)
    role = mapped_column(String, nullable=False)   # user|assistant|system
    content = mapped_column(Text, nullable=False)
    created_at = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    meta = mapped_column(JSON, nullable=True)     # e.g. {"model":"gpt-4","tokens":123,"score":0.9}
    external_id = mapped_column(String, nullable=True)  # id from AI provider (if any)

    session = relationship("ChatSessionModel", back_populates="messages")
