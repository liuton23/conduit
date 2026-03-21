import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.db.session import engine, Base
import app.models.request_log
import app.models.api_key
from app.routes.proxy import router as proxy_router
from app.routes.keys import router as keys_router
from app.routes.dashboard import router as dashboard_router

logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="Conduit",
    description="AI Gateway & Observability Platform",
    version="0.1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(proxy_router)
app.include_router(keys_router)
app.include_router(dashboard_router)

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "version": "0.1.0"
    }