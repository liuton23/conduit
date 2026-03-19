# Conduit

An open-source AI gateway and observability platform. Route requests to any LLM provider through a single endpoint, with automatic logging, cost tracking, and usage analytics.

## Features

- 🔀 **Multi-provider routing** — route requests across any LLM provider through a single endpoint
- 📊 **Usage tracking** — token counts, cost, and latency per request
- 🔑 **API key management** — virtual keys with per-project tagging
- ⚡ **Rate limiting** — Redis-backed request throttling
- 📈 **Dashboard** — visualize spend, volume, and latency over time

## Tech Stack

- **Backend** — Python, FastAPI, SQLAlchemy, asyncpg
- **Database** — PostgreSQL
- **Cache** — Redis
- **Infrastructure** — Docker, Docker Compose

## Status

| Feature | Status |
|--------|--------|
| Multi-provider proxy (Anthropic, OpenAI) | ✅ Done |
| Request logging (tokens, cost, latency) | ✅ Done |
| Project tagging via `X-Project` header | ✅ Done |
| Pricing loaded from `pricing.json` | ✅ Done |
| Virtual API key management | 🔧 In progress |
| Rate limiting per key | 🔧 In progress |
| Dashboard API endpoints | 🔧 In progress |
| Frontend dashboard | 🔧 In progress |

## Getting Started

### Prerequisites
- Docker Desktop
- Python 3.12+

### Setup

1. Clone the repo
```bash
   git clone https://github.com/yourusername/conduit.git
   cd conduit
```

2. Create a virtual environment
```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
```

3. Set up environment variables
```bash
   cp .env.example .env
```
   Fill in your API keys in `.env`

4. Start the services
```bash
   docker compose up -d
```

5. Run the server
```bash
   python -m uvicorn app.main:app --reload
```

6. Visit `http://localhost:8000/docs`

## Usage

Point your existing app at Conduit instead of Anthropic directly:
```python
import anthropic

client = anthropic.Anthropic(
    api_key="your-conduit-key",
    base_url="http://localhost:8000"
)
```

Tag requests by project for granular analytics:
```python
client = anthropic.Anthropic(
    api_key="your-conduit-key",
    base_url="http://localhost:8000",
    default_headers={"X-Project": "magsalita"}
)
```

All requests are automatically logged with token usage, cost, and latency.

## Updating Pricing

Model pricing is stored in `pricing.json` at the root of the project. To update:

1. Check the latest rates at:
   - Anthropic: https://anthropic.com/pricing
   - OpenAI: https://platform.openai.com/docs/pricing
2. Update the values in `pricing.json`
3. Update the `_comment` field with the date verified
4. Restart the server — no redeployment needed

Prices are per 1K tokens in USD.

## Roadmap

- [ ] Virtual API key management
- [ ] Rate limiting per key
- [ ] Observability dashboard
- [ ] Streaming support
- [ ] Cost alerts and budget limits
- [ ] Docker single-container deployment

## License

MIT