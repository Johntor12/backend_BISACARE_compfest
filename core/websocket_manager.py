# core/websocket_manager.py
from typing import Dict, Set
from fastapi import WebSocket

class ConnectionManager:
    """
    Sederhana: simpan WebSocket per conversation_id.
    """
    def __init__(self):
        self.rooms: Dict[int, Set[WebSocket]] = {}

    async def connect(self, conversation_id: int, websocket: WebSocket):
        await websocket.accept()
        self.rooms.setdefault(conversation_id, set()).add(websocket)

    def disconnect(self, conversation_id: int, websocket: WebSocket):
        try:
            self.rooms.get(conversation_id, set()).discard(websocket)
        except KeyError:
            pass

    async def broadcast(self, conversation_id: int, data: dict):
        dead = []
        for ws in self.rooms.get(conversation_id, set()):
            try:
                await ws.send_json(data)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(conversation_id, ws)

manager = ConnectionManager()
