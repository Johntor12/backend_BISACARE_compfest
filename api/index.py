# Vercel serverless entrypoint for FastAPI
from fastapi import FastAPI
from main import app as fastapi_app

# Vercel looks for the variable named 'app'
app: FastAPI = fastapi_app

# Optional root override for health (keeps existing root in main.py)
@fastapi_app.get("/healthz")
async def health():
    return {"status": "ok"}
