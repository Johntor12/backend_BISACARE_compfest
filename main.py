# main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from interfaces.api.auth import auth_route
from interfaces.api.routes import user, claim, testi
from infrastructure.db.connection import Base, engine, database
# from domain import models  # Pastikan ada __init__.py di domain/models

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
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(claim.router, prefix="/claim", tags=["Claims"])
app.include_router(testi.router, prefix="/testi", tags=["Testi"])

@app.get("/")
async def root():
    return {"message": "🚀 API is running!", "docs": "http://127.0.0.1:8000/docs"}
