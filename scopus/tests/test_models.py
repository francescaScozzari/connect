"""Test the Scopus app models."""

import json
from unittest import skip
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

    @classmethod
    def setUpTestData(cls):
        """Prepare initial data for testing."""
        cls.scopus_author1 = ScopusAuthor(
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
        )
        cls.scopus_author2 = ScopusAuthor(
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
        )
        cls.scopus_author3 = ScopusAuthor(
            author_id="33333333333",
            data={
                "eid": "0-s0.0-33333333333",
                "orcid": "0000-0000-0000-0003",
                "dc:identifier": "AUTHOR_ID:33333333333",
                "preferred-name": {"surname": "Wolowitz", "given-name": "Howard"},
                "affiliation-current": {
                    "affiliation-name": "Massachusetts Institute of Technology",
                },
            },
        )

    def test_str(self, m):
        """Test returning the string representation of an instance."""
        self.assertEqual(self.scopus_author1.__str__(), "11111111111")
        author_retrieval_11111111111 = ScopusAuthor(
            author_id=self.author_11111111111_id, data={"orcid": "0001-0002-0003-0004"}
        )
        self.assertEqual(author_retrieval_11111111111.__str__(), "11111111111")

    # FIXME
    @skip("Flaky test")
    def test_fetch_authors_results_not_found(self, m):  # pragma: no cover
        """Test fetching authors results not found."""
        m.get(
            AUTHOR_SEARCH_BASE_URL.format("AU-ID", self.author_1_id),
            json=json.loads(AUTHOR_1_SEARCH_JSON.read_text()),
        )
        self.assertEqual(ScopusAuthor.fetch_authors_results(self.author_1_id), [])

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

    def test_full_name(self, m):
        """Test full_name property."""
        self.assertEqual(self.scopus_author1.full_name, "Sheldon Lee Cooper")
        self.assertEqual(self.scopus_author2.full_name, "Leonard Hofstadter")
        self.assertEqual(self.scopus_author3.full_name, "Howard Wolowitz")

    def test_university(self, m):
        """Test univeresity property."""
        self.assertEqual(self.scopus_author1.university, "East Texas Tech University")
        self.assertEqual(self.scopus_author2.university, "")
        self.assertEqual(
            self.scopus_author3.university, "Massachusetts Institute of Technology"
        )
        parent_uni = ScopusAuthor(
            data={
                "author-profile": {
                    "affiliation-current": {
                        "affiliation": {
                            "ip-doc": {
                                "sort-name": "Massachusetts Institute of Technology",
                                "afdispname": "MIT - Computer Science Department",
                                "preferred-name": {"$": "Computer Science Department"},
                                "parent-preferred-name": {"$": "MIT"},
                            }
                        }
                    }
                }
            }
        )
        self.assertEqual(parent_uni.university, "MIT")
        preferred_uni = ScopusAuthor(
            data={
                "author-profile": {
                    "affiliation-current": {
                        "affiliation": {
                            "ip-doc": {
                                "sort-name": "Massachusetts Institute of Technology",
                                "afdispname": "MIT - Computer Science Department",
                                "preferred-name": {"$": "Computer Science Department"},
                            }
                        }
                    }
                }
            }
        )
        self.assertEqual(preferred_uni.university, "Computer Science Department")
        sort_uni = ScopusAuthor(
            data={
                "author-profile": {
                    "affiliation-current": {
                        "affiliation": {
                            "ip-doc": {
                                "sort-name": "Massachusetts Institute of Technology",
                                "afdispname": "MIT - Computer Science Department",
                            }
                        }
                    }
                }
            }
        )
        self.assertEqual(sort_uni.university, "Massachusetts Institute of Technology")
        afdispname_uni = ScopusAuthor(
            data={
                "author-profile": {
                    "affiliation-current": {
                        "affiliation": {
                            "ip-doc": {
                                "afdispname": "MIT - Computer Science Department",
                            }
                        }
                    }
                }
            }
        )
        self.assertEqual(afdispname_uni.university, "MIT - Computer Science Department")
        multiple_uni = ScopusAuthor(
            data={
                "author-profile": {
                    "affiliation-current": {
                        "affiliation": [
                            {
                                "ip-doc": {
                                    "afdispname": "MIT",
                                }
                            },
                            {
                                "ip-doc": {
                                    "afdispname": "Harvard",
                                }
                            },
                        ]
                    }
                }
            }
        )
        self.assertEqual(multiple_uni.university, "Harvard / MIT")

    def test_orcid(self, m):
        """Test orcid property."""
        self.assertEqual(self.scopus_author1.orcid, "0000-0000-0000-0001")
        self.assertEqual(self.scopus_author2.orcid, "")
        self.assertEqual(self.scopus_author3.orcid, "0000-0000-0000-0003")


class ScopusDocumentTest(TestCase):
    """Test the ScopusDocument model."""

    def test_str(self):
        """Test returning the string representation of an instance."""
        document_99 = ScopusDocument(
            doi="99.9999/999-9-999-99999-9_99",
            data={
                "doi": "99.9999/999-9-999-99999-9_99",
                "title": "The superfluid vacuum theory",
                "description": "Superfluid vacuum theory (SVT), or BEC vacuum theory.",
            },
        )
        self.assertEqual(document_99.__str__(), "99.9999/999-9-999-99999-9_99")

    def test_populate_documents(self):
        """Test popluate_documents method."""
        documents = [
            ScopusDocument(
                doi="99.9999/999-9-999-99999-8_88",
                data={
                    "doi": "99.9999/999-9-999-99999-8_88",
                    "title": "Lorem ipsum",
                    "description": "Dolor sit amet.",
                },
            ),
            ScopusDocument(
                doi="99.9999/999-9-999-99999-7_77",
                data={
                    "doi": "99.9999/999-9-999-99999-7_77",
                    "title": "Consectetur adipiscing",
                    "description": "Elit sed do eiusmodtempor.",
                },
            ),
            ScopusDocument(
                doi="99.9999/999-9-999-99999-6_66",
                data={
                    "doi": "99.9999/999-9-999-99999-6_66",
                    "title": "Incididunt ut labore",
                    "description": "Et dolore magna aliqua.",
                },
            ),
            ScopusDocument(
                doi="99.9999/999-9-999-99999-5_55",
                data={
                    "doi": "99.9999/999-9-999-99999-5_55",
                    "title": "Ut enim ad minim veniam",
                    "description": ",Quis nostrud exercitation ullamco.",
                },
            ),
        ]
        author_documents = ScopusDocument.populate_documents(documents)
        self.assertEqual(len(author_documents), 4)

    def test_author_ids(self):
        """Test author_ids property."""
        document_44 = ScopusDocument(
            doi="99.9999/999-9-999-99999-4_44",
            data={
                "doi": "99.9999/999-9-999-99999-4_44",
                "title": "Laboris nisi",
                "description": "Ut aliquip ex ea commodo consequat.",
                "author_ids": "11111111111;22222222222;33333333333",
            },
        )
        self.assertEqual(
            document_44.author_ids, ["11111111111", "22222222222", "33333333333"]
        )
        document_33 = ScopusDocument(
            doi="99.9999/999-9-999-99999-3_33",
            data={
                "doi": "99.9999/999-9-999-99999-3_33",
                "title": "Duis aute",
                "description": "Irure dolor in reprehenderit.",
                "author_ids": None,
            },
        )
        self.assertEqual(document_33.author_ids, [])

    def test_title(self):
        """Test title property."""
        document_22_a = ScopusDocument(
            doi="99.9999/999-9-999-99999-2_22",
            data={
                "doi": "99.9999/999-9-999-99999-2_22",
                "title": "In voluptate",
                "description": "Velit esse cillum dolore.",
            },
        )
        self.assertEqual(document_22_a.title, "In voluptate")
        document_22_b = ScopusDocument(
            doi="99.9999/999-9-999-99999-2_22",
            data={
                "doi": "99.9999/999-9-999-99999-2_22",
                "dc:title": "In voluptate",
                "dc:description": "Velit esse cillum dolore.",
            },
        )
        self.assertEqual(document_22_b.title, "In voluptate")
        document_22_c = ScopusDocument(doi="99.9999/999-9-999-99999-2_22", data={})
        self.assertEqual(document_22_c.title, "")

    def test_description(self):
        """Test description property."""
        document_11_a = ScopusDocument(
            doi="99.9999/999-9-999-99999-1_11",
            data={
                "doi": "99.9999/999-9-999-99999-1_11",
                "title": "Eu fugiat",
                "description": "Nulla pariatur. Excepteur sint.",
            },
        )
        self.assertEqual(document_11_a.description, "Nulla pariatur. Excepteur sint.")
        document_11_b = ScopusDocument(
            doi="99.9999/999-9-999-99999-1_11",
            data={
                "doi": "99.9999/999-9-999-99999-1_11",
                "dc:title": "Eu fugiat",
                "dc:description": "Nulla pariatur. Excepteur sint.",
            },
        )
        self.assertEqual(document_11_b.description, "Nulla pariatur. Excepteur sint.")
        document_11_c = ScopusDocument(doi="99.9999/999-9-999-99999-1_11", data={})
        self.assertEqual(document_11_c.description, "")
