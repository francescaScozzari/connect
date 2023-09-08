"""Initialize tests for scopus app."""

from pathlib import Path

AUTHOR_BASE_URL = "https://api.elsevier.com/content/author/author_id"

AUTHOR_11111111111_JSON = Path("scopus/tests/data/author_11111111111.json")

SEARCH_AUTHOR_11111111111_URL = "https://api.elsevier.com/content/search/scopus?count=25&view=COMPLETE&query=AU-ID%2811111111111%29&cursor=%2A"

AUTHOR_11111111111_DOCUMENTS_JSON = Path("scopus/tests/data/documents_11111111111.json")
