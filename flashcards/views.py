from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from wiki.models import Article

from core.models import Submission

from .models import Category, Flashcard, Deck
from .serializers import CategorySerializer, FlashcardSerializer, DeckSerializer

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
        if request.user.is_staff:
            queryset = Deck.objects.filter(submission__isnull=False, wiki_category_id=self.request.GET['article_id'])
        else:
            queryset = Deck.objects.filter(approved=True, wiki_category_id=self.request.GET['article_id'])
        serializer = DeckSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['put'])
    def submit(self, request, pk):
        obj = self.get_object()
        if obj.submission:
            return Response({'submission': obj.submission.id})
        obj.save()
        user = request.user
        obj.submission = Submission.objects.create(
            content_object=obj,
            submitted_by=user,
            message="Deck eingereicht",
            url=obj.wiki_category.get_absolute_url(),
        )
        obj.save()
        return Response({'submission': obj.submission.id})

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)
