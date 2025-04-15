"""Initialize tests for scopus app."""

from pathlib import Path

AUTHOR_SEARCH_BASE_URL = "https://api.elsevier.com/content/search/author?count=200&view=STANDARD&query={}%28{}%29&start=0"

SCOPUS_SEARCH_BASE_URL = "https://api.elsevier.com/content/search/scopus?count=25&view=COMPLETE&query={}%28{}%29&cursor=%2A"

AUTHOR_1_SEARCH_JSON = Path("scopus/tests/data/author_1_search.json")

AUTHOR_11111111111_SEARCH_JSON = Path(
    "scopus/tests/data/author_11111111111_search.json"
)

AUTHOR_11111111111_DOCUMENTS_JSON = Path(
    "scopus/tests/data/author_11111111111_documents.json"
)
