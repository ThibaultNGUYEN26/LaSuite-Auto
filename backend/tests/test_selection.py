import json
import unittest
from copy import deepcopy
from typing import Any

from agent.base import DelegationContext, SpecialistAgent
from agent.blocks import AgentBlock, BlockRegistry
from agent.selection import select_blocks
from schemas import ChatMessage


class ExampleAgent(SpecialistAgent):
    description = "Example capability."
    parameters = {"type": "object", "properties": {}}

    def __init__(self, name: str):
        self.name = name

    def execute(self, arguments: dict, context: DelegationContext) -> dict:
        return {"status": "ok"}


class FakeSelectionClient:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.requests = []

    async def chat_completion_stream(self, **request):
        self.requests.append(deepcopy(request))
        response = next(self.responses)
        if response.get("content"):
            yield {"type": "content", "delta": response["content"]}
        yield {"type": "done", "tool_calls": response.get("tool_calls") or []}


def selection_call(names: Any) -> dict:
    return {
        "id": "selection",
        "type": "function",
        "function": {
            "name": "select_capability_blocks",
            "arguments": json.dumps({"blocks": names}),
        },
    }


class BlockSelectionTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.blocks = BlockRegistry(
            [
                AgentBlock(
                    name="local_files",
                    description="Discover local datasets.",
                    agents=(ExampleAgent("list_local"),),
                ),
                AgentBlock(
                    name="data_analysis",
                    description="Analyze trends and evolution in tabular data.",
                    agents=(ExampleAgent("analyze_data"),),
                ),
            ]
        )

    async def test_accepts_text_json_when_model_ignores_forced_tool_call(self):
        client = FakeSelectionClient(
            [{"content": '{"blocks":["local_files","data_analysis"]}'}]
        )

        selected = await select_blocks(
            client,
            model="model",
            conversation=[
                ChatMessage(
                    role="user",
                    content="Dis-moi l'évolution de la surface pastorale.",
                )
            ],
            blocks=self.blocks,
        )

        self.assertEqual(selected, ("local_files", "data_analysis"))
        self.assertEqual(len(client.requests), 1)

    async def test_accepts_a_bare_string_for_one_block(self):
        client = FakeSelectionClient(
            [{"tool_calls": [selection_call("data_analysis")]}]
        )

        selected = await select_blocks(
            client,
            model="model",
            conversation=[ChatMessage(role="user", content="Show the trend")],
            blocks=self.blocks,
        )

        self.assertEqual(selected, ("data_analysis",))

    async def test_retries_as_plain_json_when_tool_selection_is_missing(self):
        client = FakeSelectionClient(
            [
                {},
                {"content": '{"blocks":["local_files","data_analysis"]}'},
            ]
        )

        selected = await select_blocks(
            client,
            model="model",
            conversation=[ChatMessage(role="user", content="Analyze my local CSV")],
            blocks=self.blocks,
        )

        self.assertEqual(selected, ("local_files", "data_analysis"))
        self.assertEqual(client.requests[1]["tools"], [])
        self.assertIn(
            "intended outcome in any language",
            client.requests[0]["messages"][0]["content"],
        )

    async def test_missing_selection_no_longer_raises_backend_error(self):
        client = FakeSelectionClient([{}, {}])

        selected = await select_blocks(
            client,
            model="model",
            conversation=[ChatMessage(role="user", content="Help me")],
            blocks=self.blocks,
        )

        self.assertEqual(selected, ())

    async def test_still_prefers_a_valid_tool_call(self):
        client = FakeSelectionClient(
            [{"tool_calls": [selection_call(["data_analysis"])]}]
        )

        selected = await select_blocks(
            client,
            model="model",
            conversation=[ChatMessage(role="user", content="Show the trend")],
            blocks=self.blocks,
        )

        self.assertEqual(selected, ("data_analysis",))


if __name__ == "__main__":
    unittest.main()
