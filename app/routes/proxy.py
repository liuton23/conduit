from fastapi import APIRouter, Depends, Header
from fastapi.security import HTTPBearer
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db, AsyncSessionLocal
from app.services.proxy import forward_request, forward_streaming_request
from app.services.cost import calculate_cost
from app.models.request_log import RequestLog
from app.models.api_key import APIKey
from app.models.enums import get_provider_from_model
from app.models.schemas import ProxyRequest
from app.middleware.auth import validate_api_key, security
from app.middleware.rate_limit import check_rate_limit
from typing import Optional

router = APIRouter(dependencies=[Depends(security)])

@router.post("/v1/messages")
async def proxy_messages(
    request: ProxyRequest,
    db: AsyncSession = Depends(get_db),
    api_key: APIKey = Depends(validate_api_key),
    x_project: Optional[str] = Header(None)
):
    await check_rate_limit(api_key.id)

    payload = request.model_dump(exclude_none=True)
    payload["model"] = request.model.value
    model = request.model.value
    provider = get_provider_from_model(model)
    project = x_project or api_key.project

    # handle streaming
    if payload.get("stream"):
        async def on_complete(input_tokens: int, output_tokens: int, latency_ms: float):
            total_tokens = input_tokens + output_tokens
            cost = calculate_cost(model, input_tokens, output_tokens)

            async with AsyncSessionLocal() as session:
                log = RequestLog(
                    api_key=api_key.id,
                    model=model,
                    provider=provider.value,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    total_tokens=total_tokens,
                    cost_usd=cost,
                    latency_ms=latency_ms,
                    status_code=200,
                    project=project
                )
                session.add(log)
                await session.commit()

        async def stream_generator():
            async for chunk in forward_streaming_request(model, payload, on_complete):
                yield chunk

        return StreamingResponse(
            stream_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no",
            }
        )

    # non-streaming
    response_data, status_code, latency_ms = await forward_request(model, payload)

    usage = response_data.get("usage", {})
    input_tokens = usage.get("input_tokens", 0)
    output_tokens = usage.get("output_tokens", 0)
    total_tokens = input_tokens + output_tokens
    cost = calculate_cost(model, input_tokens, output_tokens)

    log = RequestLog(
        api_key=api_key.id,
        model=model,
        provider=provider.value,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=total_tokens,
        cost_usd=cost,
        latency_ms=latency_ms,
        status_code=status_code,
        project=project
    )
    db.add(log)
    await db.commit()

    return response_data