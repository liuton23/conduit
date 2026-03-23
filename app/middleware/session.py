from fastapi import HTTPException, Request
from app.middleware.rate_limit import redis_client

async def validate_session(request: Request):
    session_token = request.cookies.get("conduit_session")
    if not session_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    valid = await redis_client.get(f"session:{session_token}")
    if not valid:
        raise HTTPException(status_code=401, detail="Session expired")

    return session_token