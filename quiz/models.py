from django.db import models
from modelcluster.fields import ParentalKey
from django.contrib.auth.models import User
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wiki.models import URLPath

from core.edit_handlers import ReadOnlyPanel

import json

# Create your models here.
class Question(ClusterableModel):
    category = models.ForeignKey('wiki.Article', on_delete=models.SET_NULL, null=True, blank=True, related_name='questions')
    order = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)
    current = models.ForeignKey("QuestionVersion", on_delete=models.SET_NULL, blank=True, null=True, related_name='current_version')

    panels = [
        FieldPanel('order'),
        FieldPanel('category'),
        FieldPanel('approved'),
        ReadOnlyPanel('current', heading="Current question version"),
        FieldPanel('user'),
        InlinePanel('questions',heading='Question versions'),
    ]

class QuestionVersion(ClusterableModel):
    question = ParentalKey(Question, on_delete=models.CASCADE, related_name='questions')
    title = models.TextField(max_length=1000)
    description = models.TextField(max_length=2000)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id) + " | " + self.title + " | " + str(self.user) + " | " + str(self.created)

    def answers_json(self):
        return json.dumps([{ "text": o.text, "correct": o.correct } for o in self.answers.all()])

    def approve(self):
        self.question.approved = True
        self.question.current = self
        self.question.save()

    def is_current(self):
        if self.question.current:
            return self.question.approved and (self.question.current.id == self.id)

        return False

    panels = [
        ReadOnlyPanel('id', heading="Id"),
        ReadOnlyPanel('is_current', heading="Current version"),
        ReadOnlyPanel('user', heading="User"),
        ReadOnlyPanel('created', heading="Created"),
        ReadOnlyPanel('question', heading="Question"),
        FieldPanel('title'),
        FieldPanel('description'),
        InlinePanel('answers',heading='Answers'),
    ]

class AnswerVersion(ClusterableModel):
    question_version = ParentalKey(QuestionVersion, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField()
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Quiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey('wiki.Article', on_delete=models.SET_NULL, null=True, blank=True)
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def calculate_score(self):
        if self.useranswer_set:
            user_answers = self.useranswer_set.all()
            x = {}
            y = {}

            total = 0

            for user_answer in user_answers:
                answers = set()
                uanswers = set()

                for q_ver in user_answer.question.questions.all():
                    for answer in q_ver.answers.all():
                        if answer.correct:
                            answers.add(answer.id)

                for choice in user_answer.choice_set.all():
                    uanswers.add(choice.answer.id)

                # real answers
                x[user_answer.question.id] = answers
                # user answers
                y[user_answer.question.id] = uanswers

                if y[user_answer.question.id] == x[user_answer.question.id]:
                    total += 1

            return total

    def total_questions(self):
        return self.get_questions_for_category().count()

    def get_questions_for_category(self):
        path = URLPath.objects.get(article=self.category.id)
        ids = [path.article.id for path in path.get_descendants()]
        # Get questions
        questions = Question.objects.filter(category_id=self.category.id) | Question.objects.filter(category_id__in=ids)
        return questions.order_by('id')

class UserAnswer(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, null=True, on_delete=models.SET_NULL)
    answer = models.ForeignKey(AnswerVersion, null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)

class Choice(models.Model):
    user_answer = models.ForeignKey(UserAnswer, null=True, on_delete=models.SET_NULL)
    answer = models.ForeignKey(AnswerVersion, null=True, on_delete=models.SET_NULL)
