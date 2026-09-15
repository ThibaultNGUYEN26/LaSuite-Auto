## Setup

Create a Python virtual environment and install the backend dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
python main.py  # http://127.0.0.1:8000
```

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

## Run the first agent

The current orchestrator uses Albert for chat and exposes Drive's public
configuration endpoint as a model-callable tool. Create your local environment
file from the committed template:

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
