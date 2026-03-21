import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timezone
from app.models.enums import SpendLimitAction
from app.models.request_log import RequestLog
from app.models.api_key import APIKey
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

async def get_current_month_spend(db: AsyncSession, api_key_id: str) -> float:
    now = datetime.now(timezone.utc)
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    result = await db.execute(
        select(func.sum(RequestLog.cost_usd))
        .where(
            RequestLog.api_key == api_key_id,
            RequestLog.created_at >= month_start
        )
    )
    total = result.scalar()
    return total or 0.0

async def fire_webhook(url: str, api_key: APIKey, current_spend: float):
    payload = {
        "event": "spend_limit_reached",
        "api_key_id": api_key.id,
        "api_key_name": api_key.name,
        "project": api_key.project,
        "spend_limit_usd": api_key.spend_limit_usd,
        "current_spend_usd": current_spend,
    }
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            await client.post(url, json=payload)
    except Exception:
        pass

async def check_spend_limit(db: AsyncSession, api_key: APIKey):
    if not api_key.spend_limit_usd:
        logger.info(f"No spend limit set for key {api_key.id}")
        return

    current_spend = await get_current_month_spend(db, api_key.id)
    logger.info(f"Key {api_key.id} spend: ${current_spend} / limit: ${api_key.spend_limit_usd} action: {api_key.spend_limit_action}")

    if current_spend >= api_key.spend_limit_usd:
        if api_key.webhook_url:
            await fire_webhook(api_key.webhook_url, api_key, current_spend)

        if api_key.spend_limit_action == SpendLimitAction.BLOCK:
            raise HTTPException(
                status_code=429,
                detail=f"Monthly spend limit of ${api_key.spend_limit_usd} reached. Current spend: ${current_spend:.4f}"
            )