"""Test the xai app facade."""

from unittest import TestCase

from django.conf import settings
from qdrant_client.http import models

from scopus.models import ScopusDocument
from xai.facade import WriteEmbeddingFacade


class TestWriteEmbeddingFacade(TestCase):
    """Test write embedding facade."""

    def setUp(self):
        """Prepare initial data for testing."""
        self.facade = WriteEmbeddingFacade()
        self.point = models.PointStruct(
            id=3849439176125250520832009392267879549757464859643919592969476415123787,
            payload={
                "authors": ["11111111111", "22222222222"],
                "title": "Score vs. Winrate in Score-Based Games: "
                "Which Reward for Reinforcement Learning?",
                "description": "In the last years, DeepMind algorithm AlphaZero "
                "has become the state of the art to efficiently tackle perfect "
                "information two-player zero-sum games with a win/lose outcome. "
                "However, when the win/lose outcome is decided by a final score "
                "difference, AlphaZero may play score-suboptimal moves, because "
                "all winning final positions are equivalent from the win/lose "
                "outcome perspective. This can be an issue, for instance when "
                "used for teaching, or when trying to understand whether there "
                "is a better move. Moreover, there is the theoretical quest of "
                "the perfect game. A naive approach would be training a "
                "AlphaZero-like agent to predict score differences instead of "
                "win/lose outcomes. Since the game of Go is deterministic, this "
                "should as well produce outcome-optimal play. However, it is a "
                "folklore belief that 'this does not work'.In this paper we first "
                "provide empirical evidence to this belief. We then give a "
                "theoretical interpretation of this suboptimality in a general "
                "perfect information two-player zero-sum game where the complexity "
                "of a game like Go is replaced by randomness of the environment. "
                "We show that an outcome-optimal policy has a different preference "
                "for uncertainty when it is winning or losing. In particular, when "
                "in a losing state, an outcome-optimal agent chooses actions "
                "leading to a higher variance of the score. We then posit that "
                "when approximation is involved, a deterministic game behaves like "
                "a nondeterministic game, where the score variance is modeled by "
                "how uncertain the position is. We validate this hypothesis in a "
                "AlphaZero-like software with a human expert.",
            },
            vector=[0.1, 0.2, 0.3],
        )

    def test_load_document_point(self):
        """Test load_document_point method."""
        res = self.facade.load_document_point(
            point=self.point, collection_name=settings.QDRANT_DOCUMENTS_COLLECTION
        )
        self.assertEqual(res.status, "completed")

    def test_merge_title_and_description(self):
        """Test merge_title_and_description method."""
        title = (
            "Score vs. Winrate in Score-Based Games: Which Reward for "
            "Reinforcement Learning?"
        )
        description = (
            "In the last years, DeepMind algorithm AlphaZero has become the "
            "state of the art to efficiently tackle perfect information two-player "
            "zero-sum games with a win/lose outcome."
        )
        merged_text = self.facade.merge_title_and_description(title, description)
        expected_result = [
            "Score vs. Winrate in Score-Based Games: Which Reward for Reinforcement "
            "Learning?. In the last years, DeepMind algorithm AlphaZero has become "
            "the state of the art to efficiently tackle perfect information "
            "two-player zero-sum games with a win/lose outcome."
        ]
        self.assertEqual(merged_text, expected_result)

    def test_generate_document_point(self):
        """Test generate_document_point method."""
        scopus_documents = [
            ScopusDocument(
                id=1,
                doi="99.9999/999-9-999-99999-1_11",
                data={
                    "doi": "99.9999/999-9-999-99999-1_11",
                    "title": "The Evaluation of Family Support Programmes in Spain. "
                    "An Analysis of their Quality Standards",
                    "author_ids": "11111111111;22222222222;33333333333",
                    "description": "Since the well-known publication of the Society "
                    "for Prevention Research about standards for evidence related to "
                    "research on prevention interventions, a rigorous evaluation is "
                    "considered one of the main requirements for "
                    "evidence-based programmes.",
                    "author_count": "3",
                    "citedby_count": 0,
                },
            ),
            ScopusDocument(
                id=2,
                doi="99.9999/999-9-999-99999-2_22",
                data={
                    "doi": "99.9999/999-9-999-99999-2_22",
                    "title": "Introduction to the monographic issue Emotional "
                    "Education in Diversity Contexts",
                    "author_ids": "11111111111;22222222222;33333333333",
                    "description": None,
                    "author_count": "3",
                    "citedby_count": 0,
                },
            ),
            ScopusDocument(
                id=3,
                doi="99.9999/999-9-999-99999-3_33",
                data={
                    "doi": "99.9999/999-9-999-99999-3_33",
                    "title": "Comparison of parental competences in fathers and "
                    "mothers with adolescent children"
                    "Education in Diversity Contexts",
                    "author_ids": "11111111111;22222222222;33333333333",
                    "description": "Parenting adolescents requires personal, emotional "
                    "and social competencies from the parents. There are few gender "
                    "studies that analyze these competencies in the father and the "
                    "mother in the same family.",
                    "author_count": "3",
                    "citedby_count": 0,
                },
            ),
        ]
        document_point1 = self.facade.generate_document_point(scopus_documents[0])
        document_point2 = self.facade.generate_document_point(scopus_documents[1])
        document_point3 = self.facade.generate_document_point(scopus_documents[2])
        self.assertEqual(len(document_point1.vector), 384)
        self.assertIn("author_ids", document_point1.payload.keys())
        self.assertIn("token", document_point1.payload.keys())
        self.assertEqual(
            document_point1.payload["author_ids"],
            ["11111111111", "22222222222", "33333333333"],
        )
        self.assertEqual(
            document_point1.payload["doi"],
            "99.9999/999-9-999-99999-1_11",
        )
        self.assertEqual(len(document_point1.payload["token"]), 57)
        self.assertEqual(len(document_point2.payload["token"]), 15)
        self.assertEqual(len(document_point3.payload["token"]), 56)
