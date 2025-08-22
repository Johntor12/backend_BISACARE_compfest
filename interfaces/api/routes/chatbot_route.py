from fastapi import APIRouter, Depends, WebSocket, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.db.connection import get_db
from infrastructure.db.repositories.chat_repository import ChatRepository
from application.usecases.chatbot_services import ChatbotService
from application.ports.ai_adapter import AIAdapter  # we will pass implementation at wiring time
from core.websocket_manager import manager
from schemas.chat_schema import MessageIn, MessageOut, SessionCreate, SessionOut

router = APIRouter(prefix="/bot", tags=["Chatbot"])

# --- REST simple endpoint to send message and get final reply ---
@router.post("/sessions", response_model=SessionOut)
async def create_session(payload: SessionCreate, session: AsyncSession = Depends(get_db)):
    repo = ChatRepository(session)
    svc = ChatbotService(repo, ai_adapter_dummy)  # replace ai_adapter_dummy with real adapter
    s = await svc.start_session(payload.user_id, payload.title)
    return s

@router.post("/sessions/{session_id}/message", response_model=dict)
async def post_message(session_id: int, payload: MessageIn, user_id: int = Query(...), session: AsyncSession = Depends(get_db)):
    repo = ChatRepository(session)
    svc = ChatbotService(repo, ai_adapter_dummy)
    out = await svc.handle_message_and_respond(session_id, user_id, payload.content)
    # convert models to pydantic or dict as desired
    return {"assistant": out["assistant_message"].content, "meta": out["ai_result_meta"]}

# --- WebSocket streaming endpoint --- 
# Client connects and sends JSON {"type":"message","content":"...","user_id":123}
# Server streams incremental chunks from AI and final assistant message at end
@router.websocket("/ws/sessions/{session_id}")
async def ws_session(websocket: WebSocket, session_id: int, token: str | None = Query(None)):
    # validate token / user (implement JWT check) -> get user_id
    await manager.connect(session_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            if data.get("type") == "message":
                user_id = data.get("user_id")
                content = data.get("content")
                # spawn streaming generator and forward chunks to client
                repo = ChatRepository(await get_db().__anext__())  # better: use dependency injection in real app
                svc = ChatbotService(repo, ai_adapter_dummy)
                async for chunk in svc.handle_message_and_stream(session_id, user_id, content):
                    # push chunk to the websocket client
                    await websocket.send_json(chunk)
            else:
                await websocket.send_json({"error":"unknown type"})
    except Exception as e:
        manager.disconnect(session_id, websocket)
