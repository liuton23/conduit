import redis.asyncio as aioredis
from fastapi import HTTPException
from app.config import settings
from app.constants import DEFAULT_RATE_LIMIT_REQUESTS, DEFAULT_RATE_LIMIT_WINDOW

redis_client = aioredis.from_url(settings.REDIS_URL, decode_responses=True)

RATE_LIMIT_REQUESTS = DEFAULT_RATE_LIMIT_REQUESTS
RATE_LIMIT_WINDOW = DEFAULT_RATE_LIMIT_WINDOW

async def check_rate_limit(api_key_id: str):
    redis_key = f"rate_limit:{api_key_id}"

    current = await redis_client.get(redis_key)

    if current is None:
        # first request — set counter with expiry
        await redis_client.set(redis_key, 1, ex=RATE_LIMIT_WINDOW)
        return

    if int(current) >= RATE_LIMIT_REQUESTS:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Max {RATE_LIMIT_REQUESTS} requests per {RATE_LIMIT_WINDOW} seconds."
        )

    await redis_client.incr(redis_key)