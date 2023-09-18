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

    @property
    def full_name(self):
        """Return the full name."""
        try:
            data = self.data["author-profile"]
        except KeyError:
            data = self.data
        preferred_name_data = data.get("preferred-name", {})
        given_name = preferred_name_data.get("given-name", "")
        surname = preferred_name_data.get("surname", "")
        return f"{given_name} {surname}".strip()

    @property
    def university(self):
        """Return the university."""
        try:
            affiliation_name = self.data["affiliation-current"]["affiliation-name"]
        except KeyError:
            affiliation_name = ""
        if not affiliation_name:
            affiliation = (
                self.data.get("author-profile", {})
                .get("affiliation-current", {})
                .get("affiliation", {})
            )
            try:
                ipdocs = [affiliation.get("ip-doc", {})]
            except AttributeError:
                ipdocs = [i for a in affiliation if (i := a.get("ip-doc", {}))]
            names = []
            for ipdoc in ipdocs:
                name = (
                    ipdoc.get("parent-preferred-name", {}).get("$", "")
                    or ipdoc.get("preferred-name", {}).get("$", "")
                    or ipdoc.get("sort-name", "")
                    or ipdoc.get("afdispname", "")
                )
                if name:
                    names.append(name)
            affiliation_name = " / ".join(sorted(names))
        return affiliation_name

    @property
    def orcid(self):
        """Return the orcid."""
        try:
            data = self.data["coredata"]
        except KeyError:
            data = self.data
        return data.get("orcid", "")


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

    @property
    def title(self):
        """Return the title."""
        return self.data.get("title", "") or self.data.get("dc:title", "")

    @property
    def description(self):
        """Return the description."""
        return self.data.get("description", "") or self.data.get("dc:description", "")
