from django.test import TestCase

from django.contrib.auth.models import User

from pages.models.jurcoach import JurcoachPage
from wagtailpolls.models import Poll

from .models import Casetraining

class CasetrainingTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='testuser', password='12345')
        self.obj = Casetraining.objects.create(name="Test case 1", difficulty="advanced", user=user)

    def test_has_difficulty(self):
        self.assertEqual(self.obj.difficulty, "advanced")

    def test_to_string(self):
        self.assertEqual(str(self.obj), "Test case 1 (advanced)")

class IndexViewTestCase(TestCase):

    def setUp(self):
        user = User.objects.create(username='testuser', password='12345')
        poll = Poll.objects.create(title="Poll Title")
        JurcoachPage.objects.create(
            body="Jurcoach Body",
            title="Jurcoach Title",
            depth=0,
            poll=poll,
            path="/"
        )
        Casetraining.objects.create(name="Advanced 1", difficulty="advanced", user=user)
        Casetraining.objects.create(name="Beginner 1", difficulty="beginner", user=user)
        Casetraining.objects.create(name="Shortcase 1", difficulty="shortcase", user=user)

    def test_index_response(self):
        response = self.client.get("/falltraining/")
        self.assertContains(response, "<h2>Falltraining</h2>", status_code=200)
        self.assertContains(response, "Advanced 1")
        self.assertContains(response, "Beginner 1", status_code=200)
        self.assertContains(response, "Shortcase 1", status_code=200)
