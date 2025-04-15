"""Test the universities app models."""

from django.test import SimpleTestCase, TestCase

from universities.models import Author, Document, University


class UniversityTest(SimpleTestCase):
    """Test the University model."""

    def test_str(self):
        """Test returning the string representation of an instance."""
        self.princeton = University(name="Princeton University")
        self.assertEqual(self.princeton.__str__(), "Princeton University")


class AuthorTest(SimpleTestCase):
    """Test the Author model."""

    def test_str(self):
        """Test returning the string representation of an instance."""
        self.princeton = University(name="Princeton University")
        self.leonard = Author(
            orcid="0000-0000-0000-0001",
            full_name="Leonard Hofstadter",
            university=self.princeton,
        )
        self.assertEqual(self.leonard.__str__(), "Leonard Hofstadter")


class DocumentTest(TestCase):
    """Test the Document model."""

    @classmethod
    def setUpTestData(cls):
        """Prepare initial data for testing."""
        cls.princeton = University.objects.create(name="Princeton University")
        cls.ettu = University.objects.create(name="East Texas Tech University")
        cls.leonard = Author.objects.create(
            orcid="0000-0000-0000-0001",
            full_name="Leonard Hofstadter",
            university=cls.princeton,
        )
        cls.sheldon = Author.objects.create(
            orcid="0000-0000-0000-0002",
            full_name="Sheldon Cooper",
            university=cls.ettu,
        )
        cls.svt = Document.objects.create(
            doi="99.9999/999-9-999-99999-9_99",
            title="The superfluid vacuum theory",
            description=(
                "Superfluid vacuum theory (SVT), sometimes known as the BEC vacuum "
                "theory, is an approach in theoretical physics and quantum mechanics "
                "where the fundamental physical vacuum (non-removable background) is "
                "considered as a superfluid or as a Bose–Einstein condensate (BEC)."
            ),
        )
        cls.svt.authors.add(cls.leonard, cls.sheldon)

    def test_str(self):
        """Test returning the string representation of an instance."""
        self.assertEqual(self.svt.__str__(), "The superfluid vacuum theory")

    def test_authors_names(self):
        """Test authors_names property."""
        self.assertEqual(self.svt.authors_names, "Leonard Hofstadter, Sheldon Cooper")
