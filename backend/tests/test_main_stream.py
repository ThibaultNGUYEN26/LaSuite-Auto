import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from agent.errors import AgentError
from agent.events import AgentEvent
from config import settings
from main import app


def parse_sse(body: str) -> list[tuple[str, str]]:
    events = []
    for frame in body.strip("\n").split("\n\n"):
        if not frame:
            continue
        lines = frame.split("\n")
        event_type = next(line[len("event: ") :] for line in lines if line.startswith("event: "))
        data = next(line[len("data: ") :] for line in lines if line.startswith("data: "))
        events.append((event_type, data))
    return events


class ChatStreamEndpointTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_streams_a_final_event_for_the_echo_provider(self):
        with patch.object(settings, "provider", "echo"):
            response = self.client.post(
                "/api/chat/stream",
                json={"messages": [{"role": "user", "content": "Hi there"}]},
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "text/event-stream; charset=utf-8")
        events = parse_sse(response.text)
        self.assertEqual(events[-1][0], "final")
        self.assertIn("Hi there", events[-1][1])

    async def _raise_agent_error(self, messages):
        raise AgentError("boom")
        yield AgentEvent("unreachable", {})  # pragma: no cover - makes this a generator

    def test_reports_agent_errors_as_an_sse_event_with_status_200(self):
        with patch("main.run_stream", self._raise_agent_error):
            response = self.client.post(
                "/api/chat/stream",
                json={"messages": [{"role": "user", "content": "Hi there"}]},
            )

        self.assertEqual(response.status_code, 200)
        events = parse_sse(response.text)
        self.assertEqual(events[-1][0], "error")
        self.assertIn("boom", events[-1][1])


class NewConversationEndpointTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_acknowledges_a_new_conversation(self):
        response = self.client.post("/api/conversations/new")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})


if __name__ == "__main__":
    unittest.main()
