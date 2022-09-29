from django.test import TestCase
from .models import Category
from .models import Deck
from .models import Flashcard

class CategoryTestCase(TestCase):
    def setUp(self):
        Category.objects.create(name="Test Category 1")

    def test_category_to_string(self):
        category = Category.objects.get(name="Test Category 1")
        self.assertEqual(str(category), "Test Category 1")

class DeckTestCase(TestCase):
    def setUp(self):
        Deck.objects.create(name="Test Deck 1")

    def test_deck_to_string(self):
        deck = Deck.objects.get(name="Test Deck 1")
        self.assertEqual(str(deck), "Test Deck 1")

class FlashcardTestCase(TestCase):
    def setUp(self):
        self.deck = Deck.objects.create(name="Test Deck 1")
        Flashcard.objects.create(deck=self.deck, front_side="Front", back_side="Back")

    def test_flashcard_to_string(self):
        flashcard = Flashcard.objects.get(deck=self.deck)
        self.assertEqual(str(flashcard), "Front - Back - Test Deck 1")
