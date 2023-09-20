"""Explainable Artificial Intelligence admin."""

from django.contrib import admin

from xai.models import TokensEmbeddings


@admin.register(TokensEmbeddings)
class TokensEmbeddingsAdmin(admin.ModelAdmin):
    """Explainable Artificial Intelligence tokens embeddings admin."""

    list_display = ("document",)
    list_select_related = ("document",)
    list_per_page = 25
    readonly_fields = ("document", "data")
