import inspect
import unittest
from unittest.mock import patch

from agent import orchestrator
from agent.base import DelegationContext, SpecialistAgent
from agent.blocks import (
    AgentBlock,
    BlockLoadError,
    BlockRegistry,
    CapabilityManifest,
    build_agent_registry,
    discover_builtin_blocks,
    discover_external_blocks,
)


class ExampleAgent(SpecialistAgent):
    name = "example_action"
    description = "Perform an example action."
    parameters = {"type": "object", "properties": {}}

    def execute(self, arguments: dict, context: DelegationContext) -> dict:
        return {"status": "ok"}


class FakeEntryPoint:
    name = "example-package"

    def load(self):
        return lambda: AgentBlock(name="external", agents=(ExampleAgent(),))


class FakeEntryPoints(list):
    def select(self, *, group: str):
        return self if group == "lasuite_automations.blocks" else []


class BlockDiscoveryTests(unittest.TestCase):
    def test_discovers_each_builtin_domain_as_a_block(self):
        blocks = discover_builtin_blocks()

        self.assertEqual(
            {block.name for block in blocks},
            {"code", "drive", "grist", "local_files", "pdf"},
        )
        drive = next(block for block in blocks if block.name == "drive")
        upload = next(
            capability
            for capability in drive.capability_catalog()
            if capability.name == "drive_upload_file"
        )
        self.assertEqual(upload.side_effect, "external_write")
        self.assertIn("drive.write", upload.permissions)
        self.assertEqual(upload.accepts[0].kind, "file")

    def test_registry_accepts_a_new_block_without_orchestrator_changes(self):
        block = AgentBlock(name="example", agents=(ExampleAgent(),))

        registry = build_agent_registry([block])

        self.assertEqual(
            registry.tool_definitions()[0]["function"]["name"],
            "example_action",
        )

    def test_permission_policy_rejects_a_block_before_advertising_it(self):
        block = AgentBlock(
            name="example",
            agents=(ExampleAgent(),),
            permissions=("remote.write",),
            capabilities=(
                CapabilityManifest(
                    name="example_action",
                    description="Perform an example action.",
                    side_effect="external_write",
                    permissions=("remote.write",),
                ),
            ),
        )
        registry = BlockRegistry(
            [block],
            allowed_permissions=("remote.read",),
        )

        with self.assertRaisesRegex(BlockLoadError, "remote.write"):
            registry.agent_registry(["example"])

    @patch("agent.blocks.metadata.entry_points")
    def test_discovers_an_installed_external_block(self, entry_points):
        entry_points.return_value = FakeEntryPoints([FakeEntryPoint()])

        blocks = discover_external_blocks()

        self.assertEqual([block.name for block in blocks], ["external"])
        self.assertEqual(blocks[0].agents[0].name, "example_action")

    def test_orchestrator_has_no_domain_or_specialist_coupling(self):
        source = inspect.getsource(orchestrator).lower()

        self.assertNotIn("agent.specialists", source)
        self.assertNotIn("drive", source)
        self.assertNotIn("grist", source)
        self.assertNotIn("local_files", source)


if __name__ == "__main__":
    unittest.main()
