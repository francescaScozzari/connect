"""Universities models."""
from django.db import models


class University(models.Model):
    """An University."""

    name = models.CharField(unique=True)

    def __str__(self):
        """Return the instance string representation."""
        return self.name


class Author(models.Model):
    """An author."""

    orcid = models.CharField(max_length=19, unique=True)
    full_name = models.CharField()
    university = models.ForeignKey(
        "University", related_name="authors", on_delete=models.PROTECT
    )

    def __str__(self):
        """Return the instance string representation."""
        return self.full_name


class Document(models.Model):
    """A document."""

    doi = models.CharField(unique=True)
    title = models.CharField()
    description = models.TextField()
    authors = models.ManyToManyField("Author", related_name="documents")

    def __str__(self):
        """Return the instance string representation."""
        return self.title

    @property
    def authors_names(self):
        """Return document's author names."""
        return ", ".join(sorted(author.full_name for author in self.authors.all()))
