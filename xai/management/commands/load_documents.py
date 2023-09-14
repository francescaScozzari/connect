"""
Explainable Artificial Intelligence management command.

This command handle the embedding generation
and load points to qdrant the vector database.
"""

from django.conf import settings
from django.core.management import BaseCommand

from scopus.models import ScopusAuthor, ScopusDocument
from xai.facade import WriteEmbeddingFacade


class Command(BaseCommand):
    """A command for load documents points to Qdrant."""

    def add_arguments(self, parser):
        """Add custom arguments."""
        parser.add_argument("--limit", dest="limit", type=int, required=False)

    def handle(self, limit, verbosity, **kwargs):
        """Load documents points to qdrant."""
        verbose = verbosity >= 2
        facade = WriteEmbeddingFacade()
        all_documents = ScopusDocument.objects.order_by("id").all()[:limit]
        verbose and self.stdout.write(
            f"Start loading {all_documents.count()} documents to qdrant."
        )
        loaded_points = 0
        connect_author_ids = ScopusAuthor.objects.all().values_list(
            "author_id", flat=True
        )
        for document in all_documents:
            document_point = facade.generate_document_point(
                document, connect_author_ids
            )
            verbose and bool(document_point) and self.stdout.write(
                f"Point for document {document.id} generated successfully."
            )
            load_response = facade.load_document_point(
                point=document_point,
                collection_name=settings.QDRANT_DOCUMENTS_COLLECTION,
            )
            if load_response.status == "completed":
                verbose and self.stdout.write(
                    f"Point {document.id} loaded successfully."
                )
                loaded_points += 1
        self.stdout.write(
            self.style.SUCCESS(f"TOT {loaded_points} points loaded successfully.")
        )
