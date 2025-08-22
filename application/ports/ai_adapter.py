from typing import AsyncIterator, Dict, Any

class AIAdapter:
    """
    Interface. Implement this with concrete class that calls OpenAI/Anthropic/etc.
    Methods:
      - generate(session_messages) -> Dict[str, Any] : returns final assistant message dict
      - stream(session_messages) -> AsyncIterator[Dict[str, Any]] : yields partial chunks { "delta": "...", "finish": bool, ...}
    """
    async def generate(self, messages: list) -> Dict[str, Any]:
        raise NotImplementedError()

    async def stream(self, messages: list) -> AsyncIterator[Dict[str, Any]]:
        raise NotImplementedError()
