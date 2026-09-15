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