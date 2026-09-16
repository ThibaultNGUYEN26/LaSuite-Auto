import json
import unittest

from agent.blocks import AgentBlock, BlockRegistry, CapabilityManifest
from agent.selection import select_blocks
from schemas import ChatMessage
from tests.test_orchestrator import FakeAlbertClient, FakePythonAgent


def _registry() -> BlockRegistry:
    block = AgentBlock(
        name="code",
        description="Execute bounded Python tasks.",
        agents=(FakePythonAgent(),),
        capabilities=(
            CapabilityManifest(name="python_execute", description="Run Python."),
        ),
    )
    return BlockRegistry([block])


async def _select(tool_calls):
    client = FakeAlbertClient([{"tool_calls": tool_calls}])
    return await select_blocks(
        client,
        model="fake-model",
        conversation=[ChatMessage(role="user", content="do something")],
        blocks=_registry(),
    )


def _call(arguments: str, name: str = "select_capability_blocks"):
    return [{"function": {"name": name, "arguments": arguments}}]


class SelectBlocksTests(unittest.IsolatedAsyncioTestCase):
    async def test_accepts_a_normal_list_selection(self):
        result = await _select(_call(json.dumps({"blocks": ["code"]})))
        self.assertEqual(result, ("code",))

    async def test_accepts_a_bare_string_instead_of_a_single_item_list(self):
        result = await _select(_call(json.dumps({"blocks": "code"})))
        self.assertEqual(result, ("code",))

    async def test_explicit_empty_list_means_no_blocks_needed(self):
        result = await _select(_call(json.dumps({"blocks": []})))
        self.assertEqual(result, ())

    async def test_drops_unknown_block_names_and_keeps_valid_ones(self):
        result = await _select(
            _call(json.dumps({"blocks": ["code", "not-a-real-block"]}))
        )
        self.assertEqual(result, ("code",))

    async def test_fails_open_when_only_unknown_blocks_are_returned(self):
        result = await _select(_call(json.dumps({"blocks": ["not-a-real-block"]})))
        self.assertEqual(result, ("code",))

    async def test_fails_open_on_invalid_json(self):
        result = await _select(_call("not json"))
        self.assertEqual(result, ("code",))

    async def test_fails_open_when_the_model_calls_the_wrong_function(self):
        result = await _select(
            _call(json.dumps({"task": "x"}), name="python_execute")
        )
        self.assertEqual(result, ("code",))

    async def test_fails_open_when_no_tool_call_is_returned(self):
        result = await _select([])
        self.assertEqual(result, ("code",))


if __name__ == "__main__":
    unittest.main()
