from rest_framework import serializers
from .models import Category, Flashcard, Deck


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class DeckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deck
        fields = "__all__"


class FlashcardSerializer(serializers.ModelSerializer):
    deck_name = serializers.SerializerMethodField(read_only=True)

    def get_deck_name(self, obj):
        return obj.deck.name

    class Meta:
        model = Flashcard
        fields = ["id", "front_side", "back_side", "deck", "deck_name", "probability"]