"""Scopus models."""

from json.decoder import JSONDecodeError
from typing import ValuesView

from django.db import models
from pybliometrics.scopus import AuthorSearch, ScopusSearch
from pybliometrics.scopus.exception import ScopusException

from scopus.utils import is_orcid_id


class ScopusAuthor(models.Model):
    """A Scopus author."""

    author_id = models.PositiveBigIntegerField(unique=True)
    data = models.JSONField()

    def __str__(self):
        """Return the instance string representation."""
        return f"{self.author_id}"

    @classmethod
    def fetch_authors_results(cls, _id: str | int):
        """Fetch authors results by provided id."""
        query_func = "ORCID" if is_orcid_id(_id) else "AU-ID"
        try:
            return AuthorSearch(query=f"{query_func}({_id})")._json
        except (ScopusException, JSONDecodeError):
            return []

    @classmethod
    def populate_authors(cls, ids: list[int | str], populate_documents: bool = False):
        """Populate authors."""
        authors: dict = {}
        documents: dict = {}
        for _id in set(ids):
            for result in cls.fetch_authors_results(_id):
                identifier = int(result["dc:identifier"].split(":")[-1])
                authors[identifier] = cls(author_id=identifier, data=result)
                if populate_documents and (
                    author_documents := cls.fetch_documents_results(identifier)
                ):
                    documents |= {
                        prism_doi: ScopusDocument(doi=prism_doi, data=document)
                        for document in author_documents
                        if (prism_doi := document.get("prism:doi"))
                    }
        created_authors = cls.objects.bulk_create(
            authors.values(),
            update_conflicts=True,
            update_fields=("data",),
            unique_fields=("author_id",),
        )
        created_documents = ScopusDocument.populate_documents(documents.values())
        return created_authors, created_documents

    @classmethod
    def fetch_documents_results(cls, _id: int):
        """Fetch documents results by provided author id."""
        return ScopusSearch(f"AU-ID({_id})")._json


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
        return documents and cls.objects.bulk_create(
            documents,
            batch_size=1000,
            update_conflicts=True,
            update_fields=("data",),
            unique_fields=("doi",),
        )

    @property
    def author_ids(self):
        """Return the list of author ids."""
        try:
            return self.data.get("author_ids").split(";")
        except AttributeError:
            return []
