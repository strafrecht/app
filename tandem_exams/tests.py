from django.contrib.auth.models import User
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
import base64

from .models import *

def pdf_test_file():
    return (
        b"%PDF-1.2 \n"
        b"9 0 obj\n<<\n>>\nstream\nBT/ 32 Tf(  YOUR TEXT HERE   )' ET\nendstream\nendobj\n"
        b"4 0 obj\n<<\n/Type /Page\n/Parent 5 0 R\n/Contents 9 0 R\n>>\nendobj\n"
        b"5 0 obj\n<<\n/Kids [4 0 R ]\n/Count 1\n/Type /Pages\n/MediaBox [ 0 0 250 50 ]\n>>\nendobj\n"
        b"3 0 obj\n<<\n/Pages 5 0 R\n/Type /Catalog\n>>\nendobj\n"
        b"trailer\n<<\n/Root 3 0 R\n>>\n"
        b"%%EOF"
    )

class TandemExamTestCase(TestCase):
    def setUp(self):
        self.obj = TandemExam.objects.create(
            name="Tandem exam 1",
            approved=True,
            description="Description for tandem exam 1",
            difficulty="advanced",
        )

    def test_has_difficulty(self):
        self.assertEqual(self.obj.difficulty, "advanced")

    def test_to_string(self):
        self.assertEqual(str(self.obj), "Tandem exam 1")

    def test_has_title(self):
        self.assertEqual(self.obj.title(), str(self.obj))

class ExamSolutionTestCase(TestCase):
    def setUp(self):
        self.pdf_file = SimpleUploadedFile("test_file.pdf", pdf_test_file(),
                                           content_type="application/pdf")
        self.pdf_file2 = SimpleUploadedFile("test_file.pdf", pdf_test_file(),
                                            content_type="application/pdf")
        user = User.objects.create(username='testuser', password='12345', first_name="Andrea")
        exam = TandemExam.objects.create(
            name="Tandem exam 1",
            approved=True,
            description="Description for tandem exam 1",
            difficulty="advanced",
        )
        self.obj = ExamSolution.objects.create(
            exam=exam,
            user=user,
        )

    def test_has_default_state(self):
        self.assertEqual(self.obj.state, "NEW")

    def test_has_file(self):
        self.obj.file = self.pdf_file
        self.obj.save()
        self.assertIn("exam_solutions/{}/file/".format(self.obj.pk), str(self.obj.file))
        self.assertIn("/Gutachten-", str(self.obj.file))

    def test_has_correction(self):
        self.obj.correction = self.pdf_file
        self.obj.save()
        self.assertIn("exam_solutions/{}/correction/".format(self.obj.pk), str(self.obj.correction))
        self.assertIn("/Korrektur-", str(self.obj.correction))

    # FIXME: why does this not work???
    # https://docs.djangoproject.com/en/3.2/topics/testing/tools/#email-services
    # def test_upload_new_correction_sends_mail(self):
    #     self.obj.upload_correction(self.pdf_file, self.pdf_file2)
    #     self.assertEquals(1, len(mail.outbox))


class ViewTestCase(TestCase):
    def setUp(self):
        self.pdf_file = SimpleUploadedFile("test_file.pdf", pdf_test_file(),
                                           content_type="application/pdf")
        self.pdf_file2 = SimpleUploadedFile("test_file.pdf", pdf_test_file(),
                                           content_type="application/pdf")
        self.user = User.objects.create(username='testuser', password='12345', first_name="Andrea")
        self.user2 = User.objects.create(username='testuser2', password='12345', first_name="Michael")
        self.exam1 = TandemExam.objects.create(
            name="Advanced-Approved",
            description="Advanced-Approved-Description",
            difficulty="advanced",
            approved=True,
        )
        self.exam2 = TandemExam.objects.create(
            name="Advanced-Not-Approved",
            description="Advanced-Not-Approved-Description",
            difficulty="advanced",
        )
        TandemExam.objects.create(
            name="Beginner-Approved",
            description="Beginner-Approved-Description",
            difficulty="beginner",
            approved=True,
        )
        TandemExam.objects.create(
            name="Beginner-Not-Approved",
            description="Beginner-Not-Approved-Description",
            difficulty="beginner",
        )

    def test_index_response(self):
        response = self.client.get("/tandemklausuren/")
        self.assertContains(response, "<h2>Tandemklausuren</h2>", status_code=200)
        self.assertContains(response, "Advanced-Approved")
        self.assertContains(response, "Beginner-Approved")
        self.assertNotContains(response, "Advanced-Not-Approved")
        self.assertNotContains(response, "Beginner-Not-Approved")

    def test_show_response(self):
        response = self.client.get("/tandemklausuren/{}/".format(self.exam1.id))
        self.assertContains(response, "Advanced-Approved", status_code=200)
        self.assertContains(response, "Advanced-Approved-Description")

    def test_deny_show_for_not_approved_exam_response(self):
        response = self.client.get("/tandemklausuren/{}/".format(self.exam2.id))
        self.assertContains(response, "", status_code=404)

    def test_anonymous_upload_new_solution(self):
        response = self.client.post(
            "/tandemklausuren/{}/new/".format(self.exam1.id),
            {}
        )
        self.assertRedirects(response,
                             '/profile/login/?next=/tandemklausuren/{}/new/'.format(self.exam1.id),
                             status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_upload_new_solution_with_no_other_new_solutions(self):
        self.assertEquals(0, self.user.exam_solutions.count())
        self.assertEquals(0, self.user.exam_solution_corrections.count())
        self.client.force_login(self.user)
        response = self.client.post(
            "/tandemklausuren/{}/new/".format(self.exam1.id),
            { "file": self.pdf_file },
            follow=True
        )
        self.assertRedirects(response,
                             '/tandemklausuren/{}/'.format(self.exam1.id),
                             status_code=302, target_status_code=200)
        self.assertContains(response, "Gutachten erfolgreich hochgeladen. Wir schicken eine Nachricht, sobald ein Tandempartner / eine Tandempartnerin gefunden wurde.", status_code=200)
        self.assertEquals(1, self.user.exam_solutions.count())
        self.assertEquals(0, self.user.exam_solution_corrections.count())

    def test_upload_new_solution_with_another_users_new_solutions(self):
        ExamSolution.objects.create(
            exam=self.exam1,
            user=self.user2,
        )
        self.assertEquals(0, self.user.exam_solutions.count())
        self.assertEquals(0, self.user.exam_solution_corrections.count())
        self.assertEquals(1, self.user2.exam_solutions.count())
        self.assertEquals(0, self.user2.exam_solution_corrections.count())
        self.client.force_login(self.user)
        response = self.client.post(
            "/tandemklausuren/{}/new/".format(self.exam1.id),
            { "file": self.pdf_file },
            follow=True
        )
        self.assertContains(response, "Gutachten erfolgreich hochgeladen. Ein anderes Gutachten wurde Dir zur Korrektur zugewiesen. Du findest das Gutachten in deinem Profil.", status_code=200)
        self.assertEquals(1, self.user.exam_solutions.count())
        self.assertEquals(1, self.user.exam_solution_corrections.count())
        self.assertEquals(1, self.user2.exam_solutions.count())
        self.assertEquals(1, self.user2.exam_solution_corrections.count())

    def test_anonymous_upload_new_correction(self):
        response = self.client.post(
            "/tandemklausuren/{}/new_correction/".format(1),
            {}
        )
        self.assertContains(response, '', status_code=302)

    def test_upload_new_correction_wrong_state(self):
        solution = ExamSolution.objects.create(
            exam=self.exam1,
            user=self.user2,
            state="CORRECTED",
            correction_by=self.user,
        )
        self.client.force_login(self.user)
        response = self.client.post(
            "/tandemklausuren/{}/new_correction/".format(solution.id),
            {}
        )
        self.assertContains(response, '', status_code=404)

    def test_upload_new_correction_wrong_user(self):
        solution = ExamSolution.objects.create(
            exam=self.exam1,
            user=self.user2,
            state="ACCEPTED",
            correction_by=self.user2,
        )
        self.client.force_login(self.user)
        response = self.client.post(
            "/tandemklausuren/{}/new_correction/".format(solution.id),
            {}
        )
        self.assertContains(response, '', status_code=404)

    def test_upload_new_correction(self):
        solution = ExamSolution.objects.create(
            exam=self.exam1,
            user=self.user2,
            state="ACCEPTED",
            correction_by=self.user,
        )
        self.client.force_login(self.user)
        response = self.client.post(
            "/tandemklausuren/{}/new_correction/".format(solution.id),
            { "correction":       self.pdf_file,
            },
        )
        self.assertRedirects(response,
                             "/profile/tandemklausuren/",
                             status_code=302,
                             target_status_code=200, fetch_redirect_response=True)
        solution.refresh_from_db()
        self.assertEquals("CORRECTED", solution.state)
