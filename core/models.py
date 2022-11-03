from django.db import models
from django.contrib.auth.models import User
from wiki.models import ArticleRevision

SUBMISSION_STATUS = (
    ('APPROVED', 'Approved'),
    ('REJECTED', 'Rejected'),
    ('PENDING', 'Pending'),
)

class Submission(models.Model):
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='submitted_by')
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='reviewed_by')
    article_revision = models.ForeignKey(ArticleRevision, on_delete=models.SET_NULL, blank=True, null=True)
    #question_version = models.ForeignKey(QuestionVersion, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    status = models.CharField(
        max_length=10,
        choices=SUBMISSION_STATUS,
        default='PENDING'
    )
    message = models.TextField(blank=True, null=True)
