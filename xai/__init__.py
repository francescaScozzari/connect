"""Initialize Explainable Artificial Intelligence app."""

import logging

logger = logging.getLogger(__name__)

EMBEDDING_FILLER_CHAR = "#"
EMBEDDING_KEY = "embedding"
EMBEDDING_METACHARS = ["[CLS]", "[SEP]"]
EMBEDDING_STRATEGY = "all-MiniLM-L6-v2"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
TOKEN_KEY = "token"  # nosec
