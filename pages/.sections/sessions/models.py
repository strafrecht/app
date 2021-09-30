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

class SessionIndexPage(RoutablePageMixin, Page):

    def get_context(self, request):
        context = super().get_context(request)
        sessions = Sessions.objects.all()
        context['sessions'] = sessions
        return context

    @route('(?P<session>\d+)/$', name="session")
    def session_page(self, request, session):
        context = super().get_context(request)
        session = Sessions.objects.get(id=session)
        context['session'] = session
        return render(request, "pages/session_page.html", {'session': session})

#class SessionTags(TaggedItemBase):
#    content_object = ParentalKey(
#        'pages.Sessions', related_name='tagged_items', on_delete=models.CASCADE
#    )
    
@register_snippet
class Sessions(models.Model):
    SESSION_TYPE_CHOICES = [
        ('lecture', 'Vorlesung'),
        ('exercise', 'Übung'),
        ('study_group', 'Arbeitsgemeinschaft'),
        ('exam_prep', 'Klausurenkurs'),
        ('seminar', 'Seminar')
    ]
    SEMESTER_TYPE_CHOICES = [
        ('ss2022', 'Sommersemester 2022'),
        ('ws2022', 'Wintersemester 2022'),
        ('ss2021', 'Sommersemester 2021'),
        ('ws2021', 'Wintersemester 2021'),
        ('ss2020', 'Sommersemester 2020'),
        ('ws2020', 'Wintersemester 2020'),
        ('ss2019', 'Sommersemester 2019'),
        ('ws2019', 'Wintersemester 2019'),
        ('ss2018', 'Sommersemester 2018'),
        ('ws2018', 'Wintersemester 2018'),
    ]

    name = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    date = RichTextField(blank=True)
    #tags = ClusterTaggableManager(through=SessionTags, blank=True)
    speaker = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    type = models.CharField(
        choices=SESSION_TYPE_CHOICES,
        default='lecture',
        max_length=255,
        blank=True
    )
    semester = models.CharField(
        choices=SEMESTER_TYPE_CHOICES,
        default='ws2020',
        max_length=255,
        blank=True
    )
    assessment = RichTextField(blank=True)
    description = RichTextField(blank=True)
    speaker_description = RichTextField(blank=True)
    content = RichTextField(blank=True)
    location = RichTextField(blank=True)
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)

    panels = [
        MultiFieldPanel([
            FieldPanel('name', classname="col-12"),
            FieldPanel('subtitle', classname="col-12"),
        ], "Session"),
        MultiFieldPanel([
            FieldPanel('date', classname="col-12"),
            FieldPanel('type', classname="col-12"),
            FieldPanel('semester', classname="col-12"),
            FieldPanel('description', classname="col-12"),
            FieldPanel('assessment', classname="col-12"),
        ], "Info"),
        MultiFieldPanel([
            FieldPanel('speaker', classname="col-12"),
            FieldPanel('speaker_description', classname="col-12"),
        ], "Speaker"),
        MultiFieldPanel([
            FieldPanel('location', classname="col-12"),
            FieldPanel('lat', classname="col-6"),
            FieldPanel('lon', classname="col-6"),
        ], "Location"),
    ]

    search_fields = [
        index.SearchField('title'),
        index.SearchField('speaker'),
        index.SearchField('description'),
    ]

    class Meta:
        verbose_name = 'Lehrveranstaltung'
        verbose_name_plural = 'Lehrveranstaltungen'
        
