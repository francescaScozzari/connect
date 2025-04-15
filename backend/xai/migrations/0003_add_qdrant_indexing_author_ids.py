from django.db import migrations

from connect.qdrant import (
    create_author_ids_index as qdrant_create_author_ids_index,
    delete_author_ids_index as qdrant_delete_author_ids_index,
)


def create_author_ids_index(apps, schema_editor):  # pragma: nocover
    """Create qdrant indexing for author_ids field."""
    qdrant_create_author_ids_index()


def delete_author_ids_index(apps, schema_editor):  # pragma: nocover
    """Delete qdrant indexing for author_ids field."""
    qdrant_delete_author_ids_index()


class Migration(migrations.Migration):
    dependencies = [
        ("xai", "0002_tokensembeddings"),
    ]

    operations = [
        migrations.RunPython(create_author_ids_index, delete_author_ids_index),
    ]
