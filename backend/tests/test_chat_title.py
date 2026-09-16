import unittest
from copy import deepcopy

from services.chat_title import fallback_title, generate_title, normalize_title


class FakeTitleClient:
    def __init__(self, content: str):
        self.content = content
        self.requests = []

    async def chat_completion_stream(self, **request):
        self.requests.append(deepcopy(request))
        yield {"type": "content", "delta": self.content}
        yield {"type": "done", "tool_calls": []}


class ChatTitleTests(unittest.IsolatedAsyncioTestCase):
    async def test_generates_a_short_normalized_title(self):
        client = FakeTitleClient('Titre: "Évolution de la surface pastorale."')

        title = await generate_title(
            "Dis-moi l'évolution de la surface pastorale",
            "La surface augmente jusqu'en 2020.",
            albert=client,
            model="text-model",
        )

        self.assertEqual(title, "Évolution de la surface pastorale")
        self.assertEqual(client.requests[0]["tools"], [])
        self.assertIn("surface pastorale", client.requests[0]["messages"][1]["content"])

    def test_fallback_uses_one_short_line_from_the_prompt(self):
        title = fallback_title(
            "Create a detailed quarterly sales report for every regional office"
        )

        self.assertLessEqual(len(title), 60)
        self.assertEqual(
            title, "Create a detailed quarterly sales report for every regional"
        )

    def test_normalization_uses_prompt_when_output_is_empty(self):
        self.assertEqual(
            normalize_title("\n", fallback_prompt="Rename my CSV\nIgnore this"),
            "Rename my CSV",
        )


if __name__ == "__main__":
    unittest.main()
