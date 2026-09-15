class ConversationMemory:
    """
    Stores the conversation between the user, the assistant,
    and the tools used by the agent.
    """

    def __init__(self, max_messages: int = 20):
        if not isinstance(max_messages, int):
            raise TypeError("max_messages must be an integer")
        if max_messages <= 0:
            raise ValueError("max_messages must be greater than 0")

        self.messages: list[dict[str, str]] = []
        self.max_messages = max_messages

    def _append_message(self, message: dict[str, str]) -> None:
        self.messages.append(message)
        self._limit_messages()

    def add_user_message(self, content: str) -> None:
        self._append_message({"role": "user", "content": self._validate_text(content)})

    def add_assistant_message(self, content: str) -> None:
        self._append_message({"role": "assistant", "content": self._validate_text(content)})

    def add_tool_message(self, tool_name: str, result: str) -> None:
        self._append_message({
            "role": "tool",
            "tool_name": self._validate_text(tool_name),
            "content": self._validate_text(result),
        })

    def get_messages(self) -> list[dict[str, str]]:
        return list(self.messages)

    def _validate_text(self, value: str) -> str:
        if not isinstance(value, str):
            raise TypeError("message content must be a string")
        return value

    def _limit_messages(self) -> None:
        """
        Keeps only the most recent messages.
        This prevents the conversation from becoming too large.
        """
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]

    def clear(self) -> None:
        self.messages = []


class AgentContext:
    """
    Stores temporary information the agent finds while
    working on the current question.
    """

    def __init__(self):
        self.query: str | None = None
        self.documents: list[dict[str, str]] = []
        self.evidence: list[str] = []

    def set_query(self, query: str | None) -> None:
        if query is not None and not isinstance(query, str):
            raise TypeError("query must be a string or None")
        self.query = query

    def add_document(self, document: dict[str, str]) -> None:
        if not isinstance(document, dict):
            raise TypeError("document must be a dictionary")
        if "title" not in document or "text" not in document:
            raise ValueError("document must include 'title' and 'text'")
        self.documents.append(document)

    def add_evidence(self, evidence: str) -> None:
        if not isinstance(evidence, str):
            raise TypeError("evidence must be a string")
        self.evidence.append(evidence)

    def get_context(self) -> dict[str, object]:
        """
        Returns the current context as Python data.
        """
        return {
            "query": self.query,
            "documents": list(self.documents),
            "evidence": list(self.evidence),
        }

    def get_context_for_llm(self) -> str:
        """
        Converts the current context into text that can be given to the LLM.
        """
        context = "Current question:\n"
        context += self.query if self.query is not None else "N/A"
        context += "\n\n"

        if self.documents:
            context += "Relevant documents:\n"

            for document in self.documents:
                title = str(document.get("title", "Untitled document"))
                text = str(document.get("text", ""))
                date = document.get("date")

                context += f"\nDocument: {title}\n"
                if date is not None:
                    context += f"Date: {date}\n"
                context += f"Content: {text}\n"

        if self.evidence:
            context += "\nEvidence:\n"

            for evidence in self.evidence:
                context += f"- {evidence}\n"

        return context

    def clear(self) -> None:
        """
        Clears the temporary research context.
        """
        self.query = None
        self.documents = []
        self.evidence = []
