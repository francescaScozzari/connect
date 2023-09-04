"""Test the scopus app management commands for importing authors."""

import io
import json
from pathlib import Path

import requests_mock
from django.core.management import call_command
from django.test import TestCase

from scopus.tests import (
    AUTHOR_11111111111_DOCUMENTS_JSON,
    AUTHOR_11111111111_JSON,
    AUTHOR_BASE_URL,
    SEARCH_AUTHOR_11111111111_URL,
)


@requests_mock.Mocker()
class ImportAuthorsCommandTests(TestCase):
    """Test the Scopus authors import management command."""

    def test_command(self, m):
        """Test importing authors from Scopus."""
        with self.subTest("No authors"):
            out = io.StringIO()
            call_command(
                "import_authors",
                verbosity=2,
                stdout=out,
            )
            self.assertIn("No author ids.", out.getvalue())
        with self.subTest("Resource not found"):
            author_id = 1
            m.get(
                f"{AUTHOR_BASE_URL}/{author_id}",
                status_code=404,
                json={
                    "service-error": {
                        "status": {
                            "statusCode": "RESOURCE_NOT_FOUND",
                            "statusText": "The resource specified cannot be found.",
                        }
                    }
                },
            )
            out = io.StringIO()
            call_command(
                "import_authors",
                author_ids=[author_id],
                verbosity=2,
                stdout=out,
            )
            self.assertIn("0 authors successfully processed.", out.getvalue())
            self.assertIn("1 authors unsuccessfully processed [1].", out.getvalue())
        author_id = 11111111111
        m.get(
            f"{AUTHOR_BASE_URL}/{author_id}",
            json={
                "author-retrieval-response": [
                    json.loads(AUTHOR_11111111111_JSON.read_text())
                ]
            },
        )
        with self.subTest("Create objects"):
            out = io.StringIO()
            call_command(
                "import_authors",
                author_ids=[author_id],
                verbosity=2,
                stdout=out,
            )
            self.assertIn("1 author ids are about to be processed.", out.getvalue())
            self.assertIn("1 authors successfully processed.", out.getvalue())
        author_path = Path("scopus/tests/data/11111111111.txt")
        m.get(
            f"{AUTHOR_BASE_URL}/{author_id}",
            json={
                "author-retrieval-response": [
                    json.loads(AUTHOR_11111111111_JSON.read_text())
                ]
            },
        )
        with self.subTest("Update objects"):
            out = io.StringIO()
            call_command(
                "import_authors",
                author_paths=[author_path],
                verbosity=2,
                stdout=out,
            )
            self.assertIn("1 authors successfully processed.", out.getvalue())
        author_id = 11111111111
        m.get(
            f"{AUTHOR_BASE_URL}/{author_id}",
            json={
                "author-retrieval-response": [
                    json.loads(AUTHOR_11111111111_JSON.read_text())
                ]
            },
        )
        with self.subTest("Update objects"):
            out = io.StringIO()
            call_command(
                "import_authors",
                author_ids=[author_id],
                verbosity=2,
                stdout=out,
            )
            self.assertIn("1 authors successfully processed.", out.getvalue())
        author_id = 11111111111
        m.get(
            f"{AUTHOR_BASE_URL}/{author_id}",
            json={
                "author-retrieval-response": [
                    json.loads(AUTHOR_11111111111_JSON.read_text())
                ]
            },
        )
        with self.subTest("Duplicated objects"):
            out = io.StringIO()
            call_command(
                "import_authors",
                author_ids=[author_id, author_id],
                verbosity=2,
                stdout=out,
            )
            self.assertIn("Duplicate author ids: 11111111111.", out.getvalue())
            self.assertIn("1 authors successfully processed.", out.getvalue())
        author_id = 11111111111
        m.get(
            f"{AUTHOR_BASE_URL}/{author_id}",
            json={
                "author-retrieval-response": [
                    json.loads(AUTHOR_11111111111_JSON.read_text())
                ]
            },
        )
        m.get(
            SEARCH_AUTHOR_11111111111_URL,
            json=json.loads(AUTHOR_11111111111_DOCUMENTS_JSON.read_text()),
        )
        with self.subTest("Populate documents"):
            out = io.StringIO()
            call_command(
                "import_authors",
                author_ids=[author_id],
                populate_documents=True,
                verbosity=2,
                stdout=out,
            )
            self.assertIn("1 authors successfully processed.", out.getvalue())
            self.assertIn(
                "4 documents successfully processed.",
                out.getvalue(),
            )
