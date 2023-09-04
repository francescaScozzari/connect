"""Scopus app management commands for importing authors."""

from collections import Counter
from pathlib import Path

from django.core.management import BaseCommand

from scopus.models import ScopusAuthor


class Command(BaseCommand):
    """A command for importing authors from Scopus."""

    def add_arguments(self, parser):
        """Add custom arguments."""
        parser.add_argument(
            "--author-ids", dest="author_ids", nargs="+", type=int, required=False
        )
        parser.add_argument(
            "--author-paths", dest="author_paths", nargs="+", type=Path, required=False
        )
        parser.add_argument("--populate-documents", action="store_true", required=False)

    def handle(self, author_paths, author_ids, verbosity, **kwargs):
        """Import authors from Scopus."""
        if author_ids is None:
            author_ids = []
        verbose = verbosity >= 2
        if author_paths:
            for author_path in author_paths:
                author_ids.extend(list(map(int, author_path.read_text().splitlines())))
        if author_ids:
            verbose and self.stdout.write(
                f"{len(author_ids)} author ids are about to be processed."
            )
            duplicates = ",".join(
                sorted(str(k) for k, v in Counter(author_ids).items() if v > 1)
            )
            verbose and duplicates and self.stdout.write(
                self.style.WARNING(f"Duplicate author ids: {duplicates}.")
            )
            processed_authors, processed_documents = ScopusAuthor.populate_authors(
                author_ids, populate_documents=kwargs.get("populate_documents")
            )
            unprocessed_ids = set(author_ids).difference(
                {a.author_id for a in processed_authors}
            )
            unprocessed_str = ",".join(map(str, unprocessed_ids))
            verbose and unprocessed_ids and self.stdout.write(
                self.style.ERROR(
                    f"{len(unprocessed_ids)} authors unsuccessfully processed "
                    f"[{unprocessed_str}]."
                )
            )
            verbose and self.stdout.write(
                self.style.SUCCESS(
                    f"{len(processed_authors)} authors successfully processed.\n"
                    f"{len(processed_documents)} documents successfully processed."
                )
            )
        else:
            verbose and self.stdout.write(self.style.WARNING("No author ids."))
