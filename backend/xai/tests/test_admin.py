"""Test the xai admin."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from scopus.models import ScopusDocument
from xai.models import TokensEmbeddings


# @override_settings(ROOT_URLCONF="admin_views.urls", USE_I18N=True, LANGUAGE_CODE="en")
class TokensEmbeddingsAdminTestCase(TestCase):
    """Test TokensEmbeddings admin."""

    change_url = "admin:xai_tokensembeddings_change"
    changelist_url = "admin:xai_tokensembeddings_changelist"

    @classmethod
    def setUpTestData(cls):
        """Set up test data."""
        cls.superuser = User.objects.create_superuser(username="user", password="pass")
        scopusdocument = ScopusDocument.objects.create(doi="1", data={})
        cls.tokensembeddings = TokensEmbeddings.objects.create(
            document=scopusdocument, data=[]
        )

    def test_get_queryset(self):
        """Test customize get_queryset method."""
        self.client.force_login(self.superuser)
        with self.assertNumQueries(4):
            self.client.get(reverse(self.changelist_url), {})
        with self.assertNumQueries(6):
            self.client.get(
                reverse(self.change_url, args=(self.tokensembeddings.pk,)), {}
            )
