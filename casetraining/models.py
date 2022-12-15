from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel

from wiki.models import Article

class Casetraining(ClusterableModel):

    DIFFICULTY_CHOICES = [
        ('shortcase',  'Shortcase'),
        ('beginner',   'Beginner'),
        ('advanced',   'Advanced'),
    ]

    name = models.CharField(max_length=100)
    difficulty = models.CharField(choices=DIFFICULTY_CHOICES, max_length=100, blank=False, null=False)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    # Sachverhalt
    facts = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} ({})".format(self.name, self.difficulty)

    panels = [
        FieldPanel('name'),
        FieldPanel('difficulty'),
        FieldPanel('user'),
        FieldPanel('facts'),
        InlinePanel('steps', heading='Steps'),
    ]

class CaseStep(ClusterableModel):

    STEP_TYPE_CHOICES = [
        ('read',          'Read'),
        ('mark_sections', 'Mark sections'),
        ('penalties',     'Penalties'),
        ('problem_areas', 'Problem areas'),
        ('weights',       'Weights'),
        ('gap_text',      'Gap text'),
        ('free_text',     'Free text'),
    ]

    case = ParentalKey(Casetraining, null=False, on_delete=models.CASCADE, related_name='steps')
    position = models.IntegerField()
    step_type = models.CharField(choices=STEP_TYPE_CHOICES, max_length=100, blank=False, null=False)
    config = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} ({}) {}".format(self.case, self.position, self.step_type)

    class Meta:
        unique_together = ('case', 'position',)

class CaseStepProblemArea(ClusterableModel):
    """ Ermitteln Sie die Problemfelder des 1. Sachverhaltsabschnitts. """
    case_step = ParentalKey(CaseStep, null=False, on_delete=models.CASCADE, related_name='problem_areas')
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True, blank=True)
    weight = models.IntegerField()

    def __str__(self):
        return "{} ({}) {}".format(self.case_step, self.article, self.weight)
