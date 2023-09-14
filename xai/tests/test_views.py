"""Test the universities app views."""

from django.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase

from connect.tests.utils import SetUpQdrantMixin
from scopus.models import ScopusAuthor, ScopusDocument
from xai.facade import SearchMostSimilarFacade, WriteEmbeddingFacade


class AuthorViewSetTest(SetUpQdrantMixin, APITestCase):
    """A set of tests for author views."""

    api_author_url = "/api/author/search/"

    @classmethod
    def setUpTestData(cls):
        """Prepare initial data for testing."""
        cls.scopus_authors = [
            ScopusAuthor(
                author_id="11111111111",
                data={
                    "coredata": {
                        "orcid": "0000-0000-0000-0001",
                    },
                    "author-profile": {
                        "preferred-name": {
                            "given-name": "Sheldon Lee",
                            "indexed-name": "Cooper S. L.",
                            "initials": "S.",
                            "surname": "Cooper",
                        },
                        "affiliation-current": {
                            "affiliation": {
                                "ip-doc": {
                                    "@id": "333333333",
                                    "afdispname": "East Texas Tech University",
                                },
                            }
                        },
                    },
                },
            ),
            ScopusAuthor(
                author_id="22222222222",
                data={
                    "coredata": {
                        "orcid": "0000-0000-0000-0002",
                    },
                    "author-profile": {
                        "preferred-name": {
                            "given-name": "Leonard",
                            "indexed-name": "Hofstadter L.",
                            "initials": "L.",
                            "surname": "Hofstadter",
                        },
                        "affiliation-current": {
                            "affiliation": [
                                {
                                    "ip-doc": {
                                        "@id": "444444444",
                                        "afdispname": "Princeton University",
                                    },
                                },
                                {
                                    "ip-doc": {
                                        "@id": "555555555",
                                        "afdispname": "University of California",
                                    },
                                },
                            ]
                        },
                    },
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
            cls.scopus_documents[1], [11111111111, 22222222222]
        )
        WriteEmbeddingFacade().load_document_point(
            point=cls.point3, collection_name=settings.QDRANT_DOCUMENTS_COLLECTION
        )

    def test_endpoint_url_path(self):
        """Test author endpoint url path."""
        self.assertEqual(self.api_author_url, "/api/author/search/")

    def test_get_search(self):
        """Test get search author endpoint."""
        response = self.client.get(self.api_author_url, {"team_size": "", "q": ""})
        expected_response = []
        self.assertJSONEqual(response.content, expected_response)
        response = self.client.get(self.api_author_url)
        expected_response = []
        self.assertJSONEqual(response.content, expected_response)
        response = self.client.get(
            self.api_author_url, {"team_size": "2", "q": "test sentence"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_response = [
            {
                "authorId": "11111111111",
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
                        "doi": "99.9999/999-9-999-99999-2_22",
                        "title": "Introduction to the monographic issue Emotional "
                        "Education in Diversity Contexts",
                        "description": None,
                        "score": 0.04815,
                    },
                ],
                "score": 0.464,
                "fullName": "Sheldon Lee Cooper",
                "university": "East Texas Tech University",
                "orcid": "0000-0000-0000-0001",
            },
            {
                "authorId": "22222222222",
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
                "score": 0.40883,
                "fullName": "Leonard Hofstadter",
                "university": "Princeton University / University of California",
                "orcid": "0000-0000-0000-0002",
            },
        ]
        self.assertJSONEqual(
            response.content,
            expected_response,
        )
