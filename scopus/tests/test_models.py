"""Test the Scopus app models."""

import json

import requests_mock
from django.test import TestCase
from pybliometrics.scopus import AuthorRetrieval

from scopus.models import ScopusAuthor, ScopusDocument
from scopus.tests import (
    AUTHOR_11111111111_DOCUMENTS_JSON,
    AUTHOR_11111111111_JSON,
    AUTHOR_BASE_URL,
    SEARCH_AUTHOR_11111111111_URL,
    SEARCH_AUTHOR_11111111111_URL_ENHANCED,
)


@requests_mock.Mocker()
class ScopusAuthorTest(TestCase):
    """Test the ScopusAuthor model."""

    def test_str(self, m):
        """Test str method."""
        author_11111111111 = ScopusAuthor(
            author_id=11111111111, data={"orcid": "0001-0002-0003-0004"}
        )
        self.assertEqual(author_11111111111.__str__(), "11111111111")

    def test_retrieve_author(self, m):
        """Test retrieving an author."""
        with self.subTest("Resource not found"):
            author_id = 1
            m.get(
                f"{AUTHOR_BASE_URL}/{author_id}",
                status_code=404,
                json={
                    "service-error": {
                        "status": {
                            "statusCode": "RESOURCE_NOT_FOUND",
                            "statusText": "The resource specified cannot be found.",
                        }
                    }
                },
            )
            self.assertIsNone(ScopusAuthor.retrieve_author(author_id))
        with self.subTest("Resource found"):
            author_id = 11111111111
            m.get(
                f"{AUTHOR_BASE_URL}/{author_id}",
                json={
                    "author-retrieval-response": [
                        json.loads(AUTHOR_11111111111_JSON.read_text())
                    ]
                },
            )
            processed_obj = ScopusAuthor.retrieve_author(author_id)
            self.assertIsInstance(processed_obj, AuthorRetrieval)
            self.assertEqual(
                processed_obj._json, json.loads(AUTHOR_11111111111_JSON.read_text())
            )
        with self.subTest("Resource id not numerical"):
            self.assertIsNone(ScopusAuthor.retrieve_author("A"))

    def test_populate_authors(self, m):
        """Test populating authors."""
        with self.subTest("Resource not found"):
            author_id = 1
            m.get(
                f"{AUTHOR_BASE_URL}/{author_id}",
                status_code=404,
                json={
                    "service-error": {
                        "status": {
                            "statusCode": "RESOURCE_NOT_FOUND",
                            "statusText": "The resource specified cannot be found.",
                        }
                    }
                },
            )
            processed_objs = ScopusAuthor.populate_authors([author_id])[0]
            self.assertEqual([(o.author_id, o.data) for o in processed_objs], [])
            self.assertQuerySetEqual(
                ScopusAuthor.objects.values_list("author_id", flat=True),
                [],
            )
        author_id = 11111111111
        m.get(
            f"{AUTHOR_BASE_URL}/{author_id}",
            json={
                "author-retrieval-response": [
                    json.loads(AUTHOR_11111111111_JSON.read_text())
                ]
            },
        )
        with self.subTest("Create objects"):
            processed_objs = ScopusAuthor.populate_authors([author_id])[0]
            self.assertEqual(
                [(o.author_id, o.data) for o in processed_objs],
                [
                    (
                        11111111111,
                        json.loads(AUTHOR_11111111111_JSON.read_text()),
                    )
                ],
            )
            self.assertQuerySetEqual(
                ScopusAuthor.objects.values_list("author_id", flat=True),
                [11111111111],
            )
        with self.subTest("Update objects"):
            processed_objs = ScopusAuthor.populate_authors([author_id])[0]
            self.assertEqual(
                [(o.author_id, o.data) for o in processed_objs],
                [
                    (
                        11111111111,
                        json.loads(AUTHOR_11111111111_JSON.read_text()),
                    )
                ],
            )
            self.assertQuerySetEqual(
                ScopusAuthor.objects.values_list("author_id", flat=True),
                [11111111111],
            )
        with self.subTest("Update objects with duplicated input author ids"):
            processed_objs = ScopusAuthor.populate_authors([author_id, author_id])[0]
            self.assertEqual(
                [(o.author_id, o.data) for o in processed_objs],
                [
                    (
                        11111111111,
                        json.loads(AUTHOR_11111111111_JSON.read_text()),
                    )
                ],
            )
            self.assertQuerySetEqual(
                ScopusAuthor.objects.values_list("author_id", flat=True),
                [11111111111],
            )

    def test_get_documents(self, m):
        """Test get_documents method."""
        author_id = 11111111111
        m.get(
            SEARCH_AUTHOR_11111111111_URL,
            json=json.loads(AUTHOR_11111111111_DOCUMENTS_JSON.read_text()),
        )
        m.get(
            SEARCH_AUTHOR_11111111111_URL_ENHANCED,
            json=json.loads(AUTHOR_11111111111_DOCUMENTS_JSON.read_text()),
        )
        documents_response = ScopusAuthor(
            author_id=author_id, data={"author_id": author_id}
        ).get_documents()
        self.assertIsNotNone(documents_response)
        self.assertEqual(len(documents_response), 4)


class ScopusDocumentTest(TestCase):
    """Test the ScopusDocument model."""

    def test_str(self):
        """Test str method."""
        document = ScopusDocument(
            doi="99.9999/999-9-999-99999-9_99",
            data={
                "doi": "99.9999/999-9-999-99999-9_99",
                "title": "The superfluid vacuum theory",
                "description": "Superfluid vacuum theory (SVT), sometimes known as "
                "the BEC vacuum theory, is an approach in theoretical physics and "
                "quantum mechanics where the fundamental physical vacuum "
                "(non-removable background) is considered as a superfluid or as a "
                "Bose–Einstein condensate (BEC).",
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
