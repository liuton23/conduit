from fastapi import APIRouter, HTTPException, Response, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel, EmailStr
from app.db.session import get_db
from app.models.user import User
from app.middleware.rate_limit import redis_client
import secrets

router = APIRouter(prefix="/auth", tags=["Auth"])

SESSION_TTL = 86400  # 24 hours

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

async def create_session(response: Response, user_id: str) -> str:
    session_token = secrets.token_urlsafe(32)
    await redis_client.set(f"session:{session_token}", user_id, ex=SESSION_TTL)
    response.set_cookie(
        key="conduit_session",
        value=session_token,
        httponly=True,
        max_age=SESSION_TTL,
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
    request: RegisterRequest,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    # check if already registered
    result = await db.execute(select(func.count(User.id)))
    count = result.scalar()
    if count > 0:
        raise HTTPException(status_code=400, detail="Already registered")

    # validate password
    errors = User.validate_password(request.password)
    if errors:
        raise HTTPException(status_code=400, detail=errors)

    # check email not taken
    existing = await db.execute(select(User).where(User.email == request.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=request.email,
        password_hash=User.hash_password(request.password)
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    await create_session(response, user.id)
    return {"message": "Registered successfully"}

@router.post("/login")
async def login(
    request: LoginRequest,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.email == request.email))
    user = result.scalar_one_or_none()

    if not user or not User.verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    await create_session(response, user.id)
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

    user_id = await redis_client.get(f"session:{session_token}")
    if not user_id:
        raise HTTPException(status_code=401, detail="Session expired")

    return {"valid": True}