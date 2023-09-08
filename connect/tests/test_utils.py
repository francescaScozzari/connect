"""The main app utils tests."""

from django.test import TestCase

from connect.utils import transform_literal_id


class TestUtils(TestCase):
    """The utils tests."""

    def test_transform_literal_id(self):
        """Test transform_literal_id method."""
        transformed_id = transform_literal_id("99.9999/999-9-999-99999-9_99")
        expected_result = (
            3849439176125250520832009392267879549757464859643919592969476415123787
        )
        self.assertEqual(transformed_id, expected_result)
