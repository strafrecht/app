from django.test import TestCase

from django.contrib.auth.models import User

from pages.models.jurcoach import JurcoachPage
from wagtailpolls.models import Poll

from .models import Casetraining

class CasetrainingTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='testuser', password='12345')
        self.obj = Casetraining.objects.create(
            name="Test case 1",
            difficulty="advanced",
            user=user,
            steps="",
            facts="Case facts"
        )

    def test_has_difficulty(self):
        self.assertEqual(self.obj.difficulty, "advanced")

    def test_to_string(self):
        self.assertEqual(str(self.obj), "Test case 1 (advanced)")

class ViewTestCase(TestCase):

    def setUp(self):
        user = User.objects.create(username='testuser', password='12345')
        poll = Poll.objects.create(title="Poll Title")
        Casetraining.objects.create(name="Beginner 1", difficulty="beginner", user=user, steps="", approved=True)
        Casetraining.objects.create(name="Shortcase 1", difficulty="shortcase", user=user, steps="", approved=True)
        self.case = Casetraining.objects.create(name="Advanced 1", difficulty="advanced", user=user, steps="", facts="Case facts", approved=True)
        self.case_hidden = Casetraining.objects.create(name="Shortcase 2", difficulty="shortcase", user=user, steps="", approved=False)

    def test_index_response(self):
        response = self.client.get("/falltraining/")
        self.assertContains(response, "<h2>Falltraining</h2>", status_code=200)
        self.assertContains(response, "Advanced 1")
        self.assertContains(response, "Beginner 1")
        self.assertContains(response, "Shortcase 1")
        self.assertNotContains(response, "Shortcase 2")

    def test_show_response(self):
        response = self.client.get("/falltraining/show/{}/".format(self.case.id))
        self.assertContains(response, "<case>", status_code=200)

    def test_deny_api_access_to_not_approved_response(self):
        response = self.client.get("/falltraining/api/case/{}.json".format(self.case_hidden.id))
        self.assertContains(response, "", status_code=404)
