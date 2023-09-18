"""Scopus app management commands for importing authors."""

from collections import Counter
from pathlib import Path

from django.core.management import BaseCommand

from scopus.models import ScopusAuthor
from scopus.utils import is_orcid_id


class Command(BaseCommand):
    """A command for importing authors from Scopus."""

    def add_arguments(self, parser):
        """Add custom arguments."""
        parser.add_argument("--ids", dest="ids", nargs="+", type=int, required=False)
        parser.add_argument(
            "--author-paths", dest="author_paths", nargs="+", type=Path, required=False
        )
        parser.add_argument("--populate-documents", action="store_true", required=False)

    def get_ids_per_type(self, ids: list[str | int]):
        """Return ids per type."""
        author_ids = []
        orcid_ids = []
        for _id in ids:
            if is_orcid_id(_id):
                orcid_ids.append(_id)
            else:
                author_ids.append(int(_id))
        return author_ids, orcid_ids

    def prepare_ids(self, ids: list[int | str], author_paths: list[Path]):
        """Prepare ids for import."""
        if ids is None:
            ids = []
        author_ids, orcid_ids = self.get_ids_per_type(ids)
        if author_paths:
            ids = [
                line
                for author_path in author_paths
                for line in author_path.read_text().splitlines()
            ]
            extra_author_ids, extra_orcid_ids = self.get_ids_per_type(ids)
            author_ids.extend(extra_author_ids)
            orcid_ids.extend(extra_orcid_ids)
        return author_ids, orcid_ids

    def process_authors(
        self,
        ids: list[int | str],
        verbose: bool = False,
        populate_documents: bool = False,
    ):
        """Process authors."""
        if is_orcid_id(ids[0]):
            id_label = "ORCID id"
        else:
            id_label = "author id"
        verbose and self.stdout.write(f"{len(ids)} {id_label}s about to be processed.")
        duplicates = ",".join(sorted(str(k) for k, v in Counter(ids).items() if v > 1))
        verbose and duplicates and self.stdout.write(
            self.style.WARNING(f"Duplicate {id_label}s: {duplicates}.")
        )
        processed_authors, processed_documents = ScopusAuthor.populate_authors(
            ids, populate_documents
        )
        processed_ids = [
            author.author_id if author.author_id in ids else author.orcid
            for author in processed_authors
        ]
        unprocessed_ids = set(ids).difference(processed_ids)
        unprocessed_str = ",".join(map(str, unprocessed_ids))
        verbose and unprocessed_ids and self.stdout.write(
            self.style.ERROR(
                f"{len(unprocessed_ids)} authors unsuccessfully processed "
                f"({unprocessed_str})."
            )
        )
        verbose and self.stdout.write(
            self.style.SUCCESS(
                f"{len(processed_authors)} authors successfully processed.\n"
                f"{len(processed_documents)} documents successfully processed."
            )
        )

    def handle(
        self,
        ids: list[int | str],
        author_paths: list[Path],
        verbosity: bool,
        **kwargs,
    ):
        """Import authors from Scopus."""
        verbose = verbosity >= 2
        author_ids, orcid_ids = self.prepare_ids(ids, author_paths)
        if author_ids:
            self.process_authors(
                author_ids, verbose, kwargs.get("populate_documents", False)
            )
        else:
            verbose and self.stdout.write(self.style.WARNING("No author ids."))
        if orcid_ids:
            self.process_authors(
                orcid_ids, verbose, kwargs.get("populate_documents", False)
            )
        else:
            verbose and self.stdout.write(self.style.WARNING("No ORCID ids."))
