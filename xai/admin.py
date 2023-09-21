"""Explainable Artificial Intelligence admin."""

from django.contrib import admin

from xai.models import TokensEmbeddings


@admin.register(TokensEmbeddings)
class TokensEmbeddingsAdmin(admin.ModelAdmin):
    """Explainable Artificial Intelligence tokens embeddings admin."""

    list_display = ("document",)
    readonly_fields = ("document", "data")
    search_fields = ("document__exact",)
    show_full_result_count = False
    sortable_by: list = []
    view_on_site = False

    def get_queryset(self, request):
        """Return a QuerySet."""
        queryset = (
            super()
            .get_queryset(request)
            .select_related("document")
            .defer("document__data")
        )
        if request.resolver_match.func.__name__ == "changelist_view":
            queryset = queryset.defer("data")
        return queryset
