"""Test the xai app management commands."""

import io

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase

from connect.qdrant import cli as qdrant_cli
from connect.tests.utils import SetUpQdrantMixin, XaiDataMixin
from xai.models import TokensEmbeddings


class LoadDocumentsCommandTests(SetUpQdrantMixin, XaiDataMixin, TestCase):
    """Test the xai load documents management command."""

    def test_command(self):
        """Test load_documents command."""
        out = io.StringIO()
        call_command(
            "load_documents",
            verbosity=2,
            stdout=out,
        )
        self.assertIn("Start loading 3 documents to qdrant.", out.getvalue())
        self.assertIn(
            "TokensEmbeddings for document 99.9999/999-9-999-99999-1_11 "
            "generated successfully.",
            out.getvalue(),
        )
        self.assertIn(
            "Point for document 99.9999/999-9-999-99999-1_11 generated successfully.",
            out.getvalue(),
        )
        self.assertIn(
            "Point 1 loaded successfully.",
            out.getvalue(),
        )
        self.assertIn("3 points loaded successfully.", out.getvalue())
        self.assertEqual(TokensEmbeddings.objects.count(), 3)
        self.assertEqual(
            qdrant_cli.count(
                collection_name=settings.QDRANT_DOCUMENTS_COLLECTION
            ).count,
            3,
        )
