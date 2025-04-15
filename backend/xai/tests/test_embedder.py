"""Test the xai app embedder."""

from django.test import TestCase

from xai.embedder import LLMEmbedder


class TestLLMEmbedder(TestCase):
    """Test Large Language Model embedder."""

    def setUp(self):
        """Prepare initial data for testing."""
        text = "this is a test sentence"
        self.embedder = LLMEmbedder(text=text)

    def test_encoded_input_model_output(self):
        """Test encoded_input_model_output method."""
        self.assertListEqual(
            ["input_ids", "token_type_ids", "attention_mask"],
            list(self.embedder.encoded_input_model_output()[0].keys()),
        )
        self.assertListEqual(
            ["last_hidden_state", "pooler_output"],
            list(self.embedder.encoded_input_model_output()[1].keys()),
        )
        embedder = LLMEmbedder()
        self.assertIsNone(embedder.encoded_input_model_output()[0])
        self.assertIsNone(embedder.encoded_input_model_output()[1])

    def test_create_embedding(self):
        """Test create_embedding method."""
        sentence_embedding_res = self.embedder.get_sentence_embeddings()
        token_embedding_res = self.embedder.get_tokens_embeddings()
        # NB given high dimensionality,
        # are compare only fer elements in order to be sure that seed is working
        sentence_embedding_element_expected = 3.69973332e-01
        sentence_embedding_element_res = sentence_embedding_res[0]
        self.assertAlmostEqual(
            sentence_embedding_element_res, sentence_embedding_element_expected, 5
        )
        token_embedding_element_expected = 5.99695206e-01
        token_embedding_element_res = token_embedding_res[1]["embedding"][0]
        self.assertAlmostEqual(
            token_embedding_element_res, token_embedding_element_expected, 5
        )

    def test_metachars(self):
        """Test embedder metachars."""
        self.assertEqual(self.embedder.metachars, ["[CLS]", "[SEP]"])

    def test_filler_char(self):
        """Test embedder filter_char."""
        self.assertEqual(self.embedder.filler_char, "#")
