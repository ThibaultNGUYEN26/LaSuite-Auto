import json
import unittest
from copy import deepcopy
from unittest.mock import patch

from agent.base import DelegationContext, SpecialistAgent
from agent.orchestrator import OrchestratorAgent, build_agent_registry
from agent.registry import AgentRegistry
from schemas import ChatMessage


class FakeAlbertClient:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.requests = []

    def chat_completion(self, **request):
        self.requests.append(deepcopy(request))
        return next(self.responses)


class FakePythonAgent(SpecialistAgent):
    name = "python_execute"
    description = "Run an approved Python task against files in a working directory."
    parameters = {
        "type": "object",
        "properties": {
            "task": {"type": "string"},
            "working_directory": {"type": "string"},
        },
        "required": ["task", "working_directory"],
        "additionalProperties": False,
    }

    def __init__(self):
        self.calls = []

    def execute(self, arguments: dict, context: DelegationContext) -> dict:
        self.calls.append((arguments, context))
        return {"status": "completed", "files_changed": 2}


class OrchestratorAgentTests(unittest.TestCase):
    def test_runtime_registry_advertises_both_drive_capabilities(self):
        names = {
            tool["function"]["name"]
            for tool in build_agent_registry().tool_definitions()
        }
        self.assertEqual(names, {"drive_get_config", "drive_list_items"})

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

    @patch("agent.drive.get_drive_config")
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

    def test_routes_a_task_to_a_registered_python_agent(self):
        python_agent = FakePythonAgent()
        registry = AgentRegistry([python_agent])
        albert = FakeAlbertClient(
            [
                {
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [
                        {
                            "id": "call-python",
                            "type": "function",
                            "function": {
                                "name": "python_execute",
                                "arguments": json.dumps(
                                    {
                                        "task": "Group PDFs by year",
                                        "working_directory": "Downloads",
                                    }
                                ),
                            },
                        }
                    ],
                },
                {"role": "assistant", "content": "I organized the PDFs."},
            ]
        )
        agent = OrchestratorAgent(
            albert,
            model="canonical-model-id",
            registry=registry,
        )

        answer = agent.run(
            [ChatMessage(role="user", content="Organize the PDFs in Downloads")]
        )

        self.assertEqual(answer, "I organized the PDFs.")
        self.assertEqual(python_agent.calls[0][0]["working_directory"], "Downloads")
        self.assertEqual(
            json.loads(albert.requests[1]["messages"][-1]["content"]),
            {"status": "completed", "files_changed": 2},
        )
        advertised_names = {
            tool["function"]["name"] for tool in albert.requests[0]["tools"]
        }
        self.assertEqual(advertised_names, {"python_execute"})


if __name__ == "__main__":
    unittest.main()
