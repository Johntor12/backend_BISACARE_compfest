from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class ChatMessage:
    id: Optional[int]
    session_id: int
    role: str                # "user" | "assistant" | "system"
    content: str
    created_at: Optional[datetime] = None
    meta: Optional[dict] = None

@dataclass
class ChatSession:
    id: Optional[int]
    user_id: int
    title: Optional[str] = None
    created_at: Optional[datetime] = None
    last_active_at: Optional[datetime] = None
    chat_metadata: Optional[dict] = None
