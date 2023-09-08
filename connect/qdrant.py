"""The main app qdrant client configuration."""

from django.conf import settings
from qdrant_client import QdrantClient

cli = QdrantClient(
    url=settings.QDRANT_URL,
    api_key=settings.QDRANT_API_KEY,
    location=settings.QDRANT_LOCATION or None,
)
