"""Scopus models."""

from typing import ValuesView

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
        documents: dict = {}
        for author_id in set(author_ids):
            if (author := cls.retrieve_author(author_id)) is not None:
                authors.append(cls(author_id=author_id, data=author._json))
                if populate_documents and (author_documents := author.get_documents()):
                    documents |= {
                        document.doi: ScopusDocument(
                            doi=document.doi, data=document._asdict()
                        )
                        for document in author_documents
                        if document.doi
                    }
        created_authors = cls.objects.bulk_create(
            authors,
            update_conflicts=True,
            update_fields=("data",),
            unique_fields=("author_id",),
        )
        created_documents = ScopusDocument.populate_documents(documents.values())
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
    def populate_documents(cls, documents: ValuesView):
        """Populate author's documents."""
        BATCH_SIZE = 1000
        return documents and cls.objects.bulk_create(
            documents,
            batch_size=BATCH_SIZE,
            update_conflicts=True,
            update_fields=("data",),
            unique_fields=("doi",),
        )

    @property
    def author_ids(self):
        """Retrun the list of author ids."""
        try:
            return self.data.get("author_ids").split(";")
        except AttributeError:
            return []
