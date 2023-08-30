"""Test the Scopus app models."""

import json

import requests_mock
from django.test import TestCase

from scopus.models import ScopusAuthor
from scopus.tests import AUTHOR_11111111111_JSON, AUTHOR_BASE_URL


class ScopusAuthorTest(TestCase):
    """Test the ScopusAuthor model."""

    def test_str(self):
        """Test str method."""
        author_11111111111 = ScopusAuthor(
            author_id=11111111111, data={"orcid": "0001-0002-0003-0004"}
        )
        self.assertEqual(author_11111111111.__str__(), "11111111111")

    def test_retrieve_author(self):
        """Test retrieving an author."""
        with requests_mock.Mocker() as m:
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
                self.assertIsInstance(processed_obj, ScopusAuthor)
                self.assertEqual(
                    processed_obj.data, json.loads(AUTHOR_11111111111_JSON.read_text())
                )

    def test_populate_authors(self):
        """Test populating authors."""
        with requests_mock.Mocker() as m:
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
                processed_objs = ScopusAuthor.populate_authors([author_id])
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
                processed_objs = ScopusAuthor.populate_authors([author_id])
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
                processed_objs = ScopusAuthor.populate_authors([author_id])
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
                processed_objs = ScopusAuthor.populate_authors([author_id, author_id])
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
