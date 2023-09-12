"""The main app commons utils for testing."""

from importlib import import_module

from django.apps import apps
from django.conf import settings
from django.db import connection

qdrant_migration = import_module("xai.migrations.0001_initial")


class SetUpQdrantMixin:
    """A test case supporting media directories creation and cleanup."""

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
