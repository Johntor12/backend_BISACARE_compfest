from typing import List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from infrastructure.db.models.chat_model import ChatSessionModel, ChatMessageModel
from datetime import datetime

class ChatRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_session(self, user_id: int, title: Optional[str]=None, metadata: Optional[dict]=None) -> ChatSessionModel:
        s = ChatSessionModel(user_id=user_id, title=title, metadata=metadata or {})
        self.session.add(s)
        await self.session.flush()
        await self.session.refresh(s)
        return s

    async def get_session(self, session_id: int) -> Optional[ChatSessionModel]:
        res = await self.session.execute(select(ChatSessionModel).where(ChatSessionModel.id==session_id))
        return res.scalars().first()
    

    async def update_session_last_active(self, session_id: int):
        session = await self.get_session(session_id)
        if session:
            session.last_active_at = datetime.utcnow()
            await self.session.commit()
            await self.session.refresh(session)
        return session

    # Messages
    async def append_message(self, session_id: int, role: str, content: str, meta: Optional[dict]=None, external_id: Optional[str]=None):
        msg = ChatMessageModel(session_id=session_id, role=role, content=content, meta=meta or {}, external_id=external_id)
        self.session.add(msg)
        await self.session.flush()
        await self.session.refresh(msg)
        return msg

    async def list_messages(self, session_id: int, limit: int=200, offset: int=0) -> List[ChatMessageModel]:
        stmt = select(ChatMessageModel).where(ChatMessageModel.session_id==session_id).order_by(ChatMessageModel.created_at.asc()).limit(limit).offset(offset)
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def delete_session(self, session_id: int):
        s = await self.get_session(session_id)
        if s:
            await self.session.delete(s)
            await self.session.commit()
            return True
        return False
