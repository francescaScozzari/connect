"""Explainable Artificial Intelligence facade."""

import datetime
import itertools
import logging

from django.conf import settings
from qdrant_client.http import models

from connect.qdrant import cli as qdrant_cli
from scopus.models import ScopusDocument
from xai import logger
from xai.embedder import LLMEmbedder
from xai.textprocessor import process_text

if settings.DEBUG:  # pragma: no cover
    logging.basicConfig(level=logging.DEBUG)


class WriteEmbeddingFacade:
    """The write embedding xai class."""

    def merge_title_and_description(
        self, title: str, description: str, merging_sym: str = "."
    ) -> str:
        """
        Merge two strings into a single one with this pattern.

        title<symbol> description
        :param merging_sym: Symbol used to merge. Default value is "."
        :param description: String on the right of the result
        :param title: String on the left of the result
        :return: merged string.
        """
        return f"{title}{merging_sym} {description}"

    def generate_document_point(
        self, document: ScopusDocument, connect_author_ids: list[int]
    ):
        """
        Generate document point.

        :param documents: scopus.ScopusDocument
        :return: qdrant_client.http.models.PointStruct
        """
        embedding = LLMEmbedder(
            text=process_text(
                self.merge_title_and_description(
                    document.data.get("title"), document.data.get("description")
                )
            )
        ).get_sentence_embeddings()
        point = models.PointStruct(
            id=document.pk,
            payload={
                "author_ids": [
                    author_id
                    for author_id in document.author_ids
                    if int(author_id) in connect_author_ids
                ],
                "doi": document.doi,
                "title": document.data.get("title"),
                "description": document.data.get("description"),
            },
            vector=embedding,
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


class SearchMostSimilarFacade:
    """The Explainable Artificial Intelligence search most similar facade class."""

    def __init__(self, sentence: str) -> None:
        """Initialize the search most similar instance by given sentence."""
        self.sentence_embeddings = LLMEmbedder(
            text=process_text(text=sentence)
        ).get_sentence_embeddings()

    def search_most_similar(self, limit: int = 50) -> dict:
        """
        Search most similar documents by given sentence.

        Returns IDs of most similar documents,
        their authors, and a score of the result.

        :param sentence: Text for which we want to search documents
        :param limit: Number of most similar documents to fetch from qdrant. Default: 50
        :return: List of dictionaries with document information
        """
        results = qdrant_cli.search(
            collection_name=settings.QDRANT_DOCUMENTS_COLLECTION,
            limit=limit,
            query_vector=self.sentence_embeddings,
            with_vectors=False,
        )
        author_ids = list(
            set(itertools.chain(*[result.payload["author_ids"] for result in results]))
        )
        return {"results": results, "author_ids": author_ids}

    def search_most_similar_filtered_by_author_id(
        self, author_id: str, limit_documents: int = 3
    ) -> dict:
        """
        Search three most similar author documents by given sentence.

        :param sentence: the given sentence
        :param author_id: filter query by author_id
        :param limit_documents: limit query result, default: 3
        return: dict
        """
        results = qdrant_cli.search(
            collection_name=settings.QDRANT_DOCUMENTS_COLLECTION,
            limit=limit_documents,
            query_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="author_ids", match=models.MatchAny(any=[author_id])
                    )
                ]
            ),
            query_vector=self.sentence_embeddings,
        )
        return results

    def get_authors_from_similar_search(
        self, limit_authors: int = 6, limit_documents: int = 100
    ):
        """Get authors from similar search."""
        total_start = datetime.datetime.now()
        result = self.search_most_similar(limit=limit_documents)
        authors = []
        logger.debug(f"start search by each {len(result['author_ids'])} authors")
        for author_id in result["author_ids"]:
            logger.debug(f"search most similar for author {author_id}")
            start = datetime.datetime.now()
            author_documents = self.search_most_similar_filtered_by_author_id(
                str(author_id)
            )
            end = datetime.datetime.now()
            total_time = end - start
            logger.debug(f"search execution time: {total_time}")
            author_scores = [document.score for document in author_documents]
            author_documents_data = [
                {
                    "doi": document.payload["doi"],
                    "title": document.payload["title"],
                    "description": document.payload["description"],
                    "score": round(document.score, 5),
                }
                for document in author_documents
            ]
            authors.append(
                {
                    "author_id": author_id,
                    "documents": author_documents_data,
                    "score": round(sum(author_scores), 5),
                }
            )
        total_end = datetime.datetime.now()
        total_time = total_end - total_start
        logger.debug(f"TOTAL execution time: {total_time}")
        return sorted(authors, key=lambda x: x["score"], reverse=True)[:limit_authors]
