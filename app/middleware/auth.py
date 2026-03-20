from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.sql import func
from app.db.session import get_db
from app.models.api_key import APIKey
from app.services.keys import hash_api_key

security = HTTPBearer()

async def validate_api_key(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> APIKey:
    raw_key = credentials.credentials
    hashed = hash_api_key(raw_key)

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

    await db.execute(
        update(APIKey)
        .where(APIKey.id == api_key.id)
        .values(last_used_at=func.now())
    )
    await db.commit()

    return api_key