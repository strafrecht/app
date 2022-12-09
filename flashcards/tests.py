from django.test import TestCase

from django.contrib.auth.models import AnonymousUser, User

from .models import Category, Deck, Flashcard

class CategoryTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='testuser', password='12345')
        Category.objects.create(name="Test Category 1", user=user)

    def test_category_to_string(self):
        category = Category.objects.get(name="Test Category 1")
        self.assertEqual(str(category), "Test Category 1")

class DeckTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='testuser', password='12345')
        Deck.objects.create(name="Test Deck 1", user=user)

    def test_deck_to_string(self):
        deck = Deck.objects.get(name="Test Deck 1")
        self.assertEqual(str(deck), "Test Deck 1")

class FlashcardTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='testuser', password='12345')
        self.deck = Deck.objects.create(name="Test Deck 1", user=user)
        Flashcard.objects.create(deck=self.deck, front_side="Front", back_side="Back", user=user)

    def test_flashcard_to_string(self):
        flashcard = Flashcard.objects.get(deck=self.deck)
        self.assertEqual(str(flashcard), "Front - Back - Test Deck 1")
