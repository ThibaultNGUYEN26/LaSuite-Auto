## Setup

Create a Python virtual environment and install the backend dependencies:

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
- `DRIVE_SESSION_ID` — development credential used for user-specific Drive
  endpoints. Copy the value of the `drive_sessionid` cookie from an authenticated
  local Drive session. Keep it in `.env` and never commit it.
- `DRIVE_CSRF_TOKEN` — the `csrftoken` cookie from the same authenticated Drive
  session, used by file-creation requests.
- `DRIVE_MAX_CREATE_BYTES` — maximum UTF-8 content size accepted by the Drive
  creation specialist. Defaults to 1 MiB.
- `DRIVE_MAX_UPLOAD_BYTES` — maximum size of an existing local file uploaded to
  Drive. Defaults to 50 MiB.
- `GRIST_API_KEY` — bearer API key created from Grist account settings.
- `GRIST_ORG_ID` — organization identifier from the Grist URL; for `/o/docs/`,
  use `docs`.
- `GRIST_WORKSPACE_ID` — optional default workspace where CSV imports are saved.

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

## Specialist-agent routing

The orchestrator is now independent from specialist implementations:

- `agent/base.py` defines the contract shared with every agent.
- `agent/registry.py` advertises available agents and dispatches model calls.
- `agent/drive.py` implements Drive configuration and authenticated recursive
  item listing.
- `providers/albert.py` contains only the Albert API client.
- `agent/orchestrator.py` coordinates the model/agent loop and registers the
  specialists available at runtime.

See `src/agent/README.md` for the Python-agent integration contract and safety
requirements.

## Run the first agent

The current orchestrator uses Albert for chat and exposes Drive configuration
and bounded recursive item listing as model-callable tools. Create your local
environment file from the committed template:

```bash
cp .env.example .env
# Then set ALBERT_API_KEY in .env. ALBERT_MODEL is optional.

source venv/bin/activate
python main.py
```

The orchestrator automatically loads `backend/.env`. Existing shell environment
variables take precedence over values in the file, and `.env` is ignored by Git.
When `ALBERT_MODEL` is omitted, the orchestrator reads Albert's live model
catalogue and uses the first canonical `text-generation` model id.

Send a request through the backend API:

```bash
curl -s http://127.0.0.1:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Which languages does Drive support?"}]}'
```

The Electron renderer sends this same POST request. Its backend URL defaults to
`http://127.0.0.1:8000`; copy `app/.env.example` to `app/.env` to override
`VITE_BACKEND_URL` when needed.
