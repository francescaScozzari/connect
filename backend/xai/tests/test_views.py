"""Test the xai app views."""

from rest_framework import status
from rest_framework.test import APITestCase

from connect.tests.utils import SetUpQdrantMixin, XaiSearchDataMixin


class AuthorViewSetTest(SetUpQdrantMixin, XaiSearchDataMixin, APITestCase):
    """A set of tests for author views."""

    api_author_url = "/api/author/search/"

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
            self.api_author_url, {"team_size": "2", "q": "test has sentence."}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_response = {
            "authors": [
                {
                    "authorId": "11111111111",
                    "documents": [
                        {
                            "doi": "99.9999/999-9-999-99999-1_11",
                            "title": "The Evaluation of Family Support Programmes "
                            "in Spain. An Analysis of their Quality Standards",
                            "description": "Since the well-known publication of the "
                            "Society for Prevention Research about standards for "
                            "evidence related to research on prevention interventions, "
                            "a rigorous evaluation is considered one of the main "
                            "requirements for evidence-based programmes.",
                            "score": 0.19869,
                            "highlights": ["evaluation", "requirements"],
                        },
                        {
                            "doi": "99.9999/999-9-999-99999-3_33",
                            "title": "Comparison of parental competences in fathers "
                            "and mothers with adolescent childrenEducation in "
                            "Diversity Contexts",
                            "description": "Parenting adolescents requires personal, "
                            "emotional and social competencies from the parents. "
                            "There are few gender studies that analyze these "
                            "competencies in the father and the mother "
                            "in the same family.",
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
                            "Society for Prevention Research about standards for "
                            "evidence related to research on prevention interventions, "
                            "a rigorous evaluation is considered one of the main "
                            "requirements for evidence-based programmes.",
                            "score": 0.19869,
                            "highlights": ["evaluation", "requirements"],
                        }
                    ],
                    "score": 0.44575,
                    "fullName": "Leonard Hofstadter",
                    "university": "Princeton University / University of California",
                    "orcid": "0000-0000-0000-0002",
                },
            ],
            "givenSentence": {
                "highlights": ["test", "sentence"],
                "text": "test has sentence.",
            },
        }
        self.assertJSONEqual(
            response.content,
            expected_response,
        )
