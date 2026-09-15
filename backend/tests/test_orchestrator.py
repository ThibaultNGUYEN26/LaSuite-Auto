import json
import os
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

from agent.orchestrator import OrchestratorAgent
from config import load_env_file
from schemas import ChatMessage


class FakeAlbertClient:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.requests = []

    def chat_completion(self, **request):
        self.requests.append(deepcopy(request))
        return next(self.responses)


class OrchestratorAgentTests(unittest.TestCase):
    def test_loads_env_file_without_overriding_existing_values(self):
        with tempfile.TemporaryDirectory() as directory:
            env_file = Path(directory) / ".env"
            env_file.write_text(
                'ALBERT_API_KEY="from-file"\nDRIVE_BASE_URL=http://drive:8071\n',
                encoding="utf-8",
            )
            with patch.dict(os.environ, {"ALBERT_API_KEY": "already-set"}, clear=True):
                load_env_file(env_file)
                self.assertEqual(os.environ["ALBERT_API_KEY"], "already-set")
                self.assertEqual(os.environ["DRIVE_BASE_URL"], "http://drive:8071")

    def test_returns_a_direct_model_answer(self):
        albert = FakeAlbertClient([{"role": "assistant", "content": "Hello."}])
        agent = OrchestratorAgent(
            albert,
            model="canonical-model-id",
            drive_base_url="http://drive:8071",
        )

        answer = agent.run([ChatMessage(role="user", content="Hello")])

        self.assertEqual(answer, "Hello.")
        self.assertEqual(len(albert.requests), 1)

    @patch("agent.orchestrator.get_drive_config")
    def test_executes_drive_tool_and_returns_the_follow_up_answer(self, get_config):
        get_config.return_value = {"LANGUAGE_CODE": "fr-fr"}
        albert = FakeAlbertClient(
            [
                {
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [
                        {
                            "id": "call-1",
                            "type": "function",
                            "function": {
                                "name": "drive_get_config",
                                "arguments": "{}",
                            },
                        }
                    ],
                },
                {"role": "assistant", "content": "Drive uses French."},
            ]
        )
        agent = OrchestratorAgent(
            albert,
            model="canonical-model-id",
            drive_base_url="http://drive:8071",
        )

        answer = agent.run(
            [ChatMessage(role="user", content="Which language does Drive use?")]
        )

        self.assertEqual(answer, "Drive uses French.")
        tool_message = albert.requests[1]["messages"][-1]
        self.assertEqual(tool_message["role"], "tool")
        self.assertEqual(tool_message["tool_call_id"], "call-1")
        self.assertEqual(json.loads(tool_message["content"]), {"LANGUAGE_CODE": "fr-fr"})
        get_config.assert_called_once_with("http://drive:8071")


if __name__ == "__main__":
    unittest.main()
