import json
import unittest
from copy import deepcopy
from unittest.mock import patch

from agent.base import DelegationContext, SpecialistAgent
from agent.blocks import (
    AgentBlock,
    BlockRegistry,
    WorkflowManifest,
    build_agent_registry,
)
from agent.orchestrator import OrchestratorAgent
from agent.registry import AgentRegistry
from agent.specialists.drive import DriveConfigAgent
from schemas import ChatMessage


class FakeAlbertClient:
    """Fakes a streaming Albert client: one entry per step's response.

    Each entry is ``{"content": str | None, "tool_calls": list | None}``.
    Content (if any) is emitted as a single ``content`` chunk, followed by
    the ``done`` chunk carrying the step's tool calls.
    """

    def __init__(self, responses):
        self.responses = iter(responses)
        self.requests = []

    async def chat_completion_stream(self, **request):
        self.requests.append(deepcopy(request))
        response = next(self.responses)
        content = response.get("content")
        if content:
            yield {"type": "content", "delta": content}
        yield {"type": "done", "tool_calls": response.get("tool_calls") or []}


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


class FakeCreateCsvAgent(SpecialistAgent):
    name = "local_create_csv"
    description = "Create a CSV file on the local computer."
    parameters = {
        "type": "object",
        "properties": {"path": {"type": "string"}},
        "required": ["path"],
        "additionalProperties": False,
    }

    def execute(self, arguments: dict, context: DelegationContext) -> dict:
        return {
            "status": "created",
            "artifact": {
                "kind": "file",
                "location": "local",
                "reference": arguments["path"],
                "media_type": "text/csv",
                "name": "sales.csv",
            },
        }


class FakeGristImportAgent(SpecialistAgent):
    name = "grist_import_csv"
    description = "Import a CSV artifact into Grist."
    parameters = {
        "type": "object",
        "properties": {"artifact": {"type": "object"}},
        "required": ["artifact"],
        "additionalProperties": False,
    }

    def __init__(self):
        self.calls = []

    def execute(self, arguments: dict, context: DelegationContext) -> dict:
        self.calls.append(arguments)
        return {"status": "imported", "document_id": "grist-doc-1"}


async def collect_events(agent, conversation):
    events = []
    async for event in agent.run_stream(conversation):
        events.append(event)
    return events


class OrchestratorAgentTests(unittest.IsolatedAsyncioTestCase):
    def test_runtime_registry_advertises_discovered_capabilities(self):
        names = {
            tool["function"]["name"]
            for tool in build_agent_registry().tool_definitions()
        }
        self.assertEqual(
            names,
            {
                "drive_get_config",
                "drive_create_file",
                "drive_create_files",
                "drive_list_items",
                "drive_read_image",
                "drive_read_pdf",
                "drive_upload_file",
                "grist_import_csv",
                "grist_list_workspaces",
                "local_files_list_items",
                "local_files_create_file",
                "local_files_read_image",
                "local_files_read_pdf",
                "run_python",
            },
        )

    async def test_returns_a_direct_model_answer(self):
        albert = FakeAlbertClient([{"content": "Hello."}])
        agent = OrchestratorAgent(
            albert,
            model="canonical-model-id",
        )

        events = await collect_events(
            agent, [ChatMessage(role="user", content="Hello")]
        )

        self.assertEqual(
            [event.type for event in events],
            ["step_start", "token", "step_complete", "final"],
        )
        self.assertEqual(events[-1].data, {"content": "Hello."})
        self.assertEqual(len(albert.requests), 1)

    @patch("agent.specialists.drive.config.get_drive_config")
    async def test_executes_drive_tool_and_returns_the_follow_up_answer(
        self, get_config
    ):
        get_config.return_value = {"LANGUAGE_CODE": "fr-fr"}
        albert = FakeAlbertClient(
            [
                {
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
                {"content": "Drive uses French."},
            ]
        )
        agent = OrchestratorAgent(
            albert,
            model="canonical-model-id",
            registry=AgentRegistry([DriveConfigAgent("http://drive:8071")]),
        )

        events = await collect_events(
            agent, [ChatMessage(role="user", content="Which language does Drive use?")]
        )

        self.assertEqual(
            [event.type for event in events],
            [
                "step_start",
                "step_complete",
                "tool_call_start",
                "tool_call_result",
                "step_start",
                "token",
                "step_complete",
                "final",
            ],
        )
        self.assertEqual(events[-1].data, {"content": "Drive uses French."})
        tool_message = albert.requests[1]["messages"][-1]
        self.assertEqual(tool_message["role"], "tool")
        self.assertEqual(tool_message["tool_call_id"], "call-1")
        self.assertEqual(json.loads(tool_message["content"]), {"LANGUAGE_CODE": "fr-fr"})
        get_config.assert_called_once_with("http://drive:8071")

    async def test_routes_a_task_to_a_registered_python_agent(self):
        python_agent = FakePythonAgent()
        registry = AgentRegistry([python_agent])
        albert = FakeAlbertClient(
            [
                {
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
                {"content": "I organized the PDFs."},
            ]
        )
        agent = OrchestratorAgent(
            albert,
            model="canonical-model-id",
            registry=registry,
        )

        events = await collect_events(
            agent, [ChatMessage(role="user", content="Organize the PDFs in Downloads")]
        )

        self.assertEqual(events[-1].data, {"content": "I organized the PDFs."})
        self.assertEqual(python_agent.calls[0][0]["working_directory"], "Downloads")
        self.assertEqual(
            json.loads(albert.requests[1]["messages"][-1]["content"]),
            {"status": "completed", "files_changed": 2},
        )
        advertised_names = {
            tool["function"]["name"] for tool in albert.requests[0]["tools"]
        }
        self.assertEqual(advertised_names, {"python_execute"})

    async def test_selects_blocks_before_advertising_detailed_tools(self):
        python_agent = FakePythonAgent()
        blocks = BlockRegistry(
            [
                AgentBlock(
                    name="python",
                    description="Perform Python-based transformations.",
                    agents=(python_agent,),
                    workflows=(
                        WorkflowManifest(
                            name="python.transform",
                            description="Transform supplied data with Python.",
                            capabilities=("python_execute",),
                        ),
                    ),
                )
            ]
        )
        albert = FakeAlbertClient(
            [
                {
                    "tool_calls": [
                        {
                            "id": "select-1",
                            "type": "function",
                            "function": {
                                "name": "select_capability_blocks",
                                "arguments": json.dumps({"blocks": ["python"]}),
                            },
                        }
                    ]
                },
                {"content": "I can handle that."},
            ]
        )
        agent = OrchestratorAgent(
            albert,
            model="canonical-model-id",
            block_registry=blocks,
        )

        events = await collect_events(
            agent, [ChatMessage(role="user", content="Process this data")]
        )

        selection_tools = albert.requests[0]["tools"]
        self.assertEqual(
            selection_tools[0]["function"]["name"],
            "select_capability_blocks",
        )
        detailed_tools = albert.requests[1]["tools"]
        self.assertEqual(
            [tool["function"]["name"] for tool in detailed_tools],
            ["python_execute"],
        )
        self.assertIn(
            "python.transform",
            albert.requests[1]["messages"][0]["content"],
        )
        self.assertEqual(events[-1].data, {"content": "I can handle that."})

    async def test_expands_blocks_after_an_artifact_for_a_cross_block_request(self):
        create_csv = FakeCreateCsvAgent()
        import_csv = FakeGristImportAgent()
        blocks = BlockRegistry(
            [
                AgentBlock(
                    name="local_files",
                    description="Create and access local files.",
                    agents=(create_csv,),
                ),
                AgentBlock(
                    name="grist",
                    description="Import tabular data into Grist.",
                    agents=(import_csv,),
                ),
            ]
        )
        artifact = {
            "kind": "file",
            "location": "local",
            "reference": "exports/sales.csv",
            "media_type": "text/csv",
            "name": "sales.csv",
        }
        albert = FakeAlbertClient(
            [
                {
                    "tool_calls": [
                        {
                            "id": "select-local",
                            "type": "function",
                            "function": {
                                "name": "select_capability_blocks",
                                "arguments": json.dumps(
                                    {"blocks": ["local_files"]}
                                ),
                            },
                        }
                    ]
                },
                {
                    "tool_calls": [
                        {
                            "id": "create-csv",
                            "type": "function",
                            "function": {
                                "name": "local_create_csv",
                                "arguments": json.dumps(
                                    {"path": "exports/sales.csv"}
                                ),
                            },
                        }
                    ]
                },
                {
                    "tool_calls": [
                        {
                            "id": "select-grist",
                            "type": "function",
                            "function": {
                                "name": "select_capability_blocks",
                                "arguments": json.dumps({"blocks": ["grist"]}),
                            },
                        }
                    ]
                },
                {
                    "tool_calls": [
                        {
                            "id": "import-csv",
                            "type": "function",
                            "function": {
                                "name": "grist_import_csv",
                                "arguments": json.dumps({"artifact": artifact}),
                            },
                        }
                    ]
                },
                {
                    "tool_calls": [
                        {
                            "id": "selection-complete",
                            "type": "function",
                            "function": {
                                "name": "select_capability_blocks",
                                "arguments": json.dumps({"blocks": []}),
                            },
                        }
                    ]
                },
                {"content": "I created the CSV and imported it into Grist."},
            ]
        )
        agent = OrchestratorAgent(
            albert,
            model="canonical-model-id",
            block_registry=blocks,
        )

        events = await collect_events(
            agent,
            [
                ChatMessage(
                    role="user",
                    content="Create sales.csv locally and put it into Grist.",
                )
            ],
        )

        self.assertEqual(
            events[-1].data,
            {"content": "I created the CSV and imported it into Grist."},
        )
        self.assertEqual(import_csv.calls, [{"artifact": artifact}])
        first_planning_tools = {
            tool["function"]["name"] for tool in albert.requests[1]["tools"]
        }
        expanded_planning_tools = {
            tool["function"]["name"] for tool in albert.requests[3]["tools"]
        }
        self.assertEqual(first_planning_tools, {"local_create_csv"})
        self.assertEqual(
            expanded_planning_tools,
            {"local_create_csv", "grist_import_csv"},
        )
        self.assertIn(
            '"media_type": "text/csv"',
            albert.requests[2]["messages"][-1]["content"],
        )

    async def test_step_limit_returns_a_partial_answer_instead_of_an_error(self):
        python_agent = FakePythonAgent()
        albert = FakeAlbertClient(
            [
                {
                    "content": None,
                    "tool_calls": [
                        {
                            "id": "call-python",
                            "type": "function",
                            "function": {
                                "name": "python_execute",
                                "arguments": json.dumps(
                                    {"task": "Count images", "working_directory": "."}
                                ),
                            },
                        }
                    ],
                },
                {
                    "content": (
                        "Some folders remain unchecked. Would you like me to focus on "
                        "a specific folder, or show everything I found so far?"
                    ),
                },
            ]
        )
        agent = OrchestratorAgent(
            albert,
            model="canonical-model-id",
            registry=AgentRegistry([python_agent]),
            max_steps=1,
        )

        events = await collect_events(
            agent, [ChatMessage(role="user", content="Count my images")]
        )

        self.assertEqual(events[-1].type, "final")
        self.assertIn("specific folder", events[-1].data["content"])
        self.assertEqual(albert.requests[-1]["tools"], [])


if __name__ == "__main__":
    unittest.main()
