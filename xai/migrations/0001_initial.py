from django.conf import settings
from django.db import migrations
from qdrant_client import models

from connect.qdrant import cli as qdrant_cli


def create_collection(apps, schema_editor):  # pragma: nocover
    qdrant_cli.create_collection(
        collection_name=settings.QDRANT_DOCUMENTS_COLLECTION,
        vectors_config=models.VectorParams(
            size=settings.QDRANT_VECTOR_SIZE, distance=models.Distance.COSINE
        ),
    )


def delete_collection(apps, schema_editor):  # pragma: nocover
    qdrant_cli.delete_collection(collection_name=settings.QDRANT_DOCUMENTS_COLLECTION)


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("scopus", "0002_scopusdocument"),
    ]

    operations = [
        migrations.RunPython(create_collection, delete_collection),
    ]
