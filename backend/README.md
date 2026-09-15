## Setup

Dependencies and the virtualenv are managed with [uv](https://docs.astral.sh/uv/).

```bash
uv sync           # creates .venv and installs dependencies from uv.lock (only needed after cloning or changing deps)
uv add <package>  # add a new dependency (updates pyproject.toml + uv.lock)
cp .env.example .env  # then edit BACKEND_URL if not running on the default host/port
uv run main.py    # run the dev server with reload, on the host/port from BACKEND_URL
```

## Configuration

Copy `.env.example` to `.env` and adjust as needed:

- `BACKEND_URL` — full URL (protocol + host + port) the server binds to, e.g.
  `http://127.0.0.1:8000`. The frontend (`app/.env`) must be set to the same
  value so it knows where to reach this server — change the host here if the
  backend runs on a different machine than the Electron app.
- `AUTO_CORS_ORIGINS` — comma-separated list of origins allowed to call the
  backend. Defaults to `*`.

## Structure

```
backend/src/
├── main.py              # FastAPI app, routes
├── schemas.py           # Pydantic models for requests/responses
├── config.py            # Which provider/model is active, loaded from settings
├── providers/           # "How do I talk to a model?"
│   ├── base.py          # Abstract interface every provider implements
│   ├── lasuite.py       # Interface to lasuit tokens 
└── agent/               # "What does the agent do with the model?"
    ├── tools/           # Folder to indivudual tool defs
    │   ├── readFile.py  # An idea
    │   ├── runbash.py   # An idea
    ├── orchestrator.py  # The loop: prompt -> maybe tool call -> maybe more prompting
    ├── tools.py         # Collated all the tool calls the agent can call
    └── memory.py        # Conversation history, context management
```