"""The universities app serializers."""

from rest_framework.fields import ReadOnlyField
from rest_framework.serializers import ModelSerializer

from universities.models import Author


class AuthorSerializer(ModelSerializer):
    """A serializer for author."""

    university = ReadOnlyField(source="university.name")

    class Meta:
        """Author serializer meta class."""

        fields: tuple = (
            "full_name",
            "orcid",
            "university",
        )
        model = Author
