"""The universities app filters."""

import django_filters

from universities.models import Author


class AuthorFilter(django_filters.FilterSet):
    """A filter for author."""

    MAX_RESULT_NUM = 25

    q = django_filters.CharFilter(label="Search", method="filter_by_search")
    team_size = django_filters.NumberFilter(
        label="Team size", method="filter_by_team_size", max_value=MAX_RESULT_NUM
    )

    class Meta:
        """Filter options."""

        model = Author
        fields: tuple = ()

    def filter_by_search(self, queryset, name, value):
        """Filter queryset by search value."""
        return queryset.order_by("?")[: self.MAX_RESULT_NUM]

    def filter_by_team_size(self, queryset, name, value):
        """Filter by team size."""
        return queryset[:value]
