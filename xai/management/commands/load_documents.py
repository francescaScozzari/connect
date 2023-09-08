"""
Explainable Artificial Intelligence management command.

This command handle the embedding generation
and load points to qdrant the vector database.
"""

from django.conf import settings
from django.core.management import BaseCommand

from scopus.models import ScopusDocument
from xai.facade import WriteEmbeddingFacade


class Command(BaseCommand):
    """A command for configuring Scopus."""

    def handle(self, verbosity, **kwargs):
        """Load documents to qdrant."""
        verbose = verbosity >= 2
        facade = WriteEmbeddingFacade()
        all_documents = ScopusDocument.objects.order_by("id").all()
        loaded_points = 0
        for document in all_documents:
            document_point = facade.generate_document_point(document)
            verbose and bool(document_point) and self.stdout.write(
                self.style.INFO(
                    f"Point for document {document.id} generated succesfully."
                )
            )
            load_response = facade.load_document_point(
                point=document_point,
                collection_name=settings.QDRANT_DOCUMENTS_COLLECTION,
            )
            if load_response.status == "completed":
                verbose and self.stdout.write(
                    self.style.INFO(f"Point {document.id} loaded succesfully.")
                )
                loaded_points += 1
        self.stdout.write(
            self.style.SUCCESS(f"TOT {loaded_points} loaded succesfully.")
        )
