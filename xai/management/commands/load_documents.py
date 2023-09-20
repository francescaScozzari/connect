"""
Explainable Artificial Intelligence management command.

This command handle the embedding generation
and load points to qdrant the vector database.
"""

from datetime import datetime

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
        started_at = datetime.now()
        verbose = verbosity >= 2
        all_documents = ScopusDocument.objects.order_by("id").all()[:limit]
        verbose and self.stdout.write(
            f"Start loading {all_documents.count()} documents to qdrant."
        )
        loaded_points = 0
        connect_author_ids = ScopusAuthor.objects.all().values_list(
            "author_id", flat=True
        )
        for document in all_documents:
            facade = WriteEmbeddingFacade(document)
            tokens_embeddings = facade.create_document_tokens_embeddings()
            verbose and bool(tokens_embeddings) and self.stdout.write(
                f"TokensEmbeddings for document {document.doi} generated successfully."
            )
            document_point = facade.generate_document_point(connect_author_ids)
            verbose and bool(document_point) and self.stdout.write(
                f"Point for document {document.doi} generated successfully."
            )
            load_response = WriteEmbeddingFacade.load_document_point(
                point=document_point,
            )
            if load_response.status == "completed":
                verbose and self.stdout.write(
                    f"Point {document.id} loaded successfully."
                )
                loaded_points += 1
        total_time = datetime.now() - started_at
        verbose and self.stdout.write(
            self.style.SUCCESS(f"TOT {loaded_points} points loaded successfully.")
        )
        verbose and self.stdout.write(f"TOTAL execution time: {total_time}")
