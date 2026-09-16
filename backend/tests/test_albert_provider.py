import unittest

from providers.albert import _chat_completion_payload


class AlbertChatPayloadTests(unittest.TestCase):
    def test_omits_tools_and_tool_choice_when_no_tools_are_available(self):
        payload = _chat_completion_payload(
            model="text-model",
            messages=[{"role": "user", "content": "Hello"}],
            tools=[],
            tool_choice="auto",
        )

        self.assertNotIn("tools", payload)
        self.assertNotIn("tool_choice", payload)

    def test_includes_tools_and_tool_choice_when_tools_are_available(self):
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "example",
                    "description": "Example",
                    "parameters": {"type": "object", "properties": {}},
                },
            }
        ]

        payload = _chat_completion_payload(
            model="text-model",
            messages=[{"role": "user", "content": "Use the example"}],
            tools=tools,
            tool_choice="auto",
        )

        self.assertEqual(payload["tools"], tools)
        self.assertEqual(payload["tool_choice"], "auto")


if __name__ == "__main__":
    unittest.main()
