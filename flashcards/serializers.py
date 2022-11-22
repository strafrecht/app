from rest_framework import serializers
from .models import Category, Flashcard, Deck


class CategorySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Category
        fields = "__all__"

    def save(self, **kwargs):
        kwargs["user"] = self.fields["user"].get_default()
        return super().save(**kwargs)

class DeckSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Deck
        fields = "__all__"

    def save(self, **kwargs):
        kwargs["user"] = self.fields["user"].get_default()
        return super().save(**kwargs)

class FlashcardSerializer(serializers.ModelSerializer):
    deck_name = serializers.SerializerMethodField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    def get_deck_name(self, obj):
        return obj.deck.name

    class Meta:
        model = Flashcard
        fields = "__all__"

    def save(self, **kwargs):
        kwargs["user"] = self.fields["user"].get_default()
        return super().save(**kwargs)
