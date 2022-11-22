from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Category, Flashcard, Deck
from .serializers import CategorySerializer, FlashcardSerializer, DeckSerializer
from django.shortcuts import render

class FlashcardViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing flashcards.
    """
    queryset = Flashcard.objects.all()
    serializer_class = FlashcardSerializer
    permission_classes = [AllowAny]


class DeckViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing decks.
    """
    queryset = Deck.objects.all()
    serializer_class = DeckSerializer
    permission_classes = [AllowAny]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
