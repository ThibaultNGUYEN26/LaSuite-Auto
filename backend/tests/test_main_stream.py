import unittest
import tempfile
from pathlib import Path
from unittest.mock import ANY, patch

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

    async def _yield_final_event(self, messages):
        yield AgentEvent(
            "final", {"content": "Answer now", "total_duration_ms": 1250}
        )

    def test_persists_the_assistant_response_when_stream_finishes(self):
        with patch("main.run_stream", self._yield_final_event), patch(
            "main.chat_repository.save_history"
        ) as save_history:
            response = self.client.post(
                "/api/chat/stream",
                json={
                    "chat_id": "conversation-1",
                    "messages": [{"role": "user", "content": "Question"}],
                },
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(save_history.call_count, 2)
        persisted_messages = save_history.call_args_list[-1].args[2]
        self.assertEqual(persisted_messages[-1].role, "assistant")
        self.assertEqual(persisted_messages[-1].content, "Answer now")
        self.assertEqual(
            persisted_messages[-1].trace,
            [{"type": "total", "durationMs": 1250}],
        )

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


class LocalEvidenceEndpointTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_serves_a_pdf_inline_for_page_aware_links(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "Client").mkdir()
            (root / "Client/evidence.pdf").write_bytes(b"%PDF-test")
            with patch.object(settings, "local_files_root", root):
                response = self.client.get(
                    "/api/local-files/view",
                    params={"path": "Client/evidence.pdf", "page": 3},
                )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "application/pdf")
        self.assertTrue(response.headers["content-disposition"].startswith("inline;"))
        self.assertEqual(response.content, b"%PDF-test")

    def test_rejects_paths_outside_the_local_files_root(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(settings, "local_files_root", Path(directory)):
                response = self.client.get(
                    "/api/local-files/view",
                    params={"path": "../secret.pdf", "page": 1},
                )

        self.assertEqual(response.status_code, 404)


class ConversationTitleEndpointTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_returns_a_generated_title(self):
        async def title_generator(prompt, response):
            self.assertEqual(prompt, "Analyse these figures")
            self.assertEqual(response, "Sales increased by 12%")
            return "Sales trend analysis"

        with patch("main.generate_chat_title", title_generator):
            response = self.client.post(
                "/api/conversations/title",
                json={
                    "prompt": "Analyse these figures",
                    "response": "Sales increased by 12%",
                },
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"title": "Sales trend analysis"})

    def test_persists_the_title_when_a_chat_id_is_supplied(self):
        async def title_generator(prompt, response):
            return "Sales trend analysis"

        with patch("main.generate_chat_title", title_generator), patch(
            "main.chat_repository.rename", return_value=object()
        ) as rename:
            response = self.client.post(
                "/api/conversations/title",
                json={
                    "chat_id": "conversation-1",
                    "prompt": "Analyse these figures",
                    "response": "Sales increased by 12%",
                },
            )

        self.assertEqual(response.status_code, 200)
        rename.assert_called_once_with(
            ANY, "conversation-1", "Sales trend analysis"
        )


if __name__ == "__main__":
    unittest.main()
