from typing import AsyncIterator, List
from application.ports.ai_adapter import AIAdapter
from infrastructure.db.repositories.chat_repository import ChatRepository
from datetime import datetime
from fastapi import HTTPException

class ChatbotService:
    """
    Tugas:
    - buat session bila perlu
    - simpan pesan user
    - minta AIAdapter untuk jawab (stream or final)
    - simpan jawaban assistant
    """
    def __init__(self, repo: ChatRepository, ai_adapter: AIAdapter):
        self.repo = repo
        self.ai = ai_adapter

    async def start_session(self, user_id: int, title: str | None = None, chat_metadata: dict | None = None):
        s = await self.repo.create_session(user_id=user_id, title=title, chat_metadata=chat_metadata)
        return s

    async def handle_message_and_respond(self, session_id: int, user_id: int, content: str) -> dict:
        # 1) validate session
        session = await self.repo.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session tidak ditemukan")

        # 2) append user message
        user_msg = await self.repo.append_message(session_id, "user", content)

        # 3) update last active
        await self.repo.update_session_last_active(session_id)

        # 4) prepare context (all messages or summarised)
        messages = await self.repo.list_messages(session_id, limit=200)

        # convert to array of dict for AI adapter
        messages_for_ai = [{"role": m.role, "content": m.content} for m in messages]

        # 5) call AI adapter (synchronous final)
        result = await self.ai.generate(messages_for_ai)

        # result expected to be { "content": "...", "meta": {...}, "external_id": "id" }
        assistant_msg = await self.repo.append_message(session_id, "assistant", result.get("content",""), meta=result.get("meta"), external_id=result.get("external_id"))
        await self.repo.update_session_last_active(session_id)
        return {
            "user_message": user_msg,
            "assistant_message": assistant_msg,
            "ai_result_meta": result.get("meta")
        }

    async def handle_message_and_stream(self, session_id: int, user_id: int, content: str) -> AsyncIterator[dict]:
        """
        Use for websocket streaming: yields partial dicts from adapter.stream()
        Each yielded item can be {"delta": "..."} or {"finish": True, "final": {...}}
        """
        session = await self.repo.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        user_msg = await self.repo.append_message(session_id, "user", content)
        await self.repo.update_session_last_active(session_id)

        messages = await self.repo.list_messages(session_id, limit=200)
        messages_for_ai = [{"role": m.role, "content": m.content} for m in messages]

        stream = self.ai.stream(messages_for_ai)
        full = []
        external_id = None
        async for chunk in stream:   # each chunk a dict like {"delta":"...", "meta":{...}} or {"finish":True, ...}
            # yield chunk to websocket caller
            yield chunk
            if "delta" in chunk:
                full.append(chunk["delta"])
            if "external_id" in chunk:
                external_id = chunk["external_id"]

        final_text = "".join(full).strip()
        # save assistant final message
        assistant_msg = await self.repo.append_message(session_id, "assistant", final_text, meta={"streamed": True}, external_id=external_id)
        await self.repo.update_session_last_active(session_id)
        yield {"finish": True, "assistant_message": {
            "id": assistant_msg.id,
            "content": assistant_msg.content
        }}
