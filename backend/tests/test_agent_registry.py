import unittest

from agent.base import DelegationContext, SpecialistAgent
from agent.registry import AgentRegistry


class StubAgent(SpecialistAgent):
    name = "stub"
    description = "Test specialist"
    parameters = {"type": "object", "properties": {}}

    def execute(self, arguments, context):
        return {"arguments": arguments, "conversation_size": len(context.conversation)}


class AsyncStubAgent(SpecialistAgent):
    name = "async_stub"
    description = "Asynchronous test specialist"
    parameters = {"type": "object", "properties": {}}

    async def execute(self, arguments, context):
        return {"arguments": arguments, "conversation_size": len(context.conversation)}


class AgentRegistryTests(unittest.TestCase):
    def setUp(self):
        self.agent = StubAgent()
        self.registry = AgentRegistry([self.agent])
        self.context = DelegationContext(conversation=())

    def test_dispatches_json_arguments(self):
        self.assertEqual(
            self.registry.dispatch("stub", '{"value": 3}', self.context),
            {"arguments": {"value": 3}, "conversation_size": 0},
        )

    def test_returns_structured_errors_for_bad_calls(self):
        self.assertEqual(
            self.registry.dispatch("missing", "{}", self.context),
            {"error": "Unknown specialist agent: missing"},
        )
        self.assertIn(
            "error", self.registry.dispatch("stub", "not-json", self.context)
        )

    def test_rejects_duplicate_names(self):
        with self.assertRaisesRegex(ValueError, "already registered"):
            self.registry.register(StubAgent())

    def test_sync_dispatch_explains_when_a_specialist_is_async(self):
        registry = AgentRegistry([AsyncStubAgent()])

        result = registry.dispatch(
            "async_stub", "{}", DelegationContext(conversation=())
        )

        self.assertIn("use async dispatch", result["error"])


class AsyncAgentRegistryTests(unittest.IsolatedAsyncioTestCase):
    async def test_dispatches_an_async_specialist(self):
        registry = AgentRegistry([AsyncStubAgent()])

        result = await registry.dispatch_async(
            "async_stub",
            '{"value": 4}',
            DelegationContext(conversation=()),
        )

        self.assertEqual(result, {"arguments": {"value": 4}, "conversation_size": 0})


if __name__ == "__main__":
    unittest.main()
