from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel

from wiki.models import Article

from core.models import Submission

class Casetraining(ClusterableModel):

    DIFFICULTY_CHOICES = [
        ('shortcase',  'Shortcase'),
        ('beginner',   'Beginner'),
        ('advanced',   'Advanced'),
    ]

    name = models.CharField(max_length=100)
    difficulty = models.CharField(choices=DIFFICULTY_CHOICES, max_length=100, blank=False, null=False)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    # Sachverhalt
    facts = models.TextField(default='')
    # our json config for the steps
    steps = models.TextField(null=True, blank=True)
    approved = models.BooleanField(default=False)
    parent = models.ForeignKey("Casetraining", null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    submission = models.ForeignKey(Submission, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return "{} ({})".format(self.name, self.difficulty)

    def listing_class(self):
        if self.approved:
            return ""

        if self.submission:
            return "text-success"

        return "text-danger"

    panels = [
        FieldPanel('name'),
        FieldPanel('difficulty'),
        FieldPanel('approved'),
        FieldPanel('user'),
        FieldPanel('facts'),
        FieldPanel('steps'),
    ]
