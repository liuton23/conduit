import httpx
import time
from app.config import settings
from app.models.enums import Provider, get_provider_from_model

PROVIDER_URLS = {
    Provider.ANTHROPIC: "https://api.anthropic.com/v1/messages",
    Provider.OPENAI: "https://api.openai.com/v1/chat/completions",
}

def build_headers(provider: Provider) -> dict:
    if provider == Provider.ANTHROPIC:
        return {
            "x-api-key": settings.ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
    return {
        "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
        "content-type": "application/json",
    }

async def forward_request(model: str, payload: dict) -> tuple[dict, int, float]:
    provider = get_provider_from_model(model)
    url = PROVIDER_URLS[provider]
    headers = build_headers(provider)

    start = time.time()
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(url, json=payload, headers=headers)
    latency_ms = (time.time() - start) * 1000

    return response.json(), response.status_code, latency_ms