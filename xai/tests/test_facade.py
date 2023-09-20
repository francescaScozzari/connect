"""Test the xai app facade."""

from django.test import TestCase, override_settings

from connect.tests.utils import SetUpQdrantMixin
from scopus.models import ScopusAuthor, ScopusDocument
from xai.facade import SearchMostSimilarFacade, WriteEmbeddingFacade


class TestWriteEmbeddingFacade(SetUpQdrantMixin, TestCase):
    """Test write embedding facade."""

    @classmethod
    def setUpTestData(cls):
        """Set up test case."""
        cls.facade = WriteEmbeddingFacade
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
        ScopusDocument.objects.bulk_create(cls.scopus_documents)
        cls.point1 = cls.facade(cls.scopus_documents[0]).generate_document_point(
            [11111111111, 22222222222]
        )
        cls.point2 = cls.facade(cls.scopus_documents[1]).generate_document_point(
            [11111111111, 22222222222]
        )
        cls.point3 = cls.facade(cls.scopus_documents[2]).generate_document_point(
            [11111111111, 22222222222]
        )

    def test_load_document_point(self):
        """Test load_document_point method."""
        res = self.facade.load_document_point(point=self.point1)
        self.assertEqual(res.status, "completed")

    def test_merge_title_and_description(self):
        """Test merge_title_and_description method."""
        merged_text = self.facade(
            self.scopus_documents[0]
        ).merge_title_and_description()
        expected_result = (
            "The Evaluation of Family Support Programmes in Spain. "
            "An Analysis of their Quality Standards. Since the well-known publication "
            "of the Society for Prevention Research about standards for evidence "
            "related to research on prevention interventions, a rigorous evaluation is "
            "considered one of the main requirements for evidence-based programmes."
        )
        self.assertEqual(merged_text, expected_result)
        merged_text = self.facade(
            self.scopus_documents[1]
        ).merge_title_and_description()
        expected_result = (
            "Introduction to the monographic issue Emotional Education "
            "in Diversity Contexts."
        )
        self.assertEqual(merged_text, expected_result)
        merged_text = self.facade(
            self.scopus_documents[2]
        ).merge_title_and_description()
        expected_result = (
            "Comparison of parental competences in fathers and mothers "
            "with adolescent childrenEducation in Diversity Contexts. Parenting "
            "adolescents requires personal, emotional and social competencies from the "
            "parents. There are few gender studies that analyze these competencies in "
            "the father and the mother in the same family."
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

    def test_create_document_tokens_embeddings(self):
        """Test create_document_tokens_embeddings method."""
        self.facade(self.scopus_documents[0]).create_document_tokens_embeddings()
        self.assertEqual(len(self.scopus_documents[0].tokens.data[0]["embedding"]), 384)
        self.assertEqual(self.scopus_documents[0].tokens.data[0]["token"], "[CLS]")
        self.assertEqual(self.scopus_documents[0].tokens.data[1]["token"], "the")
        self.assertEqual(self.scopus_documents[0].tokens.data[2]["token"], "evaluation")
        self.assertEqual(self.scopus_documents[0].tokens.data[-1]["token"], "[SEP]")


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
        ScopusDocument.objects.bulk_create(cls.scopus_documents)
        cls.facade = SearchMostSimilarFacade(sentence="test has sentence.")
        cls.document_tokens_embeddings1 = WriteEmbeddingFacade(
            cls.scopus_documents[0]
        ).create_document_tokens_embeddings()
        cls.point1 = WriteEmbeddingFacade(
            cls.scopus_documents[0]
        ).generate_document_point([11111111111, 22222222222])
        WriteEmbeddingFacade.load_document_point(point=cls.point1)
        cls.document_tokens_embeddings2 = WriteEmbeddingFacade(
            cls.scopus_documents[1]
        ).create_document_tokens_embeddings()
        cls.point2 = WriteEmbeddingFacade(
            cls.scopus_documents[1],
        ).generate_document_point([11111111111, 22222222222])
        WriteEmbeddingFacade.load_document_point(point=cls.point2)
        cls.point3 = WriteEmbeddingFacade(
            cls.scopus_documents[2]
        ).generate_document_point([11111111111, 22222222222])
        WriteEmbeddingFacade.load_document_point(point=cls.point3)

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
                        "score": 0.19869,
                        "highlights": ["evaluation", "requirements"],
                    },
                    {
                        "doi": "99.9999/999-9-999-99999-3_33",
                        "title": "Comparison of parental competences in fathers and "
                        "mothers with adolescent childrenEducation in "
                        "Diversity Contexts",
                        "description": "Parenting adolescents requires personal, "
                        "emotional and social competencies from the parents. There "
                        "are few gender studies that analyze these competencies in the "
                        "father and the mother in the same family.",
                        "score": 0.18156,
                        "highlights": [],
                    },
                    {
                        "doi": "99.9999/999-9-999-99999-2_22",
                        "title": "Introduction to the monographic issue Emotional "
                        "Education in Diversity Contexts",
                        "description": "",
                        "score": 0.05844,
                        "highlights": ["contexts", "education"],
                    },
                ],
                "score": 0.66234,
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
                        "score": 0.19869,
                        "highlights": ["evaluation", "requirements"],
                    }
                ],
                "score": 0.44575,
            },
        ]
        self.assertEqual(len(response), 2)
        self.assertEqual(response, expected_response)

    def test_get_author_normalized_score(self):
        """Test get_author_normalized_score method."""
        author_scores = [0.16714162873705102, 0.16030469109159676, 0.04759527616166713]
        normalized_score = SearchMostSimilarFacade(
            sentence=""
        ).get_author_normalized_score(author_scores)
        self.assertEqual(normalized_score, 0.61241)

    def test_get_document_explainability(self):
        """Test get_document_explainability method."""
        document_explainability = self.facade.get_document_explainability(
            self.scopus_documents[0].doi
        )
        expected_result = [
            {
                "given_word": "test",
                "restored_word": "evaluation",
                "score": 0.3064,
            },
            {
                "given_word": "sentence",
                "restored_word": "requirements",
                "score": 0.22269,
            },
        ]
        self.assertEqual(document_explainability, expected_result)

    def test_get_document_restored_word(self):
        """Test get_document_restored_word method."""
        document_explainability = self.facade.get_document_highlights(
            self.scopus_documents[0].doi
        )
        expected_result = ["evaluation", "requirements"]
        self.assertEqual(document_explainability, expected_result)

    def test_get_sentence_highlights(self):
        """Test get_sentence_highlights method."""
        sentence_highlights = self.facade.get_sentence_highlights()
        expected_result = ["test", "sentence"]
        self.assertEqual(sentence_highlights, expected_result)
