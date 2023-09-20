"""The universities app views."""

from rest_framework.response import Response
from rest_framework.views import APIView

from scopus.models import ScopusAuthor
from xai.facade import SearchMostSimilarFacade


class AuthorsSearchView(APIView):
    """Define the search authors api view."""

    def get(self, request):
        """Return the GET method response."""
        team_size = request.query_params.get("team_size") or None
        q = request.query_params.get("q") or None
        data = []
        if q and team_size:
            data = {"authors": [], "given_sentence": {"text": q, "highlights": []}}
            xai_search_facade = SearchMostSimilarFacade(sentence=q)
            sentence_highlights = xai_search_facade.get_sentence_highlights()
            data["given_sentence"]["highlights"] = sentence_highlights
            authors = xai_search_facade.get_authors_from_similar_search(
                limit_authors=team_size and int(team_size)
            )
            for author in authors:
                scopus_author = ScopusAuthor.objects.get(author_id=author["author_id"])
                data["authors"].append(
                    {
                        **author,
                        "full_name": scopus_author.full_name,
                        "university": scopus_author.university,
                        "orcid": scopus_author.orcid,
                    }
                )
        return Response(data)
