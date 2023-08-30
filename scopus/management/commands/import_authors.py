"""Scopus app management commands for importing authors."""

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
        processed_authors = ScopusAuthor.populate_authors(author_ids)
        verbosity >= 2 and self.stdout.write(
            self.style.SUCCESS(
                f"{len(processed_authors)} authors successfully processed."
            )
        )
