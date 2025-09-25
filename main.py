# main.py
import logging
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from interfaces.api.auth import auth_route
from interfaces.api.routes import claim_route, testi_route, user_route, insurance_form_route, slip_route, aju_banding_route, dokumen_invoice_route
from infrastructure.db.connection import Base, engine, database
# from domain import models  # Pastikan ada __init__.py di domain/models
from infrastructure.db.repositories.chat_repository import ChatRepository
from application.usecases.chatbot_services import ChatbotService
from application.adapter.ai_dummy import AIDummyAdapter
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware


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

logger = logging.getLogger("uvicorn.error")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ganti dengan domain spesifik kalau mau lebih aman
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_exceptions(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        logger.exception(f"Unhandled error: {e}")  # akan print stacktrace + file lokasi error
        return JSONResponse(
            status_code=500,
            content={"detail": f"Internal Server Error: {str(e)}"},
        )

# Register routes
app.include_router(auth_route.router, prefix="/auth", tags=["Auth"])
app.include_router(user_route.router, prefix="/users", tags=["Users"])
app.include_router(claim_route.router, prefix="/claim", tags=["Claims"])
app.include_router(claim_route.tracker_router, prefix="/claim", tags=["Claims Tracker"])
app.include_router(testi_route.router, prefix="/testi", tags=["Testi"])
app.include_router(insurance_form_route.router, prefix="/insuranceform", tags=["Insurance Form"])
app.include_router(slip_route.router, prefix="/slip", tags=["Slip"])
app.include_router(aju_banding_route.router, prefix="/ajubanding", tags=["Aju Banding"])
app.include_router(dokumen_invoice_route.router, prefix="/dokumeninvoice", tags=["Dokumen Invoice"])

@app.get("/")
async def root():
    return {"message": "🚀 API is running!", "docs": "http://127.0.0.1:8000/docs"}
