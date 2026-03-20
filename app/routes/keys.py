from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.api_key import APIKey
from app.services.keys import generate_api_key
from app.middleware.auth import validate_api_key
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/keys", tags=["API Keys"])

class CreateKeyRequest(BaseModel):
    name: str
    project: Optional[str] = None

class CreateKeyResponse(BaseModel):
    id: str
    name: str
    project: Optional[str]
    key: str
    message: str

@router.post("", response_model=CreateKeyResponse)
async def create_api_key(
    request: CreateKeyRequest,
    db: AsyncSession = Depends(get_db)
):
    raw_key, hashed = generate_api_key()

    api_key = APIKey(
        name=request.name,
        project=request.project,
        key_hash=hashed
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
async def list_api_keys(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(APIKey).where(APIKey.is_active == True))
    keys = result.scalars().all()
    return [
        {
            "id": k.id,
            "name": k.name,
            "project": k.project,
            "is_active": k.is_active,
            "created_at": k.created_at,
            "last_used_at": k.last_used_at
        }
        for k in keys
    ]

@router.get("/verify", tags=["API Keys"])
async def verify_api_key(api_key: APIKey = Depends(validate_api_key)):
    return {
        "valid": True,
        "name": api_key.name,
        "project": api_key.project
    }

@router.delete("/{key_id}")
async def revoke_api_key(key_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(APIKey).where(APIKey.id == key_id))
    key = result.scalar_one_or_none()

    if not key:
        raise HTTPException(status_code=404, detail="Key not found")

    key.is_active = False
    await db.commit()

    return {"message": f"Key {key_id} revoked successfully"}