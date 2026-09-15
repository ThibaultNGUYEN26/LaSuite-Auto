# Architecture reference: `suitenumerique/conversations`

Research notes on how the open-source reference project **conversations**
(cloned locally at `C:\Users\Camille\Documents\Git\conversations`, upstream
[suitenumerique/conversations](https://github.com/suitenumerique/conversations))
is structured, for use while developing this Electron chatbot (`auto/app`).

We share its UI kit (`@gouvfr-lasuite/cunningham-react`, `@gouvfr-lasuite/ui-kit`),
so its frontend patterns are directly relevant even though our shell (Electron
+ Vite, no Next.js) and backend (small fastAPI app vs. their Django) differ.

**All paths below are relative to `C:\Users\Camille\Documents\Git\conversations`
unless noted — treat that checkout as the source of truth and re-check it if
these notes go stale.**

---

## 1. Top-level layout

Yarn workspaces monorepo:

- `src/frontend/apps/` — deployable apps
  - `conversations/` — the actual chat SPA (Vite-built React, **not** Next.js)
  - `e2e/` — end-to-end tests
- `src/frontend/packages/` — shared packages
  - `eslint-config-conversations/`
  - `i18n/`
- `src/backend/` — Django project, split into focused apps:
  - `chat/` — the LLM/chat domain (see §5)
  - `conversations/` — Django project settings/urls/asgi (just the project shell, confusingly named same as the repo)
  - `core/` — shared models/auth (not deeply reviewed)
  - `activation_codes/`, `demo/`, `locale/`
- `env.d/` — env var templates at repo root
- `compose.yml`, `Dockerfile` — local dev / self-host

## 2. Frontend structure — feature-folder pattern

Source root: `src/frontend/apps/conversations/src/`

Organized **by feature, not by type**. This is the main thing worth porting.

```
src/
├── features/
│   ├── chat/
│   │   ├── api/          # React Query hooks: useChat, useConversation(s),
│   │   │                 # useCreateConversation, useRenameConversation, ...
│   │   ├── components/   # chat UI
│   │   ├── hooks/        # pure UI hooks: useChatScroll, useFileDragDrop
│   │   ├── stores/       # feature-scoped Zustand stores
│   │   ├── utils/
│   │   └── assets/
│   ├── auth/
│   ├── attachments/
│   ├── left-panel/
│   ├── settings/
│   ├── onboarding/
│   ├── banner/
│   ├── sources-panel/
│   ├── header/
│   ├── footer/
│   ├── home/
│   ├── language/
│   ├── feedback/
│   └── maintenance/
├── core/
│   └── config/
│       ├── ConfigProvider.tsx        # app-wide config context
│       ├── api/useConfig.tsx         # fetches runtime config
│       └── hooks/useFeatureEnabled.ts
├── api/                    # thin APP-WIDE fetch layer, everything else builds on this
│   ├── index.ts
│   ├── fetchApi.ts
│   ├── APIError.ts
│   ├── rateLimit.ts
│   ├── config.ts
│   ├── types.ts
│   └── utils.ts
├── stores/                 # only TRULY global stores
│   ├── useResponsiveStore.tsx
│   └── useSentryStore.tsx
└── pages/                  # thin, route-level composition only
    ├── chat/
    ├── home/
    └── login/
```

Not every feature needs `api/`/`components/`/`hooks/`/`stores/` — features have
only the subset they actually use.

Tests are colocated in `__tests__/` next to the code they cover, at every
level (components, hooks, api, utils) — not a separate top-level `tests/` tree.

**For our app:** replace the current flat `components/` + `lib/` split
(`src/renderer/src/components/ChatWindow.tsx`, `src/renderer/src/lib/api.ts`)
with `features/<domain>/{api,components,hooks,stores}`, plus one small
app-wide `src/api/` module for the raw fetch wrapper and error types.

## 3. State management — layered, not monolithic

Three distinct layers, kept separate rather than one global store:

| Layer | Tool | Example |
|---|---|---|
| Server/async state (CRUD) | `@tanstack/react-query` | `features/chat/api/useConversations.tsx`, `useCreateConversation.tsx` |
| Streaming chat state | `@ai-sdk/react` (`useChat`), wrapped | `features/chat/api/useChat.tsx` |
| Local UI/client state | `zustand`, one store per concern | `features/chat/stores/useChatPreferencesStore.ts` (uses `persist` for theme/model/panel prefs), `usePendingChatStore.ts`, `useScrollStore.ts` |

`features/chat/api/useChat.tsx` does **not** use `@ai-sdk/react`'s `useChat`
raw — it wraps it with:
- a `DefaultChatTransport` with a custom `fetch` adapter (`fetchAPIAdapter`)
  that injects query params from a Zustand store at request time
- an `onData` callback that parses custom SSE data events
  (`conversation_metadata`, `cooldown`, `images_skipped`, typed with runtime
  type guards) and triggers `queryClient.invalidateQueries` or local state
  updates
- a separate `useQuery` polling a cooldown endpoint to resync rate-limit
  state across tabs

Global stores (`src/stores/`) hold only things genuinely app-wide
(responsive breakpoint, Sentry). Everything feature-specific (chat prefs,
scroll position, pending messages) lives in `features/chat/stores/`.

**For our app:** don't hand-roll SSE parsing — use `@ai-sdk/react`'s
`useChat` / `DefaultChatTransport` and wrap it once for any custom backend
events; use React Query for anything CRUD-like (conversation list, rename,
delete); keep Zustand stores small, single-purpose, and colocated per
feature rather than one big store.

## 4. Streaming handling

- **Client:** `DefaultChatTransport({ api, fetch: fetchAPIAdapter })` from
  the `ai` package, consuming a Vercel-AI-SDK-shaped SSE stream, with custom
  data-part events multiplexed through `onData`.
  File: `src/frontend/apps/conversations/src/features/chat/api/useChat.tsx`
- **Backend:** `src/backend/chat/clients/pydantic_ai.py` — `async def
  stream_data_async(...)` streams UI-message-protocol chunks. A comment in
  this file notes the event-type constants are "Mirrored in `pydantic_ai.py`"
  — i.e. they deliberately keep a documented client/server contract for
  custom stream event types rather than letting the two drift.

## 5. Backend (`src/backend/chat/`) — lighter relevance, our backend is Express

One-file-per-concern style, worth noting as a pattern even though our stack
differs:

- `agents/` — Pydantic AI agent definitions
- `clients/pydantic_ai.py` — LLM client + streaming (~1950 lines)
- `tools/` — RAG search, web search, presentation generation — one file each
- `views/` — REST endpoints: `conversations.py`, `attachments.py`,
  `llm_config.py`
- `providers/` — model provider config (multi-provider abstraction)
- `model_routing.py`, `rate_limiting.py`
- `vercel_ai_sdk/`, `ai_sdk_types.py` — types/helpers matching the AI SDK
  wire format
- `agent_rag/`, `docs_client.py`, `document_context_builder.py`,
  `malware_detection.py`, `mcp_servers.py`, `evals/`

## 6. Styling / design system

- `@gouvfr-lasuite/cunningham-react` — the shared design system (we already
  depend on this), with generated design tokens under `src/cunningham/`
- `styled-components` for one-off component styling
- a `globals.css` for global resets

Cunningham itself isn't something to re-architect around, but the pattern —
one generated-tokens dir + component-local styling on top — is reasonable to
copy independent of adopting Cunningham wholesale.

## 7. Cross-cutting

- `env.d/` at repo root — env var templates for local dev / self-host
- `compose.yml` + `Dockerfile` — local dev environment
- Frontend has per-environment env files: `apps/conversations/.env`,
  `.env.development`, `.env.test`
- `docs/` at repo root (not deeply reviewed here)

---

## Key files to open when in doubt

| What | Path (under `C:\Users\Camille\Documents\Git\conversations`) |
|---|---|
| Streaming chat hook wrapper | `src/frontend/apps/conversations/src/features/chat/api/useChat.tsx` |
| Zustand store pattern (persisted prefs) | `src/frontend/apps/conversations/src/features/chat/stores/useChatPreferencesStore.ts` |
| App-wide fetch layer | `src/frontend/apps/conversations/src/api/index.ts`, `src/frontend/apps/conversations/src/api/fetchApi.ts` |
| Feature folder structure (template) | `src/frontend/apps/conversations/src/features/` |
| Backend streaming implementation | `src/backend/chat/clients/pydantic_ai.py` |
| Backend REST views | `src/backend/chat/views/` |

## Suggested next step for `auto/app`

Current renderer structure (`src/renderer/src/`) is flat:
`components/ChatWindow.tsx`, `lib/api.ts`. Before it grows further, consider
migrating to:

```
src/renderer/src/
├── features/
│   └── chat/
│       ├── api/        # e.g. useChat.ts wrapping @ai-sdk/react, useConversations.ts
│       ├── components/ # ChatWindow.tsx, MessageList.tsx, Composer.tsx
│       ├── hooks/
│       └── stores/      # zustand: chat prefs, pending message state
├── api/                 # app-wide fetch wrapper + APIError, replaces current lib/api.ts
└── stores/               # only truly global state, if/when it exists
```

This mirrors §2 above and gives room to add conversation history, streaming,
and multi-provider backend config without another restructure.
