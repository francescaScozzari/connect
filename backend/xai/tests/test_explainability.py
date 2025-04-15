"""Test xai app explainability."""

import numpy as np
from django.test import TestCase

from connect.tests.utils import SetUpQdrantMixin
from xai.explainability import ExplainabilityComputing


class TestlExplainabilityComputing(SetUpQdrantMixin, TestCase):
    """Test explainability computing."""

    @classmethod
    def setUpTestData(cls):
        """Set up test case."""

    def test_split_tokens_and_embeddings(self):
        """Test split_tokens_and_embeddings method."""
        sample_tokens_embeddings = [
            {"token": "test", "embedding": [1, 2]},
            {"token": "#test", "embedding": [3, 4]},
            {"token": "[CLS]", "embedding": [5, 6]},
        ]
        tokens, embeddings = ExplainabilityComputing.split_tokens_and_embeddings(
            sample_tokens_embeddings
        )
        self.assertEqual(tokens, ["test", "test"])
        self.assertEqual(len(tokens), 2)
        self.assertAlmostEqual(embeddings[0][0], 0.4472136, 5)

    def test_largest_indices(self):
        """Test largest_indices method."""
        sample_vector = np.array([[1, 2], [3, 4]])
        res_indices, res_values = ExplainabilityComputing.largest_indices(
            vector=sample_vector, nb_values=None
        )
        self.assertSequenceEqual(res_indices, [(1, 1), (1, 0), (0, 1), (0, 0)])
        self.assertSequenceEqual(res_values, [4, 3, 2, 1])
        res_indices, res_values = ExplainabilityComputing.largest_indices(
            vector=sample_vector, nb_values=1
        )
        self.assertSequenceEqual(res_indices, [(1, 1)])
        self.assertSequenceEqual(res_values, [4])

    def test_get_words_matching_with_score(self):
        """Test get_words_matching_with_score method."""
        sample_sentence_tokens_embeddings = [
            {"token": "test", "embedding": [1, 2]},
            {"token": ".", "embedding": [3, 4]},
        ]
        (
            sentence_tokens,
            sentence_embeddings,
        ) = ExplainabilityComputing.split_tokens_and_embeddings(
            sample_sentence_tokens_embeddings
        )
        sample_document_tokens_embeddings = [
            {"token": "test", "embedding": [1, 2]},
            {"token": "#test", "embedding": [1, 2]},
            {"token": "sample", "embedding": [5, 6]},
            {"token": ".", "embedding": [3, 4]},
            {"token": "[CLS]", "embedding": [1, 2]},
        ]
        (
            document_tokens,
            document_embeddings,
        ) = ExplainabilityComputing.split_tokens_and_embeddings(
            sample_document_tokens_embeddings
        )
        words_with_score = ExplainabilityComputing.get_words_matching_with_score(
            sentence_tokens, sentence_embeddings, document_tokens, document_embeddings
        )
        expected = [
            {
                "given_word": "test",
                "restored_word": "test",
                "score": 1.0,
            },
            {
                "given_word": "test",
                "restored_word": "test",
                "score": 1.0,
            },
            {
                "given_word": "test",
                "restored_word": "sample",
                "score": 0.97342,
            },
        ]
        self.assertSequenceEqual(words_with_score, expected)

    def test_get_given_words_result(self):
        """Test get_given_words_result method."""
        sentence_tokens = ["test", "search", "text"]
        words_with_score = [
            {
                "given_word": "test",
                "restored_word": "test",
                "score": 1.0,
            },
            {
                "given_word": "test",
                "restored_word": "test",
                "score": 1.0,
            },
            {
                "given_word": "test",
                "restored_word": "sample",
                "score": 0.97342,
            },
            {
                "given_word": "search",
                "restored_word": "sample",
                "score": 0.95342,
            },
            {
                "given_word": "search",
                "restored_word": "test",
                "score": 0.84673,
            },
            {
                "given_word": "text",
                "restored_word": "sample",
                "score": 0.82763,
            },
            {
                "given_word": "text",
                "restored_word": "test",
                "score": 0.72938,
            },
        ]
        given_words_result = ExplainabilityComputing.get_given_words_result(
            sentence_tokens, words_with_score
        )
        expected_result = [
            {
                "given_word": "test",
                "restored_word": "test",
                "score": 1.0,
            },
            {
                "given_word": "search",
                "restored_word": "sample",
                "score": 0.95342,
            },
            {
                "given_word": "text",
                "restored_word": "sample",
                "score": 0.82763,
            },
        ]
        self.assertEqual(given_words_result, expected_result)

    def test_explain_result(self):
        """Test explain_result method."""
        sample_sentence_tokens_embeddings = [
            {"token": "test", "embedding": [1, 2]},
            {"token": "search", "embedding": [3, 4]},
            {"token": "text", "embedding": [5, 6]},
            {"token": ".", "embedding": [7, 8]},
        ]
        sample_document_tokens_embeddings = [
            {"token": "test", "embedding": [1, 2]},
            {"token": "#test", "embedding": [1, 2]},
            {"token": "sample", "embedding": [5, 4]},
            {"token": ".", "embedding": [3, 4]},
            {"token": "[CLS]", "embedding": [1, 2]},
        ]
        explain_result = ExplainabilityComputing.explain_result(
            sample_sentence_tokens_embeddings, sample_document_tokens_embeddings
        )
        expected_result = [
            {"given_word": "test", "restored_word": "test", "score": 1.0},
            {"given_word": "search", "restored_word": "test", "score": 0.98387},
            {"given_word": "text", "restored_word": "sample", "score": 0.9798},
        ]
        self.assertEqual(explain_result, expected_result)
