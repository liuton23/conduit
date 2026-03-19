# Conduit

An open-source AI gateway and observability platform. Route requests to multiple LLM providers (Anthropic, OpenAI) through a single endpoint, with automatic logging, cost tracking, and usage analytics.

## Features

- 🔀 **Multi-provider routing** — Anthropic and OpenAI through one API
- 📊 **Usage tracking** — token counts, cost, and latency per request
- 🔑 **API key management** — virtual keys with per-project tagging
- ⚡ **Rate limiting** — Redis-backed request throttling
- 📈 **Dashboard** — visualize spend, volume, and latency over time

## Tech Stack

- **Backend** — Python, FastAPI, SQLAlchemy, asyncpg
- **Database** — PostgreSQL
- **Cache** — Redis
- **Infrastructure** — Docker, Docker Compose

## Getting Started

### Prerequisites
- Docker Desktop
- Python 3.12+

### Setup

1. Clone the repo
```bash
   git clone https://github.com/liuton23/conduit.git
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

All requests are automatically logged and tracked.

## Roadmap

- [ ] Virtual API key management
- [ ] Rate limiting per key
- [ ] Observability dashboard
- [ ] Streaming support
- [ ] Cost alerts and budget limits
- [ ] Docker single-container deployment

## License

MIT