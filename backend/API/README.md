# API Reference

This directory documents the two API surfaces used by the project:

1. The backend HTTP API exposed by the orchestration service.
2. The generated Drive Python client used by agents to call Drive endpoints.

The backend runs by default at `http://127.0.0.1:8000` and exposes a FastAPI application. Interactive documentation is available at `/docs`, and the OpenAPI document is available at `/openapi.json`.

---

## Backend HTTP API

### Health

#### `GET /api/health`

Returns `{"status":"ok"}` when the backend is running.

### Chat and conversations

#### `POST /api/chat/stream`

Streams orchestration progress and the final assistant response as Server-Sent Events. The response content type is `text/event-stream`.

Request body:

```json
{
  "chat_id": "optional-conversation-id",
  "messages": [
    {"role": "user", "content": "Summarize my latest report"}
  ]
}
```

Allowed message roles are `user` and `assistant`. When `chat_id` is supplied, the request history is saved before streaming and the final assistant response is saved when the stream completes.

Each event has an SSE `event` name and JSON `data`. Common event names include `step_start`, `token`, `step_complete`, `final`, and `error`.

Because the response may already have started, agent failures are returned as an `error` event rather than an HTTP error response.

#### `POST /api/conversations/new`

Acknowledges a new conversation:

```json
{"status": "ok"}
```

#### `GET /api/conversations`

Returns saved conversations, including their messages and timestamps.

#### `DELETE /api/conversations/{chat_id}`

Deletes a conversation. Returns `404` when the conversation does not exist.

Successful response:

```json
{"status": "ok"}
```

#### `POST /api/conversations/title`

Generates a short title from the first user prompt and assistant response.

Request body:

```json
{
  "chat_id": "optional-conversation-id",
  "prompt": "Analyse the sales figures",
  "response": "Sales increased by 12% compared with last quarter."
}
```

Response:

```json
{"title": "Quarterly sales trend"}
```

When `chat_id` is supplied, the generated title is persisted. A missing chat returns `404`; provider failures return `502`.

### Agent capabilities

#### `GET /api/agent/specializations`

Returns the capability groups advertised to the frontend. Each specialization includes its identifier, description, enabled state, and tool summaries.

The `enabled` field is currently always `true`; there is no per-user specialization preference storage yet.

### Workflows

#### `POST /api/workflows/draft`

Creates a reusable workflow draft from a conversation.

Request body:

```json
{
  "messages": [
    {"role": "user", "content": "Create a monthly sales report"}
  ]
}
```

The response contains `name`, `description`, `instructions`, and `input_question`. Provider or generation failures return `422`.

#### `GET /api/workflows`

Returns saved workflows ordered by creation date.

#### `POST /api/workflows`

Creates a workflow.

Request body:

```json
{
  "name": "Monthly sales report",
  "description": "Create a monthly report from sales data",
  "instructions": "Read the CSV, analyze the trends, and create a PDF",
  "input_question": "Which month should be analyzed?"
}
```

#### `DELETE /api/workflows/{workflow_id}`

Deletes a workflow. Returns `404` when the workflow does not exist.

### Related documentation

- [Backend setup and configuration](../README.md)
- [Capability block contract](../BLOCKS.md)
- [Agent architecture](../src/agent/README.md)

---

## Drive API client

`drive_client` is a Python client generated from Drive’s OpenAPI specification (`swagger.json`) using OpenAPI Generator.

It provides Python methods and data models to call the real Drive API, plus documentation for the operations included in the specification. Our agents can use this client from the orchestration backend. It does not require FastAPI or start another server: Drive must already be running.

### Generate the client

Run these commands from the `backend` directory.

Download the specification:

```bash
curl -fS \
  'http://localhost:8071/api/v1.0/swagger.json' \
  -o swagger.json
```

Once the download succeeds, generate the Python client:

```bash
sudo docker run --rm \
  --user "$(id -u):$(id -g)" \
  -v "$PWD:/local" \
  openapitools/openapi-generator-cli generate \
  -i /local/swagger.json \
  -g python \
  -o /local/API/drive_client
```

### Install

Create and activate a virtual environment, then install the local package:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ./API/drive_client
```

Add `.venv/` to `.gitignore`. Reactivate the environment in each new terminal with `source .venv/bin/activate`.

### Usage and authentication

Import the client into your Python code, configure the Drive server address, and call the generated methods. Examples and method names are available in `API/drive_client/README.md`.

Authentication depends on the endpoint:

- Public configuration: no authentication required.
- Files and folders: an authenticated user session or an OIDC access token accepted by Drive.
- Storage metrics: a separate API key, which does not grant access to files.

Keep credentials outside the generated code and Git repository.

### Current limitations

Metrics were excluded from our Swagger specification to work around a schema-generation error, so their endpoint is absent from this client.

The generated `NullEnum` contained invalid syntax (`class NullEnum(, Enum):`), temporarily corrected to `class NullEnum(Enum):`. Regeneration may overwrite this fix; nullable model behavior still needs validation.

---

## Summary

The backend API and the Drive client serve complementary roles:

- The backend API is the orchestration layer and user-facing interface.
- The Drive client is the typed integration layer used by agents to access Drive resources.

Together, they define the contract between the automation backend and the underlying Drive service.
