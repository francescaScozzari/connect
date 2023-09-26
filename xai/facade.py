"""Explainable Artificial Intelligence facade."""

import itertools
import logging
import math
from datetime import datetime

from django.conf import settings
from django.utils.decorators import classonlymethod
from qdrant_client.http import models

from connect.qdrant import cli as qdrant_cli
from scopus.models import ScopusDocument
from xai import STOP_WORDS, logger
from xai.embedder import LLMEmbedder
from xai.explainability import ExplainabilityComputing
from xai.models import TokensEmbeddings
from xai.textprocessor import process_text

if settings.DEBUG:  # pragma: no cover
    logging.basicConfig(level=logging.DEBUG)


class WriteEmbeddingFacade:
    """The write embedding xai class."""

    def __init__(
        self,
        document: ScopusDocument,
    ) -> None:
        """Initialize the write embedding facade class."""
        self.document = document
        self.embedder = LLMEmbedder(
            text=process_text(self.merge_title_and_description())
        )
        self.document_embeddings = (
            self.embedder.get_sentence_embeddings() if document else []
        )
        self.document_tokens_embeddings = (
            self.embedder.get_tokens_embeddings() if document else []
        )

    def merge_title_and_description(self, merging_sym: str = ".") -> str:
        """
        Merge two strings into a single one with this pattern.

        title<symbol> description
        :param merging_sym: Symbol used to merge. Default value is "."
        :param description: String on the right of the result
        :param title: String on the left of the result
        :return: merged string.
        """
        return (
            f"{self.document.title}{merging_sym} {self.document.description}".rstrip()
        )

    def create_document_tokens_embeddings(self):
        """Create a TokensEmbeddings for given document."""
        return TokensEmbeddings.objects.get_or_create(
            document_id=self.document.doi, data=self.document_tokens_embeddings
        )

    def generate_document_point(self, connect_author_ids: list[int]):
        """
        Generate document point.

        :param documents: scopus.ScopusDocument
        :return: qdrant_client.http.models.PointStruct
        """
        point = models.PointStruct(
            id=self.document.pk,
            payload={
                "author_ids": [
                    author_id
                    for author_id in self.document.author_ids
                    if int(author_id) in connect_author_ids
                ],
                "doi": self.document.doi,
                "title": self.document.title,
                "description": self.document.description,
            },
            vector=self.document_embeddings,
        )
        return point

    @classonlymethod
    def load_document_point(
        cls,
        point: models.PointStruct,
    ):
        """
        Load given data to Qdrant.

        :param payloads: List of dict.
        :param collection_name: String.
        :return: True if data are correctly wrote, False otherwise.
        """
        return qdrant_cli.upsert(
            collection_name=settings.QDRANT_DOCUMENTS_COLLECTION,
            points=[point],
        )


class SearchMostSimilarFacade:
    """The Explainable Artificial Intelligence search most similar facade class."""

    def __init__(self, sentence: str) -> None:
        """Initialize the search most similar instance by given sentence."""
        embedder = LLMEmbedder(text=process_text(text=sentence))
        self.sentence = sentence
        self.sentence_embeddings = (
            embedder.get_sentence_embeddings() if sentence else []
        )
        self.sentence_tokens_embeddings = (
            embedder.get_tokens_embeddings() if sentence else []
        )

    @classmethod
    def get_author_normalized_score(cls, author_scores):
        """Return normalized author score."""
        return round(sum(author_scores) / math.sqrt(sum(author_scores)), 5)

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

    def get_document_explainability(self, document_doi):
        """Return document explainability."""
        try:
            document_tokens_embeddings = TokensEmbeddings.objects.get(
                document_id=document_doi
            ).data
        except TokensEmbeddings.DoesNotExist:
            return None
        else:
            return ExplainabilityComputing.explain_result(
                self.sentence_tokens_embeddings,
                document_tokens_embeddings,
            )

    def get_document_highlights(self, document_doi):
        """Return flat list of highlights word for given document doi."""
        explain_results = self.get_document_explainability(document_doi)
        return (
            sorted(
                {explain_result["restored_word"] for explain_result in explain_results}
            )
            if explain_results
            else []
        )

    def get_authors_from_similar_search(
        self, limit_authors: int = 6, limit_documents: int = 50
    ):
        """Return a list of authors from similar search."""
        total_started_at = datetime.now()
        result = self.search_most_similar(limit=limit_documents)
        authors = []
        logger.debug(f"start search by each {len(result['author_ids'])} authors")
        for author_id in result["author_ids"]:
            logger.debug(f"search most similar for author {author_id}")
            started_at = datetime.now()
            author_documents = self.search_most_similar_filtered_by_author_id(
                str(author_id)
            )
            search_execution_time = datetime.now() - started_at
            logger.debug(f"search execution time: {search_execution_time}")
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
                    "score": self.get_author_normalized_score(author_scores),
                }
            )
        total_time = datetime.now() - total_started_at
        logger.debug(f"TOTAL execution time: {total_time}")
        return sorted(authors, key=lambda x: x["score"], reverse=True)[:limit_authors]

    def get_authors_with_document_highlights(
        self, limit_authors: int = 6, limit_documents: int = 50
    ):
        """Return a list of authors with document highlights."""
        authors = self.get_authors_from_similar_search(limit_authors, limit_documents)
        for author in authors:
            for document in author["documents"]:
                document["highlights"] = self.get_document_highlights(document["doi"])
        return authors

    def get_sentence_highlights(self):
        """Return given sentence highlights."""
        tokens, _embeddings = ExplainabilityComputing.split_tokens_and_embeddings(
            self.sentence_tokens_embeddings
        )
        return [token for token in tokens if token not in STOP_WORDS]
