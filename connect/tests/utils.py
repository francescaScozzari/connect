"""The main app commons utils for testing."""

from importlib import import_module

from django.apps import apps
from django.conf import settings
from django.db import connection

from scopus.models import ScopusAuthor, ScopusDocument
from xai.facade import SearchMostSimilarFacade, WriteEmbeddingFacade

qdrant_migration = import_module("xai.migrations.0001_initial")


class SetUpQdrantMixin:
    """A mixin to setup qdrant for testing."""

    @classmethod
    def setUpClass(cls):
        """Set up before tests."""
        settings.QDRANT_VECTOR_SIZE = 384
        try:
            qdrant_migration.delete_collection(apps, connection.schema_editor())
            qdrant_migration.create_collection(apps, connection.schema_editor())
        except ValueError:  # pragma: no cover
            pass
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        """Clean up after tests."""
        try:
            qdrant_migration.delete_collection(apps, connection.schema_editor())
        except ValueError:  # pragma: no cover
            pass
        super().tearDownClass()


class ScopusDataMixin:
    """A scopus app data mixin for testing."""

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
        ScopusDocument.objects.bulk_create(cls.scopus_documents)


class XaiDataMixin(ScopusDataMixin):
    """A xai app data mixin for testing."""

    @classmethod
    def setUpTestData(cls):
        """Prepare initial data for testing."""
        ScopusDataMixin.setUpTestData()
        cls.search_facade = SearchMostSimilarFacade(sentence="test has sentence.")
        cls.write_facade = WriteEmbeddingFacade
        cls.document_tokens_embeddings1 = WriteEmbeddingFacade(
            cls.scopus_documents[0]
        ).create_document_tokens_embeddings()
        cls.point1 = WriteEmbeddingFacade(
            cls.scopus_documents[0]
        ).generate_document_point([11111111111, 22222222222])
        cls.document_tokens_embeddings2 = WriteEmbeddingFacade(
            cls.scopus_documents[1]
        ).create_document_tokens_embeddings()
        cls.point2 = WriteEmbeddingFacade(
            cls.scopus_documents[1]
        ).generate_document_point([11111111111, 22222222222])
        cls.point3 = WriteEmbeddingFacade(
            cls.scopus_documents[2]
        ).generate_document_point([11111111111, 22222222222])


class XaiSearchDataMixin(XaiDataMixin):
    """A xai app data mixin for testing search most similar."""

    @classmethod
    def setUpTestData(cls):
        """Prepare initial data for testing."""
        XaiDataMixin.setUpTestData()
        WriteEmbeddingFacade.load_document_point(point=cls.point1)
        WriteEmbeddingFacade.load_document_point(point=cls.point2)
        WriteEmbeddingFacade.load_document_point(point=cls.point3)
