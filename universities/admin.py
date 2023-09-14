"""The universities app admin."""

from django.contrib import admin

from universities.models import Author, Document, University


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    """University's admin."""

    list_display = ("name",)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Author's admin."""

    list_display = ("orcid", "full_name", "university")
    list_select_related = ["university"]


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """Document's admin."""

    list_display = ("doi", "title", "authors_names")
