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
            author = AuthorRetrieval(author_id)
        except ScopusException:
            return None
        else:
            return cls(author_id=author_id, data=author._json)

    @classmethod
    def populate_authors(cls, author_ids: list[int]):
        """Populate authors."""
        return cls.objects.bulk_create(
            [
                author
                for author_id in set(author_ids)
                if (author := cls.retrieve_author(author_id)) is not None
            ],
            update_conflicts=True,
            update_fields=("data",),
            unique_fields=("author_id",),
        )
