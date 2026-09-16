import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from agent.base import DelegationContext
from agent.errors import GristAPIError
from agent.specialists.grist import GristImportCsvAgent
from services.grist import import_csv_document, list_grist_workspaces


class FakeResponse(io.BytesIO):
    def __init__(self, payload):
        super().__init__(json.dumps(payload).encode("utf-8"))
        self.headers = {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


class GristServiceTests(unittest.TestCase):
    @patch("services.grist.urlopen")
    def test_lists_workspaces_with_bearer_authentication(self, urlopen):
        urlopen.return_value = FakeResponse(
            [
                {
                    "id": 12,
                    "name": "Data",
                    "access": "owners",
                    "docs": [{"id": "doc-1", "name": "Existing", "urlId": None}],
                }
            ]
        )

        result = list_grist_workspaces(
            "http://grist:8484", "secret-key", org_id="docs"
        )

        request = urlopen.call_args.args[0]
        self.assertEqual(request.full_url, "http://grist:8484/api/orgs/docs/workspaces")
        self.assertEqual(request.get_header("Authorization"), "Bearer secret-key")
        self.assertEqual(result["workspaces"][0]["id"], 12)
        self.assertEqual(result["workspaces"][0]["documents"][0]["name"], "Existing")

    @patch("services.grist.urlopen")
    def test_imports_csv_as_a_saved_document(self, urlopen):
        urlopen.return_value = FakeResponse({"id": "new-document"})

        result = import_csv_document(
            "http://grist:8484",
            "secret-key",
            workspace_id=12,
            document_name="Quarterly sales",
            filename="Quarterly_sales.csv",
            csv_data=b"name,total\nAlice,12\n",
            org_id="docs",
        )

        request = urlopen.call_args.args[0]
        self.assertEqual(request.full_url, "http://grist:8484/api/docs")
        self.assertEqual(request.get_method(), "POST")
        self.assertEqual(request.get_header("Authorization"), "Bearer secret-key")
        self.assertIn("multipart/form-data; boundary=", request.get_header("Content-type"))
        self.assertIn(b'name="workspaceId"', request.data)
        self.assertIn(b"\r\n12\r\n", request.data)
        self.assertIn(b'name="documentName"', request.data)
        self.assertIn(b'name="upload"; filename="Quarterly_sales.csv"', request.data)
        self.assertIn(b"name,total\nAlice,12\n", request.data)
        self.assertEqual(result["status"], "imported")
        self.assertEqual(result["document_id"], "new-document")
        self.assertEqual(
            result["document_url"],
            "http://grist:8484/o/docs/doc/new-document",
        )

    def test_requires_api_key_before_network_access(self):
        with self.assertRaisesRegex(GristAPIError, "GRIST_API_KEY"):
            list_grist_workspaces("http://grist:8484", "", org_id="docs")


class GristImportCsvAgentTests(unittest.TestCase):
    def _agent(self, root: Path, *, workspace_id: int | None = 12):
        return GristImportCsvAgent(
            "http://grist:8484",
            "secret-key",
            org_id="docs",
            workspace_id=workspace_id,
            local_files_root=root,
            drive_base_url="http://drive:8071",
            drive_session_id="drive-session",
            max_import_bytes=1000,
        )

    @patch("agent.specialists.grist.import_csv.import_csv_document")
    def test_imports_csv_content_and_returns_shape(self, import_document):
        import_document.return_value = {
            "status": "imported",
            "document_id": "doc-1",
        }
        agent = self._agent(Path("."))

        result = agent.execute(
            {
                "source_type": "content",
                "source": "name,total\nAlice,12\nBob,7\n",
                "document_name": "Sales report",
            },
            DelegationContext(conversation=()),
        )

        self.assertEqual(result["data_rows"], 2)
        self.assertEqual(result["columns"], 2)
        self.assertEqual(import_document.call_args.kwargs["workspace_id"], 12)
        self.assertEqual(
            import_document.call_args.kwargs["filename"], "Sales_report.csv"
        )

    @patch("agent.specialists.grist.import_csv.import_csv_document")
    def test_reads_existing_local_csv(self, import_document):
        import_document.return_value = {"status": "imported", "document_id": "doc-2"}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "people.csv").write_bytes(b"name,city\nAlice,Paris\n")
            agent = self._agent(root)

            result = agent.execute(
                {
                    "source_type": "local",
                    "source": "people.csv",
                    "document_name": "People",
                },
                DelegationContext(conversation=()),
            )

        self.assertEqual(result["source_type"], "local")
        self.assertEqual(
            import_document.call_args.kwargs["csv_data"],
            b"name,city\nAlice,Paris\n",
        )

    def test_requires_a_workspace_destination(self):
        agent = self._agent(Path("."), workspace_id=None)
        with self.assertRaisesRegex(GristAPIError, "Choose a Grist workspace"):
            agent.execute(
                {
                    "source_type": "content",
                    "source": "name\nAlice\n",
                    "document_name": "People",
                },
                DelegationContext(conversation=()),
            )


if __name__ == "__main__":
    unittest.main()
