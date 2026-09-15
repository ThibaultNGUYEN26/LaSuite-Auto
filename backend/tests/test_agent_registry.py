import unittest

from agent.base import DelegationContext, SpecialistAgent
from agent.registry import AgentRegistry


class StubAgent(SpecialistAgent):
    name = "stub"
    description = "Test specialist"
    parameters = {"type": "object", "properties": {}}

    def execute(self, arguments, context):
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


if __name__ == "__main__":
    unittest.main()
