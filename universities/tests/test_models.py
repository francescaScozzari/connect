"""Test the universities app models."""

from django.test import SimpleTestCase, TestCase

from universities.models import Author, Document, University


class UniversityTest(SimpleTestCase):
    """Test the University model."""

    def test_str(self):
        """Test str method."""
        self.unich = University(name="University of G. d'Annunzio Chieti and Pescara")
        self.assertEqual(
            self.unich.__str__(), "University of G. d'Annunzio Chieti and Pescara"
        )


class AuthorTest(SimpleTestCase):
    """Test the Author model."""

    def test_str(self):
        """Test str method."""
        self.unich = University(name="University of G. d'Annunzio Chieti and Pescara")
        self.gianluca_mato = Author(
            orcid="0000-0002-6214-5198",
            full_name="Gianluca Amato",
            university=self.unich,
        )
        self.assertEqual(self.gianluca_mato.__str__(), "Gianluca Amato")


class DocumentTest(TestCase):
    """Test the Document model."""

    @classmethod
    def setUpTestData(cls):
        """Prepare initial data for testing."""
        cls.unich = University.objects.create(
            name="University of G. d'Annunzio Chieti and Pescara"
        )
        cls.gianluca_mato = Author.objects.create(
            orcid="0000-0002-6214-5198",
            full_name="Gianluca Amato",
            university=cls.unich,
        )
        cls.francesca_scozzari = Author.objects.create(
            orcid="0000-0002-2105-4855",
            full_name="Francesca Scozzari",
            university=cls.unich,
        )
        cls.the_scalafix_equation_solver = Document.objects.create(
            doi="10.1007/978-3-031-27481-7_10",
            title="The ScalaFix Equation Solver",
            description=(
                "We present ScalaFix, a modular library for solving equation systems by"
                "by iterative methods. ScalaFix implements several solvers, involving "
                "iteration strategies from plain Kleene’s iteration to more complex "
                "ones based on a hierarchical ordering of the unknowns. It works with "
                "finite and infinite equation systems and supports widening, narrowing "
                "and warrowing operators. It also allows intertwining ascending and "
                "descending chains and other advanced techniques such as localized "
                "widening."
            ),
        )
        cls.the_scalafix_equation_solver.authors.add(
            cls.gianluca_mato, cls.francesca_scozzari
        )

    def test_str(self):
        """Test str method."""
        self.assertEqual(
            self.the_scalafix_equation_solver.__str__(), "The ScalaFix Equation Solver"
        )

    def test_authors_names(self):
        """Test authors_names property."""
        self.assertEqual(
            self.the_scalafix_equation_solver.authors_names,
            "Francesca Scozzari, Gianluca Amato",
        )
