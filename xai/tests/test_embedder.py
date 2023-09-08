"""Test the xai app embedder."""

from unittest import TestCase

from xai.embedder import LLMEmbedder


class TestLLMEmbedder(TestCase):
    """Test Large Language Model embedder."""

    def setUp(self):
        """Prepare initial data for testing."""
        self.embedder = LLMEmbedder()

    def test_create_embedding(self):
        """Test create_embedding method."""
        texts = ["this is a test sentence"]
        sentence_embedding_res, token_embedding_res = self.embedder.create_embedding(
            texts=texts
        )
        # NB given high dimensionality,
        # are compare only fer elements in order to be sure that seed is working
        sentence_embedding_element_expected = 3.69973332e-01
        sentence_embedding_element_res = sentence_embedding_res[0][0]
        self.assertAlmostEqual(
            sentence_embedding_element_res, sentence_embedding_element_expected, 5
        )
        token_embedding_element_expected = 5.99695206e-01
        token_embedding_element_res = token_embedding_res[0][1]["embedding"][0]
        self.assertAlmostEqual(
            token_embedding_element_res, token_embedding_element_expected, 5
        )

    def test_metachars(self):
        """Test embedder metachars."""
        self.assertEqual(self.embedder.metachars, ["[CLS]", "[SEP]"])

    def test_filler_char(self):
        """Test embedder filter_char."""
        self.assertEqual(self.embedder.filler_char, "#")
