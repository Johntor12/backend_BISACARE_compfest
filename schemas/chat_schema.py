from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime

class MessageIn(BaseModel):
    session_id: Optional[int] = None  # jika null -> buat session baru
    content: str

class MessageOut(BaseModel):
    id: int
    session_id: int
    role: str
    content: str
    created_at: datetime
    meta: Optional[dict]

    model_config = {"from_attributes": True}

class SessionCreate(BaseModel):
    user_id: int
    title: Optional[str] = None

class SessionOut(BaseModel):
    id: int
    user_id: int
    title: Optional[str]
    created_at: datetime
    last_active_at: datetime
    chat_metadata: Optional[dict]

    model_config = {"from_attributes": True}
