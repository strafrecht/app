from django.db import models
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.models import User

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
    StreamFieldPanel,
)

from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page, Collection
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

class ExamTable(Page):
    def __str__(self):
        print('exam table')
    

@register_snippet
class Exams(models.Model):

    EXAM_TYPE_CHOICES = [
        ('falltraining', 'Klausur im Falltraining'),
        ('exam','Examensklausur'),
        ('original-exam', 'Originalexamensklausur'),
        ('exercise', 'Übungsfall'),
        ('tutorial', 'AG-Fall'),
    ]
    EXAM_DIFFICULTY_CHOICES = [
        ('beginner','Anfänger'),
        ('intermediate','Fortgeschrittene'),
        ('advanced','Examen'),
    ]

    def __str__(self):
        return "{}".format(self.date)

    date = models.DateField(null=True, blank=True)
    paragraphs = RichTextField(blank=True)
    problems = RichTextField(blank=True)
    sachverhalt_link = models.CharField(blank=True, max_length=255)
    loesung_link = models.CharField(blank=True, max_length=255)
    difficulty = models.CharField(
        choices=EXAM_DIFFICULTY_CHOICES,
        max_length=255,
        blank=True
    )
    type = models.CharField(
        choices=EXAM_TYPE_CHOICES,
        max_length=255,
        blank=True
    )

    #tags = ClusterTaggableManager(through=EventTags, blank=True)

    panels = [
        MultiFieldPanel([
            FieldPanel('date', classname="col-12"),
            FieldPanel('type', classname="col-12"),
            FieldPanel('difficulty', classname="col-12"),
            FieldPanel('paragraphs', classname="col-12"),
            FieldPanel('problems', classname="col-12"),
            FieldPanel('sachverhalt_link', classname="col-12"),
            FieldPanel('loesung_link', classname="col-12"),
        ], "Exam"),
    ]

    class Meta:
        verbose_name = 'Klausur'
        verbose_name_plural = 'Klausuren'
