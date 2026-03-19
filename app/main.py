from fastapi import FastAPI
from app.config import settings
from app.db.session import engine, Base
import app.models.request_log  # this registers the model with Base

app = FastAPI(
    title="Conduit",
    description="AI Gateway & Observability Platform",
    version="0.1.0"
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "version": "0.1.0"
    }