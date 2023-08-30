"""The universities app views."""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from universities.filters import AuthorFilter
from universities.models import Author
from universities.serializers import AuthorSerializer


class SearchAuthorViewSet(
    mixins.ListModelMixin,
    GenericViewSet,
):
    """Author viewset."""

    filter_backends = (DjangoFilterBackend,)
    filterset_class = AuthorFilter
    queryset = Author.objects.select_related("university").order_by("pk")
    serializer_class = AuthorSerializer

    def get_queryset(self):
        """Return the author viewset queryset."""
        queryset = super().get_queryset()
        if self.action == "list" and (
            not self.request.query_params or "" in self.request.query_params.values()
        ):
            return queryset.none()
        return queryset
