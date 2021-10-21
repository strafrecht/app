from django.db import models
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

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

    date = models.DateField(null=True, blank=True, verbose_name="Datum")
    paragraphs = RichTextField(blank=True, verbose_name="Paragraphen/Strafbarkeiten in der Klausur")
    problems = RichTextField(blank=True, verbose_name="Problemschwerpunkte der Klausur")
    sachverhalt_link = models.CharField('Link zum Sachverhalt', blank=True, max_length=255)
    loesung_link = models.CharField('Link zur Lösungsskizze', blank=True, max_length=255)
    difficulty = models.CharField(
        'Schwierigkeitsgrad',
        choices=EXAM_DIFFICULTY_CHOICES,
        max_length=255,
        blank=True
    )
    type = models.CharField(
        'Klausurtyp',
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
        ], "Klausur"),
    ]
    
    def paragraphs_html(self):
        return mark_safe(self.paragraphs)
    
    def problems_html(self):
        return mark_safe(self.problems)
    
    class Meta:
        verbose_name = 'Klausur'
        verbose_name_plural = 'Klausuren'
