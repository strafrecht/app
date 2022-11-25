from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category, Flashcard, Deck
from .serializers import CategorySerializer, FlashcardSerializer, DeckSerializer
from django.shortcuts import render

class FlashcardViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing flashcards.
    """
    serializer_class = FlashcardSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return Flashcard.objects.filter(user=self.request.user)

    def list(self, request):
        queryset = Flashcard.objects.filter(deck_id=self.request.GET['deck_id'])
        serializer = FlashcardSerializer(queryset, many=True)
        return Response(serializer.data)

class DeckViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing decks.
    """
    serializer_class = DeckSerializer

    def get_permissions(self):
        if self.action == 'for_wiki':
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return Deck.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def for_wiki(self, request):
        queryset = Deck.objects.filter(wiki_category_id=self.request.GET['article_id'])
        serializer = DeckSerializer(queryset, many=True)
        return Response(serializer.data)

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)
