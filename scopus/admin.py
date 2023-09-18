"""Scopus admin."""

from django.contrib import admin

from scopus.models import ScopusAuthor, ScopusDocument


@admin.register(ScopusAuthor)
class ScopusAuthorAdmin(admin.ModelAdmin):
    """Scopus author's admin."""

    list_display = ("author_id", "full_name", "university", "orcid")
    search_fields = ("author_id",)
    readonly_fields = ("author_id", "data", "full_name", "university", "orcid")


@admin.register(ScopusDocument)
class ScopusDocumentAdmin(admin.ModelAdmin):
    """Scopus document's admin."""

    list_display = ("doi", "title")
    search_fields = ("doi",)
    readonly_fields = ("doi", "data", "title", "description")
