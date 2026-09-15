from config import settings
from providers.base import Provider
from providers.echo import EchoProvider
from schemas import ChatMessage

_PROVIDERS: dict[str, Provider] = {
    "echo": EchoProvider(),
}


def run(messages: list[ChatMessage]) -> str:
    """The loop: prompt -> maybe tool call -> maybe more prompting.

    Currently just delegates straight to the active provider; tool calls
    will be layered in here once agent/tools.py exists.
    """
    provider = _PROVIDERS[settings.provider]
    return provider.generate(messages)
