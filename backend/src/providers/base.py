from abc import ABC, abstractmethod

from schemas import ChatMessage


class Provider(ABC):
    """Abstract interface every model provider implements."""

    @abstractmethod
    def generate(self, messages: list[ChatMessage]) -> str:
        """Given the conversation so far, return the assistant's reply."""
