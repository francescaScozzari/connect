from django.db import migrations
from connect.qdrant import cli as qdrant_cli
from django.conf import settings
from connect.qdrant import (
    create_collection as qdrant_create_collection,
    delete_collection as qdrant_delete_collection,
)
from qdrant_client import models


def create_collection(apps, schema_editor):  # pragma: nocover
    """Create a qdrant collection."""
    qdrant_create_collection()


def delete_collection(apps, schema_editor):  # pragma: nocover
    """Delete a qdrant collection."""
    qdrant_delete_collection()


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("scopus", "0002_scopusdocument"),
    ]

    operations = [
        migrations.RunPython(create_collection, delete_collection),
    ]
