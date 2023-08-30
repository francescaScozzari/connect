"""Scopus admin."""

from django.contrib import admin

from scopus.models import ScopusAuthor


@admin.register(ScopusAuthor)
class ScopusAuthorAdmin(admin.ModelAdmin):
    """Scopus author's admin."""

    list_display = ("author_id",)
