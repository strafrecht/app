from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.db import models
from wiki.models import ArticleRevision

SUBMISSION_STATUS = (
    ('APPROVED', 'Approved'),
    ('REJECTED', 'Rejected'),
    ('PENDING', 'Pending'),
)

class Submission(models.Model):
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='submitted_by')
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='reviewed_by')

    status = models.CharField(
        max_length=10,
        choices=SUBMISSION_STATUS,
        default='PENDING'
    )
    user_message = models.TextField(blank=True, null=True, verbose_name='Nachricht an Benutzer')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'content_id')
    message = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {} - {}".format(self.status, self.created.strftime("%d.%m.%Y %H:%M"), self.id)

    def save(self, *args, **kwargs):
        update = self.id != None
        super(Submission, self).save(*args, **kwargs)
        if update: return

        subject = "Neue Einreichung: {message}".format(message=self.message)
        text = """
        Einreichung:
        {site}/cms/core/submission/edit/{id}/

        Objekt: {object}
        User: {user}
        URL: {site}{url}
        """.format(site=settings.SITE_URL,
                   id=self.id,
                   object=self.content_object,
                   user=self.submitted_by,
                   url=self.url)
        send_mail(
            subject=subject,
            message=text,
            from_email='jukol@strafrecht-online.de',
            recipient_list=['jukol@strafrecht-online.de'],
            fail_silently=False,
        )

# https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#extending-django-s-default-user
# Create Profile: Profile.objects.create(user=u)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rewards = models.IntegerField(default=0, null=False)
