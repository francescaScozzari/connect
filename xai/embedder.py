"""Explainable Artificial Intelligence embedder."""

from typing import Tuple

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

    def __init__(self, text: str = "") -> None:
        """Initialize the instance."""
        self.filler_char = EMBEDDING_FILLER_CHAR
        self.metachars = EMBEDDING_METACHARS
        self.model = AutoModel.from_pretrained(MODEL_NAME)
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        self.text = text
        self.encoded_input, self.model_output = self.encoded_input_model_output()
        set_seed(42)

    def initial_setup(self):
        """Run the initial setup of the instance."""
        super().__init__()  # pragma: no cover

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

    def encoded_input_model_output(self) -> Tuple:
        """Return encoded input and model output using all-MiniLM-L6-v2 model."""
        if self.text:
            # Tokenize input
            encoded_input = self.tokenizer(
                self.text,
                padding=True,
                truncation=True,
                max_length=512,
                return_tensors="pt",
            )
            # Create word embeddings
            model_output = self.model(**encoded_input)
            return encoded_input, model_output
        return (None, None)

    def get_tokens_embeddings(self) -> list[dict]:
        """
        Return tokens embeddings for given text using all-MiniLM-L6-v2 model.

        :return: tokens embeddings for given text.
        """
        # For each text, store a list of token embeddings with fixed length
        # (length depends on LLM). In this case we have 384
        tokens = self.tokenizer.convert_ids_to_tokens(
            self.encoded_input["input_ids"][0]
        )
        embeddings = self.model_output[0][0]
        return [
            {
                TOKEN_KEY: token,
                EMBEDDING_KEY: embedding.detach().numpy().tolist(),
            }
            for token, embedding in zip(tokens, embeddings, strict=False)
        ]

    def get_sentence_embeddings(self) -> list[float]:
        """
        Return an embedding for given text using all-MiniLM-L6-v2 model.

        :return: embedding for given text.
        """
        # Pool to get sentence embeddings;
        # i.e. generate one 384 vector for the entire sentence
        sentence_embeddings = (
            self.mean_pooling(self.model_output, self.encoded_input["attention_mask"])
            .detach()
            .numpy()
        )
        # Concatenate all the embeddings into one numpy array of shape (n_texts, 384)
        sentence_embeddings = np.concatenate(sentence_embeddings).tolist()
        return sentence_embeddings
