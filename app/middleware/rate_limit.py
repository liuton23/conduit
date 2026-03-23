import redis.asyncio as aioredis
from fastapi import HTTPException
from app.config import settings
from app.constants import DEFAULT_RATE_LIMIT_REQUESTS, DEFAULT_RATE_LIMIT_WINDOW
from app.models.api_key import APIKey

redis_client = aioredis.from_url(settings.REDIS_URL, decode_responses=True)

async def check_rate_limit(api_key: APIKey):
    # use per-key limits if set, otherwise fall back to defaults
    limit = api_key.rate_limit_requests or DEFAULT_RATE_LIMIT_REQUESTS
    window = api_key.rate_limit_window or DEFAULT_RATE_LIMIT_WINDOW

    redis_key = f"rate_limit:{api_key.id}"
    current = await redis_client.get(redis_key)

    if current is None:
        await redis_client.set(redis_key, 1, ex=window)
        return

    if int(current) >= limit:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Max {limit} requests per {window} seconds."
        )

    await redis_client.incr(redis_key)