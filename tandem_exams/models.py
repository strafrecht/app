from django.conf import settings
from django.contrib.auth.models import User
from django.core import mail
from django.db import models, transaction, IntegrityError
from django.utils.translation import gettext_lazy as _
from wagtail.core.fields import RichTextField
import uuid

class TandemExam(models.Model):

    class Meta:
        verbose_name = "Tandemklausur"
        verbose_name_plural = "Tandemklausuren"

    DIFFICULTY_CHOICES = [
        ('beginner',   _('beginner')),
        ('advanced',   _('advanced')),
    ]

    name = models.CharField(max_length=100, blank=False, null=False)
    difficulty = models.CharField(choices=DIFFICULTY_CHOICES, max_length=100, blank=False, null=False)
    description = RichTextField(default='')
    approved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.name)

    def title(self):
        return self.__str__()


class ExamSolution(models.Model):

    class Meta:
        verbose_name = "Klausurlösung"
        verbose_name_plural = "Klausurlösungen"

    STATE_CHOICES = [
        ('NEW',       _('new')),
        ('ACCEPTED',  _('accepted')),
        ('CORRECTED', _('corrected')),
    ]

    def upload_target(self, name, filename):
        return "exam_solutions/{}/{}/{}/{}".format(
            self.pk,
            name,
            uuid.uuid4(),
            "{}-{}.pdf".format(filename, self.exam.title())
        )

    def file_target(instance, filename):
        return instance.upload_target("file", "Lösung")

    def correction_target(instance, filename):
        return instance.upload_target("correction", "Korrektur")

    def correction_sheet_target(instance, filename):
        return instance.upload_target("correction_sheet", "Korrekturbogen")

    exam = models.ForeignKey(TandemExam, on_delete=models.CASCADE, related_name='solutions')
    file = \
        models.FileField(blank=True, null=True,
                         upload_to=file_target,
                         verbose_name=_('Lösung'))
    correction = \
        models.FileField(blank=True, null=True,
                         upload_to=correction_target,
                         verbose_name=_('Korrektur'))
    correction_sheet = \
        models.FileField(blank=True, null=True,
                         upload_to=correction_sheet_target,
                         verbose_name=_('Korrekturbogen'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False, related_name='exam_solutions')
    correction_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='exam_solution_corrections')
    state = models.CharField(choices=STATE_CHOICES, default="NEW", max_length=100, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def tandem_exam(self):
        try:
            return ExamSolution.objects.filter(
                exam=self.exam,
                user=self.correction_by,
                correction_by=self.user,
            ).get()
        except ExamSolution.DoesNotExist:
            return None

    @transaction.atomic
    def find_tandem_partner(self):
        try:
            with transaction.atomic():
                partner_solution = ExamSolution.objects.filter(
                    exam=self.exam,
                    correction_by=None,
                    state="NEW",
                ).exclude(user=self.user).get()
                partner_solution.correction_by = self.user
                partner_solution.state = "ACCEPTED"
                partner_solution.save()
                partner_solution.notify_accepted()
                self.correction_by = partner_solution.user
                self.state = "ACCEPTED"
                self.save()
                return True
        except (IntegrityError, ExamSolution.DoesNotExist) as e:
            return False

    def upload_correction(self, correction, sheet):
        self.correction = correction
        self.correction_sheet = sheet
        self.state = "CORRECTED"
        self.save()
        self.notify_corrected()

    def notify_accepted(self):
        recipient = self.user.email
        subject = "Tandemklausur: {}".format(self.exam)

        text = """
        Hallo {first_name},

        es wurde ein Tandempartner zu Deiner Klausurlösung gefunden! Du kannst
        nun seine Tandemklausur korrigieren.
        Du findest diese in Deinem Nutzerprofil:
        {site}/profile/tandemklausuren/

        Dein Jurcoach-Team
        """.format(site=settings.SITE_URL,
                   first_name=self.user.first_name)

        mail.send_mail(
            subject=subject,
            message=text,
            from_email='jukol@strafrecht-online.de',
            recipient_list=[recipient],
            fail_silently=False,
        )

    def notify_corrected(self):
        recipient = self.user.email
        subject = "Tandemklausur: {}".format(self.exam)

        text = """
        Hallo {first_name},

        es wurde eine Korrektur zu Deiner Tandemklausur hochgeladen. Du kannst
        die Korrektur in Deinem Nutzerprofil einsehen:
        {site}/profile/tandemklausuren/

        Dein Jurcoach-Team
        """.format(site=settings.SITE_URL,
                   first_name=self.user.first_name)

        mail.send_mail(
            subject=subject,
            message=text,
            from_email='jukol@strafrecht-online.de',
            recipient_list=[recipient],
            fail_silently=False,
        )