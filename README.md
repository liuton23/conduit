# Conduit

An open-source AI gateway and observability platform. Route requests to any LLM provider through a single endpoint, with automatic logging, cost tracking, and usage analytics.

## Features

- 🔀 **Multi-provider routing** — route requests across any LLM provider through a single endpoint
- 📊 **Usage tracking** — token counts, cost, and latency per request
- 🔑 **API key management** — virtual keys with per-project tagging
- ⚡ **Rate limiting** — Redis-backed request throttling per key
- 📈 **Dashboard** — visualize spend, volume, and latency over time

## Tech Stack

- **Backend** — Python, FastAPI, SQLAlchemy, asyncpg
- **Database** — PostgreSQL
- **Cache** — Redis
- **Frontend** — React, TypeScript, Vite, Recharts
- **Infrastructure** — Docker, Docker Compose, Nginx

## Getting Started

### Prerequisites
- Docker Desktop

### Setup

1. Clone the repo
```bash
   git clone https://github.com/yourusername/conduit.git
   cd conduit
```

2. Set up environment variables
```bash
   cp .env.example .env
```
   Fill in your API keys in `.env`

3. Start everything
```bash
   docker compose up --build
```

4. Open `http://localhost:3000`

That's it. No separate installs needed.

## Usage

### 1. Create an API key
Log into the dashboard at `http://localhost:3000` and create an API key from the **API Keys** page.

### 2. Point your app at Conduit
```python
import anthropic

client = anthropic.Anthropic(
    api_key="your-conduit-key",
    base_url="http://localhost:8000"
)
```

### 3. Tag requests by project
```python
client = anthropic.Anthropic(
    api_key="your-conduit-key",
    base_url="http://localhost:8000",
    default_headers={"X-Project": "my-app"}
)
```

All requests are automatically logged with token usage, cost, and latency.

## Updating Pricing

Pricing is stored in `pricing.json` at the root of the project. Update the values and restart the server — no redeployment needed.

Sources:
- Anthropic: https://anthropic.com/pricing
- OpenAI: https://platform.openai.com/docs/pricing

## Roadmap

- [ ] Streaming support
- [ ] Per-key rate limit configuration
- [ ] Redis caching for key validation
- [ ] Cost alerts and budget limits
- [ ] OpenTelemetry support

## License

MIT