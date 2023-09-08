"""Explainable Artificial Intelligence facade."""

from qdrant_client.http import models

from connect.qdrant import cli as qdrant_cli
from scopus.models import ScopusDocument
from xai import TOKEN_KEY
from xai.embedder import LLMEmbedder
from xai.textprocessor import process_text


class WriteEmbeddingFacade:
    """The write embedding xai class."""

    def merge_title_and_description(
        self, title: str, description: str, merging_sym: str = "."
    ) -> list[str]:
        """
        Merge two strings into a single one with this pattern.

        title<symbol> description
        :param merging_sym: Symbol used to merge. Default value is "."
        :param description: String on the right of the result
        :param title: String on the left of the result
        :return: merged string.
        """
        return [f"{title}{merging_sym} {description}"]

    def generate_document_point(self, document: ScopusDocument):
        """
        Generate document points.

        :param documents: List of dict.
        :return: List of PointStruct.
        """
        embeddings, token_embeddings = LLMEmbedder().create_embedding(
            texts=process_text(
                self.merge_title_and_description(
                    document.data.get("title"), document.data.get("description")
                )
            )
        )
        point = models.PointStruct(
            id=document.pk,
            payload={
                "author_ids": document.author_ids,
                "doi": document.doi,
                TOKEN_KEY: token_embeddings[0],
            },
            vector=embeddings[0],
        )
        return point

    def load_document_point(
        self,
        point: models.PointStruct,
        collection_name: str,
    ) -> bool:
        """
        Load given data to Qdrant.

        :param payloads: List of dict.
        :param collection_name: String.
        :return: True if data are correctly wrote, False otherwise.
        """
        return qdrant_cli.upsert(
            collection_name=collection_name,
            points=[point],
        )
