from fastapi import HTTPException, Request
from app.middleware.rate_limit import redis_client

async def validate_session(request: Request) -> str:
    session_token = request.cookies.get("conduit_session")
    if not session_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    user_id = await redis_client.get(f"session:{session_token}")
    if not user_id:
        raise HTTPException(status_code=401, detail="Session expired")

    return user_id