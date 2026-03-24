from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.api_key import APIKey
from app.services.keys import generate_api_key
from app.middleware.api_key import validate_api_key
from app.middleware.session import validate_session
from app.models.enums import SpendLimitAction
from pydantic import BaseModel
from typing import Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/keys", tags=["API Keys"])

class CreateKeyRequest(BaseModel):
    name: str
    project: str  # required
    spend_limit_usd: Optional[float] = None
    spend_limit_action: Optional[SpendLimitAction] = SpendLimitAction.WARN
    webhook_url: Optional[str] = None
    rate_limit_requests: Optional[int] = None
    rate_limit_window: Optional[int] = None

class UpdateKeyRequest(BaseModel):
    project: Optional[str] = None
    spend_limit_usd: Optional[float] = None
    spend_limit_action: Optional[SpendLimitAction] = None
    webhook_url: Optional[str] = None
    rate_limit_requests: Optional[int] = None
    rate_limit_window: Optional[int] = None

class CreateKeyResponse(BaseModel):
    id: str
    name: str
    project: str
    key: str
    message: str

@router.post("")
async def create_api_key(
    request: CreateKeyRequest,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(validate_session)
):
    raw_key, hashed = generate_api_key()

    api_key = APIKey(
        user_id=user_id,
        name=request.name,
        project=request.project,
        key_hash=hashed,
        spend_limit_usd=request.spend_limit_usd,
        spend_limit_action=request.spend_limit_action.value if request.spend_limit_action else SpendLimitAction.WARN.value,
        webhook_url=request.webhook_url,
        rate_limit_requests=request.rate_limit_requests,
        rate_limit_window=request.rate_limit_window
    )

    db.add(api_key)
    await db.commit()
    await db.refresh(api_key)

    return CreateKeyResponse(
        id=api_key.id,
        name=api_key.name,
        project=api_key.project,
        key=raw_key,
        message="Store this key safely — it won't be shown again."
    )

@router.get("")
async def list_api_keys(
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(validate_session)
):
    result = await db.execute(
        select(APIKey).where(
            APIKey.is_active == True,
            APIKey.user_id == user_id
        )
    )
    keys = result.scalars().all()
    return [
        {
            "id": k.id,
            "name": k.name,
            "project": k.project,
            "is_active": k.is_active,
            "created_at": k.created_at,
            "last_used_at": k.last_used_at,
            "spend_limit_usd": k.spend_limit_usd,
            "spend_limit_action": k.spend_limit_action,
            "webhook_url": k.webhook_url,
            "rate_limit_requests": k.rate_limit_requests,
            "rate_limit_window": k.rate_limit_window,
        }
        for k in keys
    ]

@router.patch("/{key_id}")
async def update_api_key(
    key_id: str,
    request: UpdateKeyRequest,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(validate_session)
):
    result = await db.execute(
        select(APIKey).where(APIKey.id == key_id, APIKey.user_id == user_id)
    )
    key = result.scalar_one_or_none()

    if not key:
        raise HTTPException(status_code=404, detail="Key not found")

    if request.project is not None:
        key.project = request.project
    if request.spend_limit_usd is not None:
        key.spend_limit_usd = request.spend_limit_usd
    if request.spend_limit_action is not None:
        key.spend_limit_action = request.spend_limit_action.value
    if request.webhook_url is not None:
        key.webhook_url = request.webhook_url
    if request.rate_limit_requests is not None:
        key.rate_limit_requests = request.rate_limit_requests
    if request.rate_limit_window is not None:
        key.rate_limit_window = request.rate_limit_window

    await db.commit()
    return {"message": "Key updated successfully"}

@router.delete("/{key_id}")
async def revoke_api_key(
    key_id: str,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(validate_session)
):
    result = await db.execute(
        select(APIKey).where(APIKey.id == key_id, APIKey.user_id == user_id)
    )
    key = result.scalar_one_or_none()

    if not key:
        raise HTTPException(status_code=404, detail="Key not found")

    key.is_active = False
    await db.commit()

    from app.middleware.rate_limit import redis_client
    cache_key = f"api_key_cache:{key.key_hash}"
    await redis_client.delete(cache_key)

    return {"message": f"Key {key_id} revoked successfully"}

@router.get("/verify")
async def verify_api_key(api_key: APIKey = Depends(validate_api_key)):
    return {
        "valid": True,
        "name": api_key.name,
        "project": api_key.project
    }