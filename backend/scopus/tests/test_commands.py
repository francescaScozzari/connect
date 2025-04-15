"""Test the Scopus app management commands for importing authors."""

import io
import json
from pathlib import Path

import requests_mock
from django.core.management import call_command
from django.test import TestCase

from scopus.tests import (
    AUTHOR_1_SEARCH_JSON,
    AUTHOR_11111111111_DOCUMENTS_JSON,
    AUTHOR_11111111111_SEARCH_JSON,
    AUTHOR_SEARCH_BASE_URL,
    SCOPUS_SEARCH_BASE_URL,
)


@requests_mock.Mocker()
class ImportAuthorsCommandTests(TestCase):
    """Test the Scopus authors import management command."""

    author_1_id = 1
    author_11111111111_id = 11111111111
    author_1_orcid_id = "n0n3x1st3nt"
    author_11111111111_orcid_id = "1111-1111-1111-111X"

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
            m.get(
                AUTHOR_SEARCH_BASE_URL.format("ORCID", self.author_1_orcid_id),
                json=json.loads(AUTHOR_1_SEARCH_JSON.read_text()),
            )
            m.get(
                AUTHOR_SEARCH_BASE_URL.format("AU-ID", self.author_1_id),
                json=json.loads(AUTHOR_1_SEARCH_JSON.read_text()),
            )
            out = io.StringIO()
            call_command(
                "import_authors",
                ids=[self.author_1_id, self.author_1_orcid_id],
                verbosity=2,
                stdout=out,
            )
            self.assertIn("0 authors successfully processed.", out.getvalue())
            self.assertIn("1 authors unsuccessfully processed (1).", out.getvalue())
        m.get(
            AUTHOR_SEARCH_BASE_URL.format("ORCID", self.author_11111111111_orcid_id),
            json=json.loads(AUTHOR_11111111111_SEARCH_JSON.read_text()),
        )
        m.get(
            AUTHOR_SEARCH_BASE_URL.format("AU-ID", self.author_11111111111_id),
            json=json.loads(AUTHOR_11111111111_SEARCH_JSON.read_text()),
        )
        with self.subTest("Create objects"):
            out = io.StringIO()
            call_command(
                "import_authors",
                ids=[self.author_11111111111_id, self.author_11111111111_orcid_id],
                verbosity=2,
                stdout=out,
            )
            self.assertIn("1 author ids about to be processed.", out.getvalue())
            self.assertIn("1 authors successfully processed.", out.getvalue())
        author_path = Path("scopus/tests/data/11111111111.txt")
        with self.subTest("Update objects"):
            out = io.StringIO()
            call_command(
                "import_authors",
                author_paths=[author_path],
                verbosity=2,
                stdout=out,
            )
            self.assertIn("1 authors successfully processed.", out.getvalue())
        with self.subTest("Update objects"):
            out = io.StringIO()
            call_command(
                "import_authors",
                ids=[self.author_11111111111_id, self.author_11111111111_orcid_id],
                verbosity=2,
                stdout=out,
            )
            self.assertIn("1 authors successfully processed.", out.getvalue())
        with self.subTest("Duplicated objects"):
            out = io.StringIO()
            call_command(
                "import_authors",
                ids=[self.author_11111111111_id, self.author_11111111111_id],
                verbosity=2,
                stdout=out,
            )
            self.assertIn("Duplicate author ids: 11111111111.", out.getvalue())
            self.assertIn("1 authors successfully processed.", out.getvalue())
        m.get(
            SCOPUS_SEARCH_BASE_URL.format("AU-ID", self.author_11111111111_id),
            json=json.loads(AUTHOR_11111111111_DOCUMENTS_JSON.read_text()),
        )
        with self.subTest("Populate documents"):
            out = io.StringIO()
            call_command(
                "import_authors",
                ids=[self.author_11111111111_id],
                populate_documents=True,
                verbosity=2,
                stdout=out,
            )
            self.assertIn("1 authors successfully processed.", out.getvalue())
            self.assertIn(
                "4 documents successfully processed.",
                out.getvalue(),
            )
