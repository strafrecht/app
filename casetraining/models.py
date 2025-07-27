import bleach
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel

from wiki.models import Article

from core.models import Submission

class Casetraining(ClusterableModel):

    class Meta:
        verbose_name = "Falltraining"

    DIFFICULTY_CHOICES = [
        ('shortcase',  'Shortcase'),
        ('beginner',   'Beginner'),
        ('advanced',   'Advanced'),
    ]

    name = models.CharField(max_length=100)
    difficulty = models.CharField(choices=DIFFICULTY_CHOICES, max_length=100, blank=False, null=False)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    # sachverhalt
    facts = models.TextField(default='')
    # our json config for the steps
    steps = models.TextField(null=True, blank=True)
    # slug der lösungsskizze
    solution_slug = models.TextField(null=True, blank=True)
    approved = models.BooleanField(default=False)
    parent = models.ForeignKey("Casetraining", null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    submission = models.ForeignKey(Submission, null=True, on_delete=models.SET_NULL)

    def save(self, *args, **kwargs):
        self.facts      = bleach.clean(self.facts,
                                       tags=["p", "span", "li", "ol", "ul", "strong"],
                                       attributes=["style"], styles=["background-color"])
        self.difficulty = bleach.clean(self.difficulty)
        self.steps      = bleach.clean(self.steps)
        self.name       = bleach.clean(self.name)
        super(Casetraining, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.name)

    def title(self):
        return self.__str__()

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
