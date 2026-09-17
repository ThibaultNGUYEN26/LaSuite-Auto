import json
import unittest
from copy import deepcopy
from unittest.mock import patch

from agent.base import DelegationContext, SpecialistAgent
from agent.blocks import (
    AgentBlock,
    ArtifactContract,
    CapabilityManifest,
    BlockRegistry,
    WorkflowManifest,
    build_agent_registry,
)
from agent.orchestrator import (
    OrchestratorAgent,
    _append_resource_links,
    _has_completed_required_outcome,
    _is_capability_catalog_request,
    _partial_result_fallback,
    _requests_corpus_document_analysis,
    _render_capability_catalog,
)
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


class FakeCorpusAnalysisAgent(SpecialistAgent):
    name = "example_analyze_folder"
    description = "Analyze every document in a folder as one bounded corpus."
    parameters = {
        "type": "object",
        "properties": {"directory": {"type": "string"}},
        "required": ["directory"],
        "additionalProperties": False,
    }

    def __init__(self):
        self.calls = []

    def execute(self, arguments: dict, context: DelegationContext) -> dict:
        self.calls.append(arguments)
        return {
            "status": "analyzed",
            "document_count": 16,
            "pdf_memories": {
                "requested": 10,
                "created": 10,
                "updated": 0,
                "skipped": 0,
                "failed": 0,
                "limited": False,
            },
        }


async def collect_events(agent, conversation):
    events = []
    async for event in agent.run_stream(conversation):
        events.append(event)
    return events


class OrchestratorAgentTests(unittest.IsolatedAsyncioTestCase):
    def test_required_corpus_outcome_rejects_incomplete_pdf_preparation(self):
        capabilities = ("example_analyze_folder",)
        self.assertFalse(
            _has_completed_required_outcome(
                [
                    {
                        "capability": "example_analyze_folder",
                        "result": {
                            "status": "analyzed",
                            "pdf_memories": {
                                "requested": 10,
                                "created": 1,
                                "updated": 0,
                                "skipped": 0,
                                "failed": 9,
                                "limited": False,
                            },
                        },
                    }
                ],
                capabilities,
            )
        )
        self.assertTrue(
            _has_completed_required_outcome(
                [
                    {
                        "capability": "example_analyze_folder",
                        "result": {
                            "status": "analyzed",
                            "pdf_memories": {
                                "requested": 10,
                                "created": 9,
                                "updated": 0,
                                "skipped": 1,
                                "failed": 0,
                                "limited": False,
                            },
                        },
                    }
                ],
                capabilities,
            )
        )

    def test_recognizes_natural_corpus_analysis_without_audit(self):
        self.assertTrue(
            _requests_corpus_document_analysis(
                [
                    ChatMessage(
                        role="user",
                        content=(
                            "Analyze the complete checklist and all documents from "
                            "the first client. Summarize them separately and do not "
                            "compare them or perform a compliance audit yet."
                        ),
                    )
                ]
            )
        )
        self.assertFalse(
            _requests_corpus_document_analysis(
                [
                    ChatMessage(
                        role="user",
                        content="Audit all documents from the first client.",
                    )
                ]
            )
        )

    async def test_corpus_analysis_cannot_finalize_before_bounded_capability(self):
        corpus_agent = FakeCorpusAnalysisAgent()
        blocks = BlockRegistry(
            [
                AgentBlock(
                    name="documents",
                    description="Analyze document collections.",
                    agents=(corpus_agent,),
                    capabilities=(
                        CapabilityManifest(
                            name=corpus_agent.name,
                            description=corpus_agent.description,
                            produces=(ArtifactContract("document_analysis"),),
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
                            "id": "select-documents",
                            "type": "function",
                            "function": {
                                "name": "select_capability_blocks",
                                "arguments": json.dumps({"blocks": ["documents"]}),
                            },
                        }
                    ]
                },
                {"content": "Here is a summary based on individual reads."},
                {
                    "tool_calls": [
                        {
                            "id": "analyze-corpus",
                            "type": "function",
                            "function": {
                                "name": corpus_agent.name,
                                "arguments": json.dumps({"directory": "AUTO/Client"}),
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
                {"content": "All client documents were analyzed separately."},
            ]
        )
        agent = OrchestratorAgent(
            albert,
            model="canonical-model-id",
            block_registry=blocks,
            max_steps=4,
        )

        events = await collect_events(
            agent,
            [
                ChatMessage(
                    role="user",
                    content="Analyze all documents from the first client folder.",
                )
            ],
        )

        self.assertEqual(corpus_agent.calls, [{"directory": "AUTO/Client"}])
        self.assertEqual(
            events[-1].data["content"],
            "All client documents were analyzed separately.",
        )
        self.assertIn(
            "document_analysis outcome",
            albert.requests[1]["messages"][0]["content"],
        )

    def test_recognizes_capability_catalog_requests(self):
        self.assertTrue(
            _is_capability_catalog_request(
                [ChatMessage(role="user", content="List every tool we have")]
            )
        )
        self.assertFalse(
            _is_capability_catalog_request(
                [ChatMessage(role="user", content="Create a CSV file")]
            )
        )

    async def test_catalog_request_uses_live_registry_without_calling_model(self):
        python_agent = FakePythonAgent()
        blocks = BlockRegistry(
            [
                AgentBlock(
                    name="python",
                    description="Perform Python-based transformations.",
                    agents=(python_agent,),
                )
            ]
        )
        albert = FakeAlbertClient([])
        agent = OrchestratorAgent(
            albert,
            model="canonical-model-id",
            block_registry=blocks,
        )

        events = await collect_events(
            agent,
            [ChatMessage(role="user", content="Show every available tool")],
        )

        content = events[-1].data["content"]
        self.assertIn("## python", content)
        self.assertIn("`python_execute`", content)
        self.assertIn('"working_directory"', content)
        self.assertEqual(albert.requests, [])

    def test_detailed_catalog_includes_exact_policy_and_schema(self):
        python_agent = FakePythonAgent()
        blocks = BlockRegistry(
            [
                AgentBlock(
                    name="python",
                    description="Perform transformations.",
                    agents=(python_agent,),
                )
            ]
        )

        rendered = _render_capability_catalog(blocks)

        self.assertIn("Side effect: `none`", rendered)
        self.assertIn('"required": [', rendered)
        self.assertIn('"task"', rendered)

    def test_partial_fallback_preserves_completed_audit_outputs(self):
        content = _partial_result_fallback(
            [
                {
                    "capability": "example_audit",
                    "result": {
                        "status": "audited",
                        "client_directory": "Clients/Valdorne",
                        "criteria_count": 40,
                        "source_count": 15,
                        "complete": True,
                        "audit_csv": {
                            "relative_path": "Reports/Valdorne_matrix.csv"
                        },
                    },
                }
            ]
        )

        self.assertIn("40 criteria", content)
        self.assertIn("15 evidence files", content)
        self.assertIn("`Reports/Valdorne_matrix.csv`", content)

    def test_appends_verified_drive_and_grist_links(self):
        content = _append_resource_links(
            "The report and matrix were created.",
            [
                {
                    "capability": "drive_upload_file",
                    "result": {
                        "url_permalink": "http://drive/explorer/items/report-id"
                    },
                },
                {
                    "capability": "grist_import_csv",
                    "result": {
                        "document_url": "http://grist/o/docs/doc/audit-id",
                        "artifact": {
                            "metadata": {
                                "url": "http://grist/o/docs/doc/audit-id"
                            }
                        },
                    },
                },
            ],
        )

        self.assertIn(
            "[Open the uploaded report]"
            "(http://drive/explorer/items/report-id)",
            content,
        )
        self.assertIn(
            "[Open the imported audit matrix]"
            "(http://grist/o/docs/doc/audit-id)",
            content,
        )
        self.assertEqual(content.count("http://grist/o/docs/doc/audit-id"), 1)

    def test_runtime_registry_advertises_discovered_capabilities(self):
        names = {
            tool["function"]["name"]
            for tool in build_agent_registry().tool_definitions()
        }
        self.assertEqual(
            names,
            {
                "drive_get_config",
                "drive_create_folder",
                "drive_create_file",
                "drive_create_files",
                "drive_download_folder",
                "drive_list_items",
                "drive_read_image",
                "drive_read_pdf",
                "drive_search_pdfs",
                "drive_read_text",
                "drive_rename_file",
                "drive_upload_file",
                "data_analyze_table",
                "grist_import_csv",
                "grist_list_workspaces",
                "local_files_list_items",
                "local_files_create_file",
                "local_files_create_folder",
                "local_files_analyze_folder",
                "local_files_audit_folder",
                "local_files_audit_pdf",
                "local_files_compare_pdfs",
                "local_files_read_image",
                "local_files_read_pdf",
                "local_files_search_pdfs",
                "local_files_search_pdf_memory",
                "local_files_summarize_pdf",
                "local_files_summarize_pdfs",
                "local_files_read_text",
                "local_files_rename_file",
                "run_python",
                "pdf_create",
                "pdf_apply_template",
                "pdf_render_analysis",
                "pdf_render_audit",
                "pdf_run_script",
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
        self.assertIn(
            "Treat the extracted document text as the source of truth",
            albert.requests[0]["messages"][0]["content"],
        )
        self.assertIn(
            "pass the returned CSV artifact directly to a compatible",
            albert.requests[0]["messages"][0]["content"],
        )
        self.assertIn(
            "include it as a clickable Markdown link",
            albert.requests[0]["messages"][0]["content"],
        )

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
