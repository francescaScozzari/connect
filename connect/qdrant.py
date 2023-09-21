"""The main app qdrant client configuration."""

from django.conf import settings
from qdrant_client import QdrantClient, models

cli = QdrantClient(
    url=settings.QDRANT_URL,
    api_key=settings.QDRANT_API_KEY,
    location=settings.QDRANT_LOCATION or None,
    timeout=settings.QDRANT_TIMEOUT,
)


def create_collection():  # pragma: nocover
    """Create a qdrant collection."""
    cli.create_collection(
        collection_name=settings.QDRANT_DOCUMENTS_COLLECTION,
        vectors_config=models.VectorParams(
            size=settings.QDRANT_VECTOR_SIZE, distance=models.Distance.COSINE
        ),
    )


def delete_collection():  # pragma: nocover
    """Delete a qdrant collection."""
    cli.delete_collection(collection_name=settings.QDRANT_DOCUMENTS_COLLECTION)
