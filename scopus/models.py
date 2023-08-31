"""Scopus models."""

from django.db import models
from pybliometrics.scopus import AuthorRetrieval
from pybliometrics.scopus.exception import ScopusException


class ScopusAuthor(models.Model):
    """A Scopus author."""

    author_id = models.PositiveBigIntegerField(unique=True)
    data = models.JSONField()

    def __str__(self):
        """Return the instance string representation."""
        return f"{self.author_id}"

    @classmethod
    def retrieve_author(cls, author_id: int):
        """Retrieve an author."""
        try:
            return AuthorRetrieval(int(author_id))
        except (ScopusException, ValueError):
            return None

    @classmethod
    def populate_authors(cls, author_ids: list[int], populate_documents: bool = False):
        """Populate authors."""
        authors: list[ScopusAuthor] = []
        created_documents: list[ScopusDocument] = []
        for author_id in set(author_ids):
            author = cls.retrieve_author(author_id)
            if author is not None:
                authors.append(cls(author_id=author_id, data=author._json))
                if populate_documents and (documents := author.get_documents()):
                    docs = {d.doi: d._asdict() for d in documents if d.doi}
                    created_documents.extend(
                        ScopusDocument.populate_documents(
                            [ScopusDocument(doi=k, data=v) for k, v in docs.items()]
                        )
                    )
        created_authors = cls.objects.bulk_create(
            authors,
            update_conflicts=True,
            update_fields=("data",),
            unique_fields=("author_id",),
        )
        return created_authors, created_documents

    def get_documents(self):
        """Get author's documents."""
        return self.retrieve_author(self.author_id).get_documents()


class ScopusDocument(models.Model):
    """A Scopus document."""

    doi = models.CharField(unique=True)
    data = models.JSONField()

    def __str__(self):
        """Return the instance string representation."""
        return f"{self.doi}"

    @classmethod
    def populate_documents(cls, documents: list):
        """Populate author's documents."""
        return documents and cls.objects.bulk_create(
            documents,
            update_conflicts=True,
            update_fields=("data",),
            unique_fields=("doi",),
        )
