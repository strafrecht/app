from django.db import models
from django.db.models import Q
from django.shortcuts import render
from django.utils.safestring import mark_safe

from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
)
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.snippets.models import register_snippet

class ExamTable(Page):
    class Meta:
        verbose_name = "Klausurdatenbank-Seite"

    def __str__(self):
        return 'exam table'


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
        ('intermediate','Examen'),
        ('advanced','Fortgeschrittene'),
        ('shortcases','Kurzfälle'),
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
    sachverhalt_dl = models.ForeignKey('wagtaildocs.Document', blank=True, null=True, on_delete=models.SET_NULL,
                                       related_name='+', verbose_name='Sachverhalt [PDF]')
    loesung_dl     = models.ForeignKey('wagtaildocs.Document', blank=True, null=True, on_delete=models.SET_NULL,
                                       related_name='+', verbose_name='Lösung [PDF]')

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
        DocumentChooserPanel('sachverhalt_dl'),
        DocumentChooserPanel('loesung_dl'),
    ]

    def paragraphs_html(self):
        return mark_safe(self.paragraphs)

    def problems_html(self):
        return mark_safe(self.problems)

    class Meta:
        verbose_name = 'Klausur'
        verbose_name_plural = 'Klausuren'
