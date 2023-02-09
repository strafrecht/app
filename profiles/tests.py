from django.test import TestCase

from django.contrib.auth.models import User

from wiki.models import Article, ArticleRevision, URLPath
from tandem_exams.models import *

class BookmarkViewTestCase(TestCase):

    def setUp(self):
        # create wiki entry
        URLPath.create_root(title="Root")
        url = URLPath.create_urlpath(URLPath.root(), "slug",
                                     title="Wiki-Title",
                                     content="Content")
        self.article = url.articles.first().article
        self.user = User.objects.get_or_create(username='testuser')[0]

    def test_bookmarks_login_redirect(self):
        response = self.client.get("/profile/bookmarks/")
        self.assertRedirects(response, '/profile/login/?next=/profile/bookmarks/',
                             status_code=302,
                             target_status_code=200,
                             fetch_redirect_response=True)

    def test_bookmarks_response(self):
        self.client.force_login(self.user)
        self.user.bookmarks.create(content_object=self.article)
        response = self.client.get("/profile/bookmarks/")
        self.assertContains(response, "<h3>Deine Lesezeichen</h3>", status_code=200)
        self.assertContains(response, "Wiki-Title")

    def test_bookmark_create(self):
        self.client.force_login(self.user)
        response = self.client.post("/profile/bookmarks/create/{}".format(self.article.id))
        self.assertEqual(self.article, self.user.bookmarks.first().content_object)

    def test_bookmark_delete(self):
        self.client.force_login(self.user)
        self.user.bookmarks.create(content_object=self.article)
        self.assertEqual(1, self.user.bookmarks.count())
        response = self.client.post("/profile/bookmarks/delete/{}".format(self.article.id))
        self.assertEqual(0, self.user.bookmarks.count())

class ViewTestCase(TestCase):

    def setUp(self):
        # nothing
        setup = None
        self.user = User.objects.get_or_create(username='testuser')[0]

    def test_index_login_redirect(self):
        response = self.client.get("/profile/")
        self.assertRedirects(response, '/profile/login/?next=/profile/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_index_response(self):
        self.client.force_login(self.user)
        response = self.client.get("/profile/")
        self.assertContains(response, "<h3>Dein Jurcoach Profil</h3>", status_code=200)

    def test_submissions_login_redirect(self):
        response = self.client.get("/profile/submissions/")
        self.assertRedirects(response, '/profile/login/?next=/profile/submissions/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_submissions_response(self):
        self.client.force_login(self.user)
        response = self.client.get("/profile/submissions/")
        self.assertContains(response, "<h3>Deine Einreichungen</h3>", status_code=200)

    def test_quizzes_login_redirect(self):
        response = self.client.get("/profile/quizzes/")
        self.assertRedirects(response, '/profile/login/?next=/profile/quizzes/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_quizzes_response(self):
        self.client.force_login(self.user)
        response = self.client.get("/profile/quizzes/")
        self.assertContains(response, "<h3>Deine MCT Ergebnisse</h3>", status_code=200)

    def test_flashcards_login_redirect(self):
        response = self.client.get("/profile/flashcards/")
        self.assertRedirects(response, '/profile/login/?next=/profile/flashcards/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_flashcards_response(self):
        self.client.force_login(self.user)
        response = self.client.get("/profile/flashcards/")
        self.assertContains(response, "<deck>", status_code=200)

    def test_exam_solutions_login_redirect(self):
        response = self.client.get("/profile/tandemklausuren/")
        self.assertRedirects(response, '/profile/login/?next=/profile/tandem_exams/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_exam_solutions_response(self):
        self.client.force_login(self.user)
        exam = TandemExam.objects.create(
            name="Tandem exam 1",
            approved=True,
            description="Description for tandem exam 1",
            difficulty="advanced",
        )
        ExamSolution.objects.create(
            exam=exam,
            user=self.user,
        )
        ExamSolution.objects.create(
            exam=exam,
            user=self.user,
            correction_by=self.user,
        )

        response = self.client.get("/profile/tandemklausuren/")
        self.assertContains(response, "<h3>Tandem exam 1</h3>", status_code=200)
