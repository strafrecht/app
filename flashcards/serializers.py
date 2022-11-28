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
    user_name = serializers.SerializerMethodField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    def get_user_name(self, obj):
        return str(obj.user)

    class Meta:
        model = Deck
        fields = "__all__"

    def validate(self, attrs):
        category = attrs["category"]
        if category and category.user != self.get_user():
            del attrs["category"]
        return attrs

    def get_user(self):
        return self.fields["user"].get_default()

    def save(self, **kwargs):
        kwargs["user"] = self.get_user()
        return super().save(**kwargs)

class FlashcardSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Flashcard
        fields = "__all__"

    def validate(self, attrs):
        deck = attrs["deck"]
        if deck.user != self.get_user():
            del attrs["deck"]
        return attrs

    def get_user(self):
        return self.fields["user"].get_default()

    def save(self, **kwargs):
        kwargs["user"] = self.get_user()
        return super().save(**kwargs)
