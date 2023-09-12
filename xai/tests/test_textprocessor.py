"""Test the xai app text processor."""

from django.test import TestCase

from xai.textprocessor import process_text


class TestProcessText(TestCase):
    """Test process text."""

    def test_process_text(self):
        """Test process_text method."""
        text = "I'm a test text,\n which contains 9 words"
        res = process_text(text=text)
        expected = "i'm a test text, which contains words"
        self.assertEqual(res, expected)
