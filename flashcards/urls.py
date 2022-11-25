from django.contrib import admin
from django.db import router
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from flashcards import views

app_name = 'flashcards'

router = DefaultRouter(trailing_slash=False)
router.register(r'cards', views.FlashcardViewSet, basename='card')
router.register(r'decks', views.DeckViewSet, basename='deck')
router.register(r'categories', views.CategoryViewSet, basename='category') # cards categories (not wiki categories)

urlpatterns = [
    path('api/', include(router.urls)),
]
