"""
Explainable Artificial Intelligence management command.

This command handle the initial setup of the Large Language Model embedder.
"""

from django.core.management import BaseCommand

from xai.embedder import LLMEmbedder


class Command(BaseCommand):
    """A command for initial setup of the Large Language Model embedder."""

    def handle(self, verbosity, **kwargs):
        """Set up the Large Language Model embedder."""
        LLMEmbedder().initial_setup()
        self.stdout.write(
            self.style.SUCCESS(
                "Large Language Model embedder initialized successfully."
            )
        )
