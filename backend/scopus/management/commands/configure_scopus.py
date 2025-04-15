"""Scopus app management commands for configuring Scopus."""

from django.conf import settings
from django.core.management import BaseCommand
from pybliometrics.scopus.utils.create_config import create_config


class Command(BaseCommand):
    """A command for configuring Scopus."""

    def handle(self, verbosity, **kwargs):
        """Configure Scopus."""
        create_config(
            keys=settings.SCOPUS_API_KEYS,
            insttoken=settings.SCOPUS_INST_TOKEN,
        )
