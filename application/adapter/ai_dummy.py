import asyncio
from typing import AsyncIterator, Dict, Any, List
from application.ports.ai_adapter import AIAdapter

class AIDummyAdapter(AIAdapter):
    async def generate(self, messages: List[dict]) -> Dict[str, Any]:
        # simple echo plus timestamp
        text = "Echo (assistant): " + (messages[-1]["content"] if messages else "hi")
        return {"content": text, "meta": {"provider": "dummy"}, "external_id": None}

    async def stream(self, messages: List[dict]) -> AsyncIterator[Dict[str, Any]]:
        # yield small chunks slowly
        text = "Simulated streaming response for: " + (messages[-1]["content"] if messages else "")
        for ch in text.split():
            await asyncio.sleep(0.05)
            yield {"delta": ch + " "}
        yield {"external_id": "dummy-123"}
