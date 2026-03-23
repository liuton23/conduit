import json
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.sql import func
from app.db.session import get_db
from app.models.api_key import APIKey
from app.services.keys import hash_api_key
from app.middleware.rate_limit import redis_client
from app.constants import API_KEY_CACHE_TTL

security = HTTPBearer()

def serialize_api_key(api_key: APIKey) -> str:
    return json.dumps({
        "id": api_key.id,
        "name": api_key.name,
        "project": api_key.project,
        "is_active": api_key.is_active,
        "spend_limit_usd": api_key.spend_limit_usd,
        "spend_limit_action": api_key.spend_limit_action,
        "webhook_url": api_key.webhook_url,
        "rate_limit_requests": api_key.rate_limit_requests,
        "rate_limit_window": api_key.rate_limit_window,
    })

def deserialize_api_key(data: str) -> APIKey:
    d = json.loads(data)
    key = APIKey()
    key.id = d["id"]
    key.name = d["name"]
    key.project = d["project"]
    key.is_active = d["is_active"]
    key.spend_limit_usd = d["spend_limit_usd"]
    key.spend_limit_action = d["spend_limit_action"]
    key.webhook_url = d["webhook_url"]
    key.rate_limit_requests = d["rate_limit_requests"]
    key.rate_limit_window = d["rate_limit_window"]
    return key

async def validate_api_key(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> APIKey:
    raw_key = credentials.credentials
    hashed = hash_api_key(raw_key)
    cache_key = f"api_key_cache:{hashed}"

    # check Redis cache first
    cached = await redis_client.get(cache_key)
    if cached:
        return deserialize_api_key(cached)

    # cache miss — check DB
    result = await db.execute(
        select(APIKey).where(
            APIKey.key_hash == hashed,
            APIKey.is_active == True
        )
    )
    api_key = result.scalar_one_or_none()

    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="Invalid or revoked API key"
        )

    # update last_used_at
    await db.execute(
        update(APIKey)
        .where(APIKey.id == api_key.id)
        .values(last_used_at=func.now())
    )
    await db.commit()

    # cache the key
    await redis_client.set(cache_key, serialize_api_key(api_key), ex=API_KEY_CACHE_TTL)

    return api_key