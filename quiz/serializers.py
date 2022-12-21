from core.models import *
from rest_framework import serializers

from .models import Question, QuestionVersion, AnswerVersion, Quiz, UserAnswer, Choice

class QuestionOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'filepath', 'slug', 'order', 'category']


class QuestionVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionVersion
        fields = ['id', 'question', 'slug', 'title', 'description', 'categories', 'approved']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerVersion
        fields = ['id', 'question_version', 'text', 'correct']


class QuestionSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    categories = serializers.ListField(child=serializers.IntegerField())
    answers = serializers.JSONField()
    user = serializers.CharField()

    class Meta:
        fields = ['user', 'categories', 'description', 'title', 'answers']


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'user', 'category', 'completed', 'created', 'updated']


class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = ['id', 'quiz', 'question', 'created']


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'user_answer', 'answer']
