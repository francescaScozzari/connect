"""Explainable Artificial Intelligence explainability."""

import logging
from typing import List, Optional, Tuple

import numpy as np
from django.conf import settings
from django.utils.decorators import classonlymethod
from sklearn.preprocessing import normalize

from xai import (
    EMBEDDING_FILLER_CHAR,
    EMBEDDING_KEY,
    EMBEDDING_METACHARS,
    EXPLAIN_GIVEN_WORD,
    EXPLAIN_RESTORED_WORD,
    EXPLAIN_SCORE,
    STOP_WORDS,
    TOKEN_KEY,
    logger,
)

if settings.DEBUG:  # pragma: no cover
    logging.basicConfig(level=logging.DEBUG)


class ExplainabilityComputing:
    """The Explainability computing class."""

    @classonlymethod
    def split_tokens_and_embeddings(
        cls, tokens_embeddings: List[dict]
    ) -> Tuple[List[str], np.array]:
        """
        Compute a normalized embeddings for each token.

        :param token_embedding: Dictionary with token embeddings created by Embedder
        :return: List of tokens and list of normalized embeddings for each token.
        """
        tokens, embeddings = [], []
        for word in tokens_embeddings:
            if word[TOKEN_KEY] not in EMBEDDING_METACHARS:
                tokens.append(word[TOKEN_KEY].replace(EMBEDDING_FILLER_CHAR, ""))
                embeddings.append(word[EMBEDDING_KEY])
        embeddings = normalize(embeddings, norm="l2")
        return tokens, embeddings

    @classonlymethod
    def largest_indices(
        cls, vector: np.array, nb_values: Optional[int] = 10
    ) -> Tuple[List[int], List[float]]:
        """
        Return list of coordinates of first-n greatest values and their values.

        Given a multidimensional numpy array, this function returns a tuple with
        list of coordinates of first-n greatest values, and their values
        :param vector: Numpy array of numeric values
        :param nb_values: Number of first-n tuple to return
        :return: Tuple with coordinates of greatest values, and values.
        """
        arr_shape = vector.shape
        nb_elements = np.prod(arr_shape)
        if nb_values is None:
            nb_values = nb_elements
        else:
            nb_values = nb_elements if nb_values > nb_elements else nb_values
        flat = vector.flatten()
        indices = np.argpartition(flat, -nb_values)[-nb_values:]
        indices = indices[np.argsort(-flat[indices])]
        coords_list = np.unravel_index(indices, arr_shape)
        coords = []
        values = list(vector[coords_list])
        for coord in zip(*coords_list, strict=False):
            coords.append(coord)
        return coords, values

    @classonlymethod
    def get_words_matching_with_score(
        cls, sentence_tokens, sentence_embeddings, document_tokens, document_embeddings
    ):
        """Return words matching with score result."""
        attention = sentence_embeddings @ document_embeddings.T  # type: ignore
        indexes, values = cls.largest_indices(vector=attention, nb_values=None)
        words_result = []
        for coords, score in zip(indexes, values, strict=False):
            given_word = sentence_tokens[coords[0]]  # type: ignore
            restored_word = document_tokens[coords[1]]  # type: ignore
            if given_word not in STOP_WORDS and restored_word not in STOP_WORDS:
                data = {
                    EXPLAIN_GIVEN_WORD: given_word,
                    EXPLAIN_RESTORED_WORD: restored_word,
                    EXPLAIN_SCORE: round(score, 5),
                }
                words_result.append(data)
        return words_result

    @classonlymethod
    def get_given_words_result(cls, sentence_tokens, words_result):
        """Return given words result."""
        result: list = []
        for given_word in sentence_tokens:
            if given_word not in STOP_WORDS:
                given_word_result = [
                    item
                    for item in words_result
                    if (
                        item[EXPLAIN_GIVEN_WORD] == given_word
                        and item[EXPLAIN_RESTORED_WORD] not in STOP_WORDS
                    )
                ]
                given_word_explain = sorted(
                    given_word_result,
                    key=lambda x: x[EXPLAIN_SCORE],  # type: ignore
                    reverse=True,
                )[0]
                result.append(given_word_explain)
        return result

    @classonlymethod
    def explain_result(
        cls,
        sentence_tokens_embeddings: List[dict],
        document_tokens_embeddings: List[dict],
    ) -> List[dict]:
        """
        Compute for each given token, how much a pair of word influenced final result.

        :param document_tokens_embeddings: Token embedding saved on QDrant.
        :param sentence_tokens_embeddings: Token embedding of given sentence.
        :return: List of dictionaries for each elements in document_tokens_embeddings.
        """
        sentence_tokens, sentence_embeddings = cls.split_tokens_and_embeddings(
            sentence_tokens_embeddings
        )
        logger.debug("I'm Computing attention for document text token")
        (
            document_tokens,
            document_embeddings,
        ) = cls.split_tokens_and_embeddings(document_tokens_embeddings)
        words_result = cls.get_words_matching_with_score(
            sentence_tokens, sentence_embeddings, document_tokens, document_embeddings
        )
        return cls.get_given_words_result(sentence_tokens, words_result)
