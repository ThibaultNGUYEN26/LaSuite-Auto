import unittest

from providers.albert import AlbertClient, _chat_completion_payload


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


class AlbertConnectionPoolTests(unittest.IsolatedAsyncioTestCase):
    async def test_reuses_and_closes_persistent_async_client(self):
        provider = AlbertClient("test-key", base_url="https://albert.example/v1")

        first = provider._get_async_client()
        second = provider._get_async_client()

        self.assertIs(first, second)
        self.assertFalse(first.is_closed)

        await provider.aclose()

        self.assertTrue(first.is_closed)


if __name__ == "__main__":
    unittest.main()
