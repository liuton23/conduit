from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.session import engine, Base
import app.models.request_log
from app.routes.proxy import router as proxy_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # shutdown (add cleanup here later if needed)

app = FastAPI(
    title="Conduit",
    description="AI Gateway & Observability Platform",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(proxy_router)

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "version": "0.1.0"
    }