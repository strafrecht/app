from django.db import models
from modelcluster.fields import ParentalKey
from django.contrib.auth.models import User
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wiki.models import URLPath
import json

# Create your models here.
class Question(ClusterableModel):
    category = models.ForeignKey('wiki.Article', on_delete=models.SET_NULL, null=True, blank=True, related_name='questions')
    order = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    panels = [
        FieldPanel('filepath'),
        FieldPanel('slug'),
        FieldPanel('order'),
        FieldPanel('category'),
        FieldPanel('user'),
    ]

    # FIXME: return the first approved QuestionVersion
    def current(self):
        return self.questions.filter(approved=True).first()

class QuestionVersion(ClusterableModel):
    question = ParentalKey(Question, on_delete=models.CASCADE, related_name='questions')
    title = models.TextField(max_length=1000)
    description = models.TextField(max_length=2000)
    approved = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def answers_json(self):
        return json.dumps([{ "text": o.text, "correct": o.correct } for o in self.answers.all()])

    def approve(self):
        for qv in self.question.questions.all():
            qv.approved = False
            qv.save()
        self.approved = True
        self.save()

    panels = [
            FieldPanel('question'),
            FieldPanel('title'),
            FieldPanel('description'),
            FieldPanel('approved'),
            InlinePanel('answers'),
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
