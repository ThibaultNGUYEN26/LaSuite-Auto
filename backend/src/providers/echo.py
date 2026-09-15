from providers.base import Provider
from schemas import ChatMessage


class EchoProvider(Provider):
    """Placeholder provider used until a real model backend is wired up."""

    def generate(self, messages: list[ChatMessage]) -> str:
        last_user_message = messages[-1].content if messages else ""
        return f"## In markdown\n_You said_: {last_user_message}"
