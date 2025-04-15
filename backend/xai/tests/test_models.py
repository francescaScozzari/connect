"""Test xai app models."""

from django.test import TestCase

from scopus.models import ScopusDocument
from xai.models import TokensEmbeddings


class TokenEmbeddingsTest(TestCase):
    """Test the TokenEmbeddings model."""

    @classmethod
    def setUpTestData(cls):
        """Prepare initial data for testing."""
        cls.tokens_embeddings1 = TokensEmbeddings(
            pk=1, document=ScopusDocument(doi="99.9999/999-9-999-99999-1_11")
        )
        cls.tokens_embeddings2 = TokensEmbeddings(
            pk=2,
        )

    def test_str(self):
        """Test returning the string representation of an instance."""
        self.assertEqual(
            self.tokens_embeddings1.__str__(),
            "TokensEmbeddings for 99.9999/999-9-999-99999-1_11",
        )
        self.assertEqual(self.tokens_embeddings2.__str__(), "TokensEmbeddings for None")
