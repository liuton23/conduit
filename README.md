# Conduit

An open-source AI gateway and observability platform. Route requests to any LLM provider through a single endpoint, with automatic logging, cost tracking, and usage analytics.

## Features

- 🔀 **Multi-provider routing** — route requests across any LLM provider through a single endpoint
- 📊 **Usage tracking** — token counts, cost, and latency per request
- 🔑 **API key management** — virtual keys with per-project tagging
- ⚡ **Rate limiting** — Redis-backed request throttling per key
- 📈 **Dashboard** — visualize spend, volume, and latency over time
- 🌊 **Streaming support** — passthrough streaming with accurate token logging

## Tech Stack

- **Backend** — Python, FastAPI, SQLAlchemy, asyncpg
- **Database** — PostgreSQL
- **Cache** — Redis
- **Frontend** — React, TypeScript, Vite, Recharts
- **Infrastructure** — Docker, Docker Compose, Nginx

## Who is this for

Conduit is for developers who embed LLM calls in their apps and want visibility into usage, cost, and performance.

The setup is always the same pattern:
1. Deploy Conduit
2. Swap your API key and base URL
3. Tag requests by feature or project
4. Open the dashboard to monitor

**Solo developers** building a SaaS with AI features — track costs per feature or customer.

**Small teams** with multiple AI-powered products — one place to see all LLM spend across projects.

**Developer tools** like code reviewers or assistants — monitor which users consume the most tokens.

Conduit works anywhere you control the code making the API call. Your API keys and prompts never leave your own infrastructure.

### What Conduit works with

✅ Your own apps and scripts  
✅ Claude Code (terminal)  
✅ Cursor, Windsurf, VS Code AI extensions  
✅ Any tool that supports a custom base URL and API key  

### API key strategy

You can use one Conduit key across multiple apps and use the `X-Project` header to separate them — this is fine for solo developers.

For teams or multiple production apps, create a separate key per app. That way you can revoke access per app independently and get cleaner per-key analytics.
```python
# One key, multiple projects via header
client = anthropic.Anthropic(
    api_key="cdt-your-conduit-key",
    base_url="http://your-conduit-server",
    default_headers={"X-Project": "my-app"}
)
```

### Example — Claude Code

Route all your Claude Code terminal sessions through Conduit:
```bash
export ANTHROPIC_API_KEY="cdt-your-conduit-key"
export ANTHROPIC_BASE_URL="http://localhost:8000"
claude
```

Every coding session is now tracked in your Conduit dashboard.

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

- [ ] Per-key rate limit configuration
- [ ] Redis caching for key validation
- [ ] Cost alerts and budget limits
- [ ] OpenTelemetry support

## License

MIT