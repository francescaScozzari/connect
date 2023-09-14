"""Test the Scopus app models."""

import json
from unittest.mock import patch

import requests_mock
from django.test import TestCase
from pybliometrics.scopus.exception import ScopusException

from scopus.models import ScopusAuthor, ScopusDocument
from scopus.tests import (
    AUTHOR_1_SEARCH_JSON,
    AUTHOR_11111111111_DOCUMENTS_JSON,
    AUTHOR_11111111111_SEARCH_JSON,
    AUTHOR_SEARCH_BASE_URL,
    SCOPUS_SEARCH_BASE_URL,
)


@requests_mock.Mocker()
class ScopusAuthorTest(TestCase):
    """Test the ScopusAuthor model."""

    author_1_id = 1
    author_11111111111_id = 11111111111
    author_11111111111_orcid_id = "1111-1111-1111-111X"

    def test_str(self, m):
        """Test returning the string representation of an instance."""
        author_retrieval_11111111111 = ScopusAuthor(
            author_id=self.author_11111111111_id, data={"orcid": "0001-0002-0003-0004"}
        )
        self.assertEqual(author_retrieval_11111111111.__str__(), "11111111111")

    def test_fetch_authors_results(self, m):
        """Test fetching authors results."""
        with self.subTest("Catch Scopus exception"):
            m.get(
                AUTHOR_SEARCH_BASE_URL.format("AU-ID", self.author_1_id),
                json=json.loads(AUTHOR_1_SEARCH_JSON.read_text()),
            )
            with patch("scopus.models.AuthorSearch", side_effect=(ScopusException,)):
                self.assertEqual(
                    ScopusAuthor.fetch_authors_results(self.author_1_id), []
                )
        with self.subTest("Resource not found"):
            m.get(
                AUTHOR_SEARCH_BASE_URL.format("AU-ID", self.author_1_id),
                json=json.loads(AUTHOR_1_SEARCH_JSON.read_text()),
            )
            self.assertEqual(ScopusAuthor.fetch_authors_results(self.author_1_id), [])
        with self.subTest("Resource found"):
            m.get(
                AUTHOR_SEARCH_BASE_URL.format("AU-ID", self.author_11111111111_id),
                json=json.loads(AUTHOR_11111111111_SEARCH_JSON.read_text()),
            )
            processed_objs = ScopusAuthor.fetch_authors_results(
                self.author_11111111111_id
            )
            self.assertEqual(
                processed_objs[0],
                json.loads(AUTHOR_11111111111_SEARCH_JSON.read_text())[
                    "search-results"
                ]["entry"][0],
            )

    def test_populate_authors(self, m):
        """Test populating authors."""
        with self.subTest("Resource not found"):
            m.get(
                AUTHOR_SEARCH_BASE_URL.format("AU-ID", self.author_1_id),
                json=json.loads(AUTHOR_1_SEARCH_JSON.read_text()),
            )
            processed_objs = ScopusAuthor.populate_authors([self.author_1_id])[0]
            self.assertEqual([(o.author_id, o.data) for o in processed_objs], [])
            self.assertQuerySetEqual(
                ScopusAuthor.objects.values_list("author_id", flat=True),
                [],
            )
        m.get(
            AUTHOR_SEARCH_BASE_URL.format("ORCID", self.author_11111111111_orcid_id),
            json=json.loads(AUTHOR_11111111111_SEARCH_JSON.read_text()),
        )
        m.get(
            AUTHOR_SEARCH_BASE_URL.format("AU-ID", self.author_11111111111_id),
            json=json.loads(AUTHOR_11111111111_SEARCH_JSON.read_text()),
        )
        with self.subTest("Create objects"):
            processed_objs = ScopusAuthor.populate_authors(
                [self.author_11111111111_id, self.author_11111111111_orcid_id]
            )[0]
            self.assertEqual(
                [(o.author_id, o.data) for o in processed_objs],
                [
                    (
                        self.author_11111111111_id,
                        json.loads(AUTHOR_11111111111_SEARCH_JSON.read_text())[
                            "search-results"
                        ]["entry"][0],
                    )
                ],
            )
            self.assertQuerySetEqual(
                ScopusAuthor.objects.values_list("author_id", flat=True),
                [self.author_11111111111_id],
            )
        with self.subTest("Update objects"):
            processed_objs = ScopusAuthor.populate_authors(
                [self.author_11111111111_id]
            )[0]
            self.assertEqual(
                [(o.author_id, o.data) for o in processed_objs],
                [
                    (
                        self.author_11111111111_id,
                        json.loads(AUTHOR_11111111111_SEARCH_JSON.read_text())[
                            "search-results"
                        ]["entry"][0],
                    )
                ],
            )
            self.assertQuerySetEqual(
                ScopusAuthor.objects.values_list("author_id", flat=True),
                [self.author_11111111111_id],
            )
        with self.subTest("Update objects with duplicated input author ids"):
            processed_objs = ScopusAuthor.populate_authors(
                [self.author_11111111111_id, self.author_11111111111_orcid_id]
            )[0]
            self.assertEqual(
                [(o.author_id, o.data) for o in processed_objs],
                [
                    (
                        self.author_11111111111_id,
                        json.loads(AUTHOR_11111111111_SEARCH_JSON.read_text())[
                            "search-results"
                        ]["entry"][0],
                    )
                ],
            )
            self.assertQuerySetEqual(
                ScopusAuthor.objects.values_list("author_id", flat=True),
                [self.author_11111111111_id],
            )

    def test_fetch_documents_results(self, m):
        """Test fetching documents results."""
        m.get(
            SCOPUS_SEARCH_BASE_URL.format("AU-ID", self.author_11111111111_id),
            json=json.loads(AUTHOR_11111111111_DOCUMENTS_JSON.read_text()),
        )
        documents_response = ScopusAuthor.fetch_documents_results(
            self.author_11111111111_id
        )
        self.assertEqual(len(documents_response), 4)


class ScopusDocumentTest(TestCase):
    """Test the ScopusDocument model."""

    def test_str(self):
        """Test returning the string representation of an instance."""
        document = ScopusDocument(
            doi="99.9999/999-9-999-99999-9_99",
            data={
                "doi": "99.9999/999-9-999-99999-9_99",
                "title": "The superfluid vacuum theory",
                "description": "Superfluid vacuum theory (SVT), sometimes known as "
                "the BEC vacuum theory, is an approach in theoretical physics and "
                "quantum mechanics where the fundamental physical vacuum "
                "(non-removable background) is considered as a superfluid or as a "
                "Bose-Einstein condensate (BEC).",
            },
        )
        self.assertEqual(document.__str__(), "99.9999/999-9-999-99999-9_99")

    def test_populate_documents(self):
        """Test popluate_documents method."""
        documents = [
            ScopusDocument(
                doi="99.9999/999-9-999-99999-8_88",
                data={
                    "doi": "99.9999/999-9-999-99999-8_88",
                    "title": "Lorem ipsum",
                    "description": "Lorem ipsum dolor sit amet, consectetur "
                    "adipiscing elit, sed do eiusmod tempor incididunt ut labore "
                    "et dolore magna aliqua.",
                },
            ),
            ScopusDocument(
                doi="99.9999/999-9-999-99999-7_77",
                data={
                    "doi": "99.9999/999-9-999-99999-7_77",
                    "title": "Lorem ipsum",
                    "description": "Lorem ipsum dolor sit amet, consectetur "
                    "adipiscing elit, sed do eiusmod tempor incididunt ut labore "
                    "et dolore magna aliqua.",
                },
            ),
            ScopusDocument(
                doi="99.9999/999-9-999-99999-6_66",
                data={
                    "doi": "99.9999/999-9-999-99999-6_66",
                    "title": "Lorem ipsum",
                    "description": "Lorem ipsum dolor sit amet, consectetur "
                    "adipiscing elit, sed do eiusmod tempor incididunt ut labore "
                    "et dolore magna aliqua.",
                },
            ),
            ScopusDocument(
                doi="99.9999/999-9-999-99999-5_55",
                data={
                    "doi": "99.9999/999-9-999-99999-5_55",
                    "title": "Lorem ipsum",
                    "description": "Lorem ipsum dolor sit amet, consectetur "
                    "adipiscing elit, sed do eiusmod tempor incididunt ut labore "
                    "et dolore magna aliqua.",
                },
            ),
        ]
        author_documents = ScopusDocument.populate_documents(documents)
        self.assertEqual(len(author_documents), 4)

    def test_author_ids(self):
        """Test author_ids property."""
        document = ScopusDocument(
            doi="99.9999/999-9-999-99999-8_88",
            data={
                "doi": "99.9999/999-9-999-99999-8_88",
                "title": "Lorem ipsum",
                "description": "Lorem ipsum dolor sit amet, consectetur "
                "adipiscing elit, sed do eiusmod tempor incididunt ut labore "
                "et dolore magna aliqua.",
                "author_ids": "11111111111;22222222222;33333333333",
            },
        )
        self.assertEqual(
            document.author_ids, ["11111111111", "22222222222", "33333333333"]
        )
        document = ScopusDocument(
            doi="99.9999/999-9-999-99999-8_88",
            data={
                "doi": "99.9999/999-9-999-99999-8_88",
                "title": "Lorem ipsum",
                "description": "Lorem ipsum dolor sit amet, consectetur "
                "adipiscing elit, sed do eiusmod tempor incididunt ut labore "
                "et dolore magna aliqua.",
                "author_ids": None,
            },
        )
        self.assertEqual(document.author_ids, [])
