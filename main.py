# main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from interfaces.api.auth import auth_route
from interfaces.api.routes import claim_route, testi_route, user_route, insurance_form_route
from infrastructure.db.connection import Base, engine, database
# from domain import models  # Pastikan ada __init__.py di domain/models
from infrastructure.db.repositories.chat_repository import ChatRepository
from application.usecases.chatbot_services import ChatbotService
from application.adapter.ai_dummy import AIDummyAdapter

ai_adapter = AIDummyAdapter()

# in route factory:
repo = ChatRepository(Base)
svc = ChatbotService(repo, ai_adapter)


# Lifespan handler (pengganti @app.on_event)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await database.connect()
    print("✅ Database connected!") 
    yield
    # Shutdown
    await database.disconnect()
    print("🛑 Database disconnected.")


app = FastAPI(lifespan=lifespan)

# Register routes
app.include_router(auth_route.router, prefix="/auth", tags=["Auth"])
app.include_router(user_route.router, prefix="/users", tags=["Users"])
app.include_router(claim_route.router, prefix="/claim", tags=["Claims"])
app.include_router(claim_route.tracker_router, prefix="/claim", tags=["Claims Tracker"])
app.include_router(testi_route.router, prefix="/testi", tags=["Testi"])
app.include_router(insurance_form_route.router, prefix="/insuranceform", tags=["Insurance Form"])

@app.get("/")
async def root():
    return {"message": "🚀 API is running!", "docs": "http://127.0.0.1:8000/docs"}
