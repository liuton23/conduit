from fastapi import APIRouter, HTTPException, Response, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel
from app.db.session import get_db
from app.models.user import User
from app.middleware.rate_limit import redis_client
from app.constants import USER_SESSION_TTL
import secrets

router = APIRouter(prefix="/auth", tags=["Auth"])

class AccessKeyRequest(BaseModel):
    access_key: str

async def create_session(response: Response) -> str:
    session_token = secrets.token_urlsafe(32)
    await redis_client.set(f"session:{session_token}", "valid", ex=USER_SESSION_TTL)
    response.set_cookie(
        key="conduit_session",
        value=session_token,
        httponly=True,
        max_age=USER_SESSION_TTL,
        samesite="lax"
    )
    return session_token

@router.get("/status")
async def auth_status(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(func.count(User.id)))
    count = result.scalar()
    return {"registered": count > 0}

@router.post("/register")
async def register(
    request: AccessKeyRequest,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    # check if already registered
    result = await db.execute(select(func.count(User.id)))
    count = result.scalar()
    if count > 0:
        raise HTTPException(status_code=400, detail="Already registered")

    if len(request.access_key) < 8:
        raise HTTPException(status_code=400, detail="Access key must be at least 8 characters")

    user = User(access_key_hash=User.hash_access_key(request.access_key))
    db.add(user)
    await db.commit()

    await create_session(response)
    return {"message": "Registered successfully"}

@router.post("/login")
async def login(
    request: AccessKeyRequest,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    hashed = User.hash_access_key(request.access_key)
    result = await db.execute(
        select(User).where(User.access_key_hash == hashed)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid access key")

    await create_session(response)
    return {"message": "Login successful"}

@router.post("/logout")
async def logout(request: Request, response: Response):
    session_token = request.cookies.get("conduit_session")
    if session_token:
        await redis_client.delete(f"session:{session_token}")
    response.delete_cookie("conduit_session")
    return {"message": "Logged out"}

@router.get("/verify")
async def verify_session(request: Request):
    session_token = request.cookies.get("conduit_session")
    if not session_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    valid = await redis_client.get(f"session:{session_token}")
    if not valid:
        raise HTTPException(status_code=401, detail="Session expired")

    return {"valid": True}