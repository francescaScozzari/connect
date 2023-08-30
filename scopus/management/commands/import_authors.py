"""Scopus app management commands for importing authors."""

from collections import Counter

from django.core.management import BaseCommand

from scopus.models import ScopusAuthor


class Command(BaseCommand):
    """A command for importing authors from Scopus."""

    def add_arguments(self, parser):
        """Add custom arguments."""
        parser.add_argument(
            "--author-ids", dest="author_ids", nargs="+", type=int, required=True
        )

    def handle(self, author_ids, verbosity, **kwargs):
        """Import authors from Scopus."""
        verbose = verbosity >= 2
        verbose and self.stdout.write(
            f"{len(author_ids)} author ids are about to be processed."
        )
        duplicates = ",".join(
            sorted(str(k) for k, v in Counter(author_ids).items() if v > 1)
        )
        verbose and duplicates and self.stdout.write(
            self.style.WARNING(f"Duplicate author ids: {duplicates}.")
        )
        processed_authors = ScopusAuthor.populate_authors(author_ids)
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
                f"{len(processed_authors)} authors successfully processed."
            )
        )
