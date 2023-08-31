"""Scopus admin."""

from django.contrib import admin

from scopus.models import ScopusAuthor, ScopusDocument


@admin.register(ScopusAuthor)
class ScopusAuthorAdmin(admin.ModelAdmin):
    """Scopus author's admin."""

    list_display = ("author_id",)


@admin.register(ScopusDocument)
class ScopusDocumentAdmin(admin.ModelAdmin):
    """Scopus document's admin."""

    list_display = ("doi",)
