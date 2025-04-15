"""Test the Scopus utils."""

from django.test import SimpleTestCase

from scopus.utils import is_orcid_id


class UtilsTest(SimpleTestCase):
    """Test the utils."""

    def test_is_orcid_id(self):
        """Test telling whether the provided id is an ORCID id."""
        self.assertFalse(is_orcid_id(1))
        self.assertTrue(is_orcid_id("A"))
