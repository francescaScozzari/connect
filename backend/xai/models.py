"""Explainable Artificial Intelligence models."""

from django.db import models


class TokensEmbeddings(models.Model):
    """A tokens embeddings."""

    data = models.JSONField(default=list)
    document = models.OneToOneField(
        "scopus.ScopusDocument",
        to_field="doi",
        related_name="tokens",
        on_delete=models.CASCADE,
    )

    class Meta:
        """Django model options."""

        verbose_name = "tokens embeddings"
        verbose_name_plural = "tokens embeddings"

    def __str__(self):
        """Return the instance string representation."""
        return f"TokensEmbeddings for {self.document_id}"
