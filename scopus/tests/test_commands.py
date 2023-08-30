"""Test the scopus app management commands for importing authors."""

import io
import json

import requests_mock
from django.core.management import call_command
from django.test import TestCase

from scopus.tests import AUTHOR_11111111111_JSON, AUTHOR_BASE_URL


class ImportAuthorsCommandTests(TestCase):
    """Test the Scopus authors import management command."""

    def test_command_fail(self):
        """Test importing authors from Scopus."""
        with requests_mock.Mocker() as m:
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
