"""Test the xai app facade."""

from django.conf import settings
from django.test import TestCase, override_settings

from connect.tests.utils import SetUpQdrantMixin
from scopus.models import ScopusAuthor, ScopusDocument
from xai.facade import SearchMostSimilarFacade, WriteEmbeddingFacade


class TestWriteEmbeddingFacade(SetUpQdrantMixin, TestCase):
    """Test write embedding facade."""

    @classmethod
    def setUpTestData(cls):
        """Set up test case."""
        cls.facade = WriteEmbeddingFacade()
        cls.scopus_authors = [
            ScopusAuthor(
                author_id="11111111111",
                data={
                    "author-profile": {
                        "preferred-name": {
                            "given-name": "Sheldon Lee",
                            "indexed-name": "Cooper S. L.",
                            "initials": "S.",
                            "surname": "Cooper",
                        },
                    }
                },
            ),
            ScopusAuthor(
                author_id="22222222222",
                data={
                    "author-profile": {
                        "preferred-name": {
                            "given-name": "Leonard",
                            "indexed-name": "Hofstadter L.",
                            "initials": "L.",
                            "surname": "Hofstadter",
                        },
                    }
                },
            ),
        ]
        ScopusAuthor.objects.bulk_create(cls.scopus_authors)
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
        cls.point1 = cls.facade.generate_document_point(
            scopus_documents[0], [11111111111, 22222222222]
        )
        cls.point2 = cls.facade.generate_document_point(
            scopus_documents[1], [11111111111, 22222222222]
        )
        cls.point3 = cls.facade.generate_document_point(
            scopus_documents[2], [11111111111, 22222222222]
        )

    def test_load_document_point(self):
        """Test load_document_point method."""
        res = self.facade.load_document_point(
            point=self.point1, collection_name=settings.QDRANT_DOCUMENTS_COLLECTION
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
        expected_result = (
            "Score vs. Winrate in Score-Based Games: Which Reward for Reinforcement "
            "Learning?. In the last years, DeepMind algorithm AlphaZero has become "
            "the state of the art to efficiently tackle perfect information "
            "two-player zero-sum games with a win/lose outcome."
        )
        self.assertEqual(merged_text, expected_result)

    def test_generate_document_point(self):
        """Test generate_document_point method."""
        self.assertEqual(len(self.point1.vector), 384)
        self.assertIn("author_ids", self.point1.payload.keys())
        self.assertEqual(
            self.point1.payload["author_ids"],
            ["11111111111", "22222222222"],
        )
        self.assertEqual(
            self.point1.payload["doi"],
            "99.9999/999-9-999-99999-1_11",
        )


@override_settings(QDRANT_VECTOR_SIZE=384)
class TestSearchMostSimilarFacade(SetUpQdrantMixin, TestCase):
    """Test search most similar facade."""

    @classmethod
    def setUpTestData(cls):
        """Prepare initial data for testing."""
        cls.scopus_authors = [
            ScopusAuthor(
                author_id="11111111111",
                data={
                    "author-profile": {
                        "preferred-name": {
                            "given-name": "Sheldon Lee",
                            "indexed-name": "Cooper S. L.",
                            "initials": "S.",
                            "surname": "Cooper",
                        },
                    }
                },
            ),
            ScopusAuthor(
                author_id="22222222222",
                data={
                    "author-profile": {
                        "preferred-name": {
                            "given-name": "Leonard",
                            "indexed-name": "Hofstadter L.",
                            "initials": "L.",
                            "surname": "Hofstadter",
                        },
                    }
                },
            ),
        ]
        ScopusAuthor.objects.bulk_create(cls.scopus_authors)
        cls.scopus_documents = [
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
                    "author_ids": "11111111111",
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
                    "author_ids": "11111111111;33333333333",
                    "description": "Parenting adolescents requires personal, emotional "
                    "and social competencies from the parents. There are few gender "
                    "studies that analyze these competencies in the father and the "
                    "mother in the same family.",
                    "author_count": "3",
                    "citedby_count": 0,
                },
            ),
        ]
        cls.facade = SearchMostSimilarFacade(sentence="test sentence")
        cls.point1 = WriteEmbeddingFacade().generate_document_point(
            cls.scopus_documents[0], [11111111111, 22222222222]
        )
        WriteEmbeddingFacade().load_document_point(
            point=cls.point1, collection_name=settings.QDRANT_DOCUMENTS_COLLECTION
        )
        cls.point2 = WriteEmbeddingFacade().generate_document_point(
            cls.scopus_documents[1], [11111111111, 22222222222]
        )
        WriteEmbeddingFacade().load_document_point(
            point=cls.point2, collection_name=settings.QDRANT_DOCUMENTS_COLLECTION
        )
        cls.point3 = WriteEmbeddingFacade().generate_document_point(
            cls.scopus_documents[2], [11111111111, 22222222222]
        )
        WriteEmbeddingFacade().load_document_point(
            point=cls.point3, collection_name=settings.QDRANT_DOCUMENTS_COLLECTION
        )

    def test_search_most_similar(self):
        """Test search_most_similar method."""
        response = self.facade.search_most_similar(limit=1)
        self.assertEqual(len(response["results"]), 1)
        self.assertEqual(len(response["author_ids"]), 2)
        response = self.facade.search_most_similar(limit=2)
        self.assertEqual(len(response["results"]), 2)
        self.assertEqual(len(response["author_ids"]), 2)

    def test_search_most_similar_filtered_by_author_id(self):
        """Test search_most_similar_filtered_by_author_id method."""
        response = self.facade.search_most_similar_filtered_by_author_id(
            author_id="11111111111", limit_documents=1
        )
        self.assertEqual(len(response), 1)
        response = self.facade.search_most_similar_filtered_by_author_id(
            author_id="11111111111", limit_documents=2
        )
        self.assertEqual(len(response), 2)
        response = self.facade.search_most_similar_filtered_by_author_id(
            author_id="22222222222", limit_documents=3
        )
        self.assertEqual(len(response), 1)

    def test_get_authors_from_similar_search(self):
        """Test get_authors_from_similar_search method."""
        response = self.facade.get_authors_from_similar_search(
            limit_authors=2,
        )
        expected_response = [
            {
                "author_id": "11111111111",
                "documents": [
                    {
                        "doi": "99.9999/999-9-999-99999-1_11",
                        "title": "The Evaluation of Family Support Programmes "
                        "in Spain. An Analysis of their Quality Standards",
                        "description": "Since the well-known publication of the "
                        "Society for Prevention Research about standards for evidence "
                        "related to research on prevention interventions, a rigorous "
                        "evaluation is considered one of the main requirements for "
                        "evidence-based programmes.",
                        "score": 0.16714,
                    },
                    {
                        "doi": "99.9999/999-9-999-99999-3_33",
                        "title": "Comparison of parental competences in fathers and "
                        "mothers with adolescent childrenEducation in "
                        "Diversity Contexts",
                        "description": "Parenting adolescents requires personal, "
                        "emotional and social competencies from the parents. There are "
                        "few gender studies that analyze these competencies in the "
                        "father and the mother in the same family.",
                        "score": 0.1603,
                    },
                    {
                        "doi": "99.9999/999-9-999-99999-2_22",
                        "title": "Introduction to the monographic issue Emotional "
                        "Education in Diversity Contexts",
                        "description": None,
                        "score": 0.04815,
                    },
                ],
                "score": 0.3756,
            },
            {
                "author_id": "22222222222",
                "documents": [
                    {
                        "doi": "99.9999/999-9-999-99999-1_11",
                        "title": "The Evaluation of Family Support Programmes "
                        "in Spain. An Analysis of their Quality Standards",
                        "description": "Since the well-known publication of the "
                        "Society for Prevention Research about standards for evidence "
                        "related to research on prevention interventions, a rigorous "
                        "evaluation is considered one of the main requirements for "
                        "evidence-based programmes.",
                        "score": 0.16714,
                    }
                ],
                "score": 0.16714,
            },
        ]
        self.assertEqual(len(response), 2)
        self.assertEqual(response, expected_response)
