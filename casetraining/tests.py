from django.test import TestCase

from pages.models.jurcoach import JurcoachPage
from wagtailpolls.models import Poll

class IndexTestCase(TestCase):

    def setUp(self):
        poll = Poll.objects.create(title="Poll Title")
        JurcoachPage.objects.create(
            body="Jurcoach Body",
            title="Jurcoach Title",
            depth=0,
            poll=poll,
            path="/"
        )

    def test_index_response(self):
        response = self.client.get("/falltraining/")
        self.assertContains(response, "casetraining", status_code=200)
