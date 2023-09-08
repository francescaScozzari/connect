"""Explainable Artificial Intelligence embedder."""

from typing import List, Tuple

import numpy as np
import torch
from transformers import AutoModel, AutoTokenizer, set_seed

from xai import (
    EMBEDDING_FILLER_CHAR,
    EMBEDDING_KEY,
    EMBEDDING_METACHARS,
    MODEL_NAME,
    TOKEN_KEY,
)


class LLMEmbedder:
    """The Large Language Model embedder xai class."""

    def __init__(self) -> None:
        """Initialize the instance."""
        self.filler_char = EMBEDDING_FILLER_CHAR
        self.metachars = EMBEDDING_METACHARS
        self.model = AutoModel.from_pretrained(MODEL_NAME)
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        set_seed(42)

    def mean_pooling(self, model_output, attention_mask) -> torch.Tensor:
        """
        Mean pooling to get sentence embeddings.

        See:
        https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
        :param model_output: Embedding created by the model
        :param attention_mask: Attention mask given by the tokenizer
        :return: Mean pooling of a text given tokens list.
        """
        token_embeddings = model_output[0]
        # Create an attention mask for each expanded token
        # with 384 dimension for each token
        input_mask_expanded = (
            attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        )
        # token_embeddings * input_mask_expanded
        # -> element wise multiplication (not mat mul)
        # torch.sum, sums elements (in this code is a col sum)
        # in order to have a single tensor for sentence
        sum_embeddings = torch.sum(
            token_embeddings * input_mask_expanded, 1
        )  # Sum columns
        # input_mask_expanded.sum(1) for each row of input_mask_expanded,
        # sum its elements and put them in a single row tensor
        # torch.clamp applies a lower and upeer bound
        sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        mean_pooling = sum_embeddings / sum_mask
        return mean_pooling

    def create_embedding(
        self, texts: List[str]
    ) -> Tuple[List[List[float]], List[List[dict]]]:
        """
        Create an embedding for given list of texts using all-MiniLM-L6-v2 model.

        :param texts: List of texts to embed.
        :return: Tuple with embedding for each text and token embedding
        for each token for each text.
        """
        sentence_embeddings = []
        token_embeddings = []
        len(texts)
        for text in texts:
            # Tokenize input
            encoded_input = self.tokenizer(
                text, padding=True, truncation=True, max_length=512, return_tensors="pt"
            )
            # Create word embeddings
            model_output = self.model(**encoded_input)
            # For each text, store a list of token embeddings with fixed length
            # (length depends on LLM). In this case we have 384
            tokens = self.tokenizer.convert_ids_to_tokens(encoded_input["input_ids"][0])
            embeddings = model_output[0][0]
            token_embeddings.append(
                [
                    {
                        TOKEN_KEY: token,
                        EMBEDDING_KEY: embedding.detach().numpy().tolist(),
                    }
                    for token, embedding in zip(tokens, embeddings, strict=False)
                ]
            )
            # Pool to get sentence embeddings;
            # i.e. generate one 384 vector for the entire sentence
            sentence_embeddings.append(
                self.mean_pooling(model_output, encoded_input["attention_mask"])
                .detach()
                .numpy()
            )
        # Concatenate all the embeddings into one numpy array of shape (n_texts, 384)
        sentence_embeddings = np.concatenate(sentence_embeddings).tolist()
        return sentence_embeddings, token_embeddings
