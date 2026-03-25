from fastapi import HTTPException
import httpx
import time
import json
from app.config import settings
from app.models.enums import Provider, get_provider_from_model

PROVIDER_URLS = {
    Provider.ANTHROPIC: "https://api.anthropic.com/v1/messages",
    Provider.OPENAI: "https://api.openai.com/v1/chat/completions",
}

def build_headers(provider: Provider) -> dict:
    if provider == Provider.ANTHROPIC:
        if not settings.ANTHROPIC_API_KEY:
            raise HTTPException(status_code=400, detail="ANTHROPIC_API_KEY is not configured")
        return {
            "x-api-key": settings.ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
    elif provider == Provider.OPENAI:
        if not settings.OPENAI_API_KEY:
            raise HTTPException(status_code=400, detail="OPENAI_API_KEY is not configured")
        return {
            "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
            "content-type": "application/json",
        }
    elif provider == Provider.MISTRAL:
        if not settings.MISTRAL_API_KEY:
            raise HTTPException(status_code=400, detail="MISTRAL_API_KEY is not configured")
        return {
            "Authorization": f"Bearer {settings.MISTRAL_API_KEY}",
            "content-type": "application/json",
        }
    elif provider == Provider.DEEPSEEK:
        if not settings.DEEPSEEK_API_KEY:
            raise HTTPException(status_code=400, detail="DEEPSEEK_API_KEY is not configured")
        return {
            "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}",
            "content-type": "application/json",
        }
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported provider: {provider}")

async def forward_request(model: str, payload: dict) -> tuple[dict, int, float]:
    provider = get_provider_from_model(model)
    url = PROVIDER_URLS[provider]
    headers = build_headers(provider)

    start = time.time()
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(url, json=payload, headers=headers)
    latency_ms = (time.time() - start) * 1000

    return response.json(), response.status_code, latency_ms

async def forward_streaming_request(model: str, payload: dict, on_complete):
    provider = get_provider_from_model(model)
    url = PROVIDER_URLS[provider]
    headers = build_headers(provider)

    input_tokens = 0
    output_tokens = 0
    start = time.time()

    async with httpx.AsyncClient(timeout=120.0) as client:
        async with client.stream("POST", url, json=payload, headers=headers) as response:
            async for line in response.aiter_lines():
                if not line:
                    continue

                # forward raw line to client
                yield f"{line}\n\n".encode()

                # parse for usage data
                if line.startswith("data:"):
                    data_str = line[len("data:"):].strip()
                    if data_str == "[DONE]":
                        continue
                    try:
                        data = json.loads(data_str)

                        # Anthropic sends usage in message_start
                        if data.get("type") == "message_start":
                            usage = data.get("message", {}).get("usage", {})
                            input_tokens = usage.get("input_tokens", 0)

                        # Anthropic sends output tokens in message_delta
                        if data.get("type") == "message_delta":
                            usage = data.get("usage", {})
                            output_tokens = usage.get("output_tokens", 0)

                    except json.JSONDecodeError:
                        pass

    latency_ms = (time.time() - start) * 1000

    # call the callback with usage data
    await on_complete(
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        latency_ms=latency_ms
    )