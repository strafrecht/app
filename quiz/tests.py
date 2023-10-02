from django.test import TestCase

from django.contrib.auth.models import AnonymousUser, User
from wiki.models import Article, ArticleRevision, URLPath

from pages.models.jurcoach import JurcoachPage
from wagtailpolls.models import Poll

from .models import Question, QuestionVersion, AnswerVersion, Quiz, UserAnswer

class QuestionTestCase(TestCase):
    def setUp(self):
        Question.objects.create()

    def test_question_to_string(self):
        question = Question.objects.get()
        self.assertEqual(str(question), "Question object (" + str(question.id) + ")")

class AnswerVersionTestCase(TestCase):
    def setUp(self):
        question = Question.objects.create()
        question_version = QuestionVersion.objects.create(question=question,
                                                          title="Question Version 1")
        AnswerVersion.objects.create(question_version=question_version,
                                     text="Answer 1")

    def test_answer_version_to_string(self):
        answer_version = AnswerVersion.objects.get()
        self.assertEqual(str(answer_version), "Answer 1")

class QuizTestCase(TestCase):
    def setUp(self):
        URLPath.create_root(title="Root")
        url = URLPath.create_urlpath(URLPath.root(), "slug",
                                     title="Title 2",
                                     content="Content")
        article = url.articles.first().article
        self.quiz = Quiz.objects.create(category=article)
        question = Question.objects.create(category=article)
        question_version = QuestionVersion.objects.create(question=question,
                                                          title="Question Version 1")
        answer = AnswerVersion.objects.create(question_version=question_version,
                                              text="Answer 1")
        UserAnswer.objects.create(quiz=self.quiz,
                                  question=question,
                                  answer=answer)

    def test_quiz_has_total_questions(self):
        self.assertEqual(self.quiz.total_questions(), 1)

    def test_quiz_calculates_score(self):
        # FIXME: calculation is broken... ?
        self.assertEqual(self.quiz.calculate_score(), 1)

class IndexViewTests(TestCase):

    def setUp(self):
        #self.client.force_login(User.objects.get_or_create(username='admin')[0])
        URLPath.create_root(title="Root")
        URLPath.create_urlpath(URLPath.root(), "at",
                               title="Title 1",
                               content="Content")
        URLPath.create_urlpath(URLPath.root(), "bt",
                               title="Title 1",
                               content="Content")
        poll = Poll.objects.create(title="Poll Title")
        JurcoachPage.objects.create(body="Jurcoach Body",
                                    title="Jurcoach Title",
                                    depth=0,
                                    poll=poll,
                                    path="/"
                                    )

    def test_index_response(self):
        response = self.client.get("/quiz/")
        self.assertContains(response, "jurcoach-page", status_code=200)
