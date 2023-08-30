"""Test the universities app views."""

from rest_framework import status
from rest_framework.test import APITestCase

from universities.models import Author, University


class AuthorViewSetTest(APITestCase):
    """A set of tests for author views."""

    api_author_url = "/api/author/search/"

    @classmethod
    def setUpTestData(cls):
        """Prepare initial data for testing."""
        princeton = University.objects.create(name="Princeton University")
        ettu = University.objects.create(name="East Texas Tech University")
        mit = University.objects.create(name="Massachusetts Institute of Technology")
        cambridge = University.objects.create(name="University of Cambridge")
        uc = University.objects.create(name="University of California")
        harvard = University.objects.create(name="Harvard University")
        Author.objects.bulk_create(
            [
                Author(
                    orcid="0000-0000-0000-0001",
                    full_name="Leonard Hofstadter",
                    university_id=princeton.id,
                ),
                Author(
                    orcid="0000-0000-0000-0002",
                    full_name="Sheldon Cooper",
                    university_id=ettu.id,
                ),
                Author(
                    orcid="0000-0000-0000-0003",
                    full_name="Howard Wolowitz",
                    university_id=mit.id,
                ),
                Author(
                    orcid="0000-0000-0000-0004",
                    full_name="Raj Koothrappali",
                    university_id=cambridge.id,
                ),
                Author(
                    orcid="0000-0000-0000-0005",
                    full_name="Bernadette Rostenkowski",
                    university_id=uc.id,
                ),
                Author(
                    orcid="0000-0000-0000-0006",
                    full_name="Amy Farrah Fowler",
                    university_id=harvard.id,
                ),
            ]
        )

    def test_endpoint_url_path(self):
        """Test author endpoint url path."""
        self.assertEqual(self.api_author_url, "/api/author/search/")

    def test_get_list(self):
        """Test get list author endpoint."""
        with self.subTest("Test get without filters."):
            response = self.client.get(self.api_author_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertJSONEqual(response.content, [])
        with self.subTest("Test get filtered by team_size."):
            response = self.client.get(self.api_author_url, {"team_size": "3"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertJSONEqual(
                response.content,
                [
                    {
                        "fullName": "Leonard Hofstadter",
                        "orcid": "0000-0000-0000-0001",
                        "university": "Princeton University",
                    },
                    {
                        "fullName": "Sheldon Cooper",
                        "orcid": "0000-0000-0000-0002",
                        "university": "East Texas Tech University",
                    },
                    {
                        "fullName": "Howard Wolowitz",
                        "orcid": "0000-0000-0000-0003",
                        "university": "Massachusetts Institute of Technology",
                    },
                ],
            )
        with self.subTest("Test get filtered by query search."):
            response = self.client.get(self.api_author_url, {"q": "Computer science"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.json()), 6)

    def test_search_and_filter_by_team_size(self):
        """Test search and filter by team_size on authors endpoint."""
        response = self.client.get(
            f"{self.api_author_url}",
            {
                "q": "Computer science",
                "team_size": "4",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 4)
