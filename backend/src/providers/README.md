# Providers

The provider layer is the interface to model backends. It is intentionally narrow: the orchestrator and the specialist agents depend on a provider contract, not on one specific vendor implementation.

## Core contract

The abstract provider interface is defined in `providers/base.py`:

```python
class Provider(ABC):
    @abstractmethod
    def generate(self, messages: list[ChatMessage]) -> str:
        ...
```

This is the minimal abstraction used by the app for simple non-streaming text generation.

## Current implementations

### `echo.py`
A lightweight fallback implementation used when a real model provider is unavailable or disabled. It returns a deterministic demo-style response based on the latest user message.

### `albert.py`
The active production provider for the application. It is responsible for:

- resolving available model IDs
- streaming chat completions from the Albert backend
- handling tool calls and content deltas
- surfacing API-level errors consistently

The class wraps the model HTTP API and is used by the orchestrator and service utilities such as chat title generation and PDF memory creation.

## Design notes

- Providers are intentionally decoupled from the orchestrator logic.
- The orchestrator only cares that a provider can answer a chat completion request.
- External API specifics, model selection, and auth details live in the provider implementation rather than in the reasoning code.

## Related docs

- [backend/src/agent/README.md](../agent/README.md)
- [backend/src/services/README.md](../services/README.md)
- [backend/README.md](../../README.md)
