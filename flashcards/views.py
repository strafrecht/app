from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Category, Flashcard, Deck
from .serializers import CategorySerializer, FlashcardSerializer, DeckSerializer
from django.shortcuts import render

class FlashcardViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing flashcards.
    """
    serializer_class = FlashcardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Flashcard.objects.filter(user=self.request.user)


class DeckViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing decks.
    """
    serializer_class = DeckSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Deck.objects.filter(user=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)
