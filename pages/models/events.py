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
from wagtail.documents.models import Document
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.core import blocks
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from django.shortcuts import get_object_or_404, render

from pages.models.sidebar import (
    SidebarSimpleBlock,
    SidebarHeaderBlock,
    SidebarTitleBlock,
    SidebarBorderBlock,
    SidebarImageTextBlock,
)

class EventsBlock(blocks.StructBlock):
    class Meta:
        template = 'blocks/widgets/events_block.html'

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context['events'] = EventPage.objects.filter(type='tacheles')
        return context

# Content Blocks
class ContentBlocks(blocks.StreamBlock):
    richtext = blocks.RichTextBlock()
    events_block = EventsBlock()

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        return context

# Sidebar Blocks
class SidebarBlocks(blocks.StreamBlock):
    sidebar_title = SidebarTitleBlock()
    sidebar_header = SidebarHeaderBlock()
    sidebar_border = SidebarBorderBlock()
    sidebar_simple = SidebarSimpleBlock()
    sidebar_image_text = SidebarImageTextBlock()

class EventsPage(RoutablePageMixin, Page):
    content = StreamField([
        ('content', ContentBlocks()),
    ], block_counts={
        'content': {'min_num': 1, 'max_num': 1},
    })

    sidebar = StreamField(SidebarBlocks(required=False), blank=True)

    content_panels = [
        FieldPanel('title'),
        FieldRowPanel([
            FieldPanel('content', classname='col8'),
            FieldPanel('sidebar', classname='col4'),
        ], classname='full')
    ]

    template = 'page.html'

    @route(r'^(?P<semester>[\w-]+)/(?P<slug>[\w-]+)/?$')
    def event_by_semester(self, request, semester, slug):
        event = get_object_or_404(
            EventPage,
            semester=semester,
            slug=slug
        )
        a = "sos-2021"
        b = "triage-in-der-covid-19-pandemie-nur-theoretische-debatte-oder-bereits-realität-insbes-bei-menschen-mit-behinderung"
        print(a)
        print(b)
        print(event)
        return event.serve(request)

class EventPage(Page):
    EVENT_TYPE_CHOICES = [
        ('tacheles', 'Tacheles'),
        ('sonstige', 'Sonstige')
    ]

    SEMESTER_TYPE_CHOICES = [
        ('ws-2024', 'Wintersemester 2024/2025'),
        ('sos-2024', 'Sommersemester 2024'),
        ('ws-2023', 'Wintersemester 2023/2024'),
        ('sos-2023', 'Sommersemester 2023'),
        ('ws-2022', 'Wintersemester 2022/2023'),
        ('sos-2022', 'Sommersemester 2022'),
        ('ws-2021', 'Wintersemester 2021/2022'),
        ('sos-2021', 'Sommersemester 2021'),
        ('ws-2020', 'Wintersemester 2020/2021'),
        ('sos-2020', 'Sommersemester 2020'),
        ('ws-2019', 'Wintersemester 2019/2020'),
        ('sos-2019', 'Sommersemester 2019'),
        ('ws-2018', 'Wintersemester 2018/2019'),
        ('sos-2018', 'Sommersemester 2018'),
        ('ws-2017', 'Wintersemester 2017/2018'),
        ('sos-2017', 'Sommersemester 2017'),
        ('ws-2016', 'Wintersemester 2016/2017'),
        ('sos-2016', 'Sommersemester 2016'),
        ('ws-2015', 'Wintersemester 2015/2016'),
        ('sos-2015', 'Sommersemester 2015'),
        ('ws-2014', 'Wintersemester 2014/2015'),
        ('sos-2014', 'Sommersemester 2014'),
        ('ws-2013', 'Wintersemester 2013/2014'),
        ('sos-2013', 'Sommersemester 2013'),
        ('ws-2012', 'Wintersemester 2012/2013'),
        ('sos-2012', 'Sommersemester 2012'),
        ('ws-2011', 'Wintersemester 2011/2012'),
        ('sos-2011', 'Sommersemester 2011'),
        ('ws-2010', 'Wintersemester 2010/2011'),
        ('sos-2010', 'Sommersemester 2010'),
    ]

    subtitle = models.CharField("Untertitel", max_length=255, null=True, blank=True)
    date = models.DateTimeField()
    semester = models.CharField("Semester", 
        choices=SEMESTER_TYPE_CHOICES,
        max_length=255,
        blank=True
    )
    #tags = ClusterTaggableManager(through=EventTags, blank=True)
    poster_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    poster_pdf = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    youtube_link = models.CharField("Link zur Aufzeichnung des Vortrags auf YouTube", max_length=500, null=True, blank=True)
    newsletter = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    type = models.CharField("Tacheles-Vortrag oder Sonstiges?"person's first name", ", 
        choices=EVENT_TYPE_CHOICES,
        default='tacheles',
        max_length=255,
        blank=True
    )
    description = RichTextField(blank=True)
    speaker_description = RichTextField(blank=True)
    location = models.CharField("Ort", max_length=255, null=True, blank=True)
    showmap = models.BooleanField(default=False)
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)
    sidebar = True

    content_panels = [
        MultiFieldPanel([
            FieldPanel('title', classname="col-12"),
            FieldPanel('subtitle', classname="col-12"),
        ], "Event"),
        MultiFieldPanel([
            FieldPanel('semester', classname="col-12"),
            FieldPanel('date', classname="col-12"),
            FieldPanel('type', classname="col-12"),
            FieldPanel('description', classname="col-12"),
        ], "Info"),
        MultiFieldPanel([
            ImageChooserPanel('poster_image', classname="col-12"),
            DocumentChooserPanel('poster_pdf', classname="col-12"),
        ], "Poster"),
        MultiFieldPanel([
            FieldPanel('speaker_description', classname="col-12"),
        ], "Speaker"),
        MultiFieldPanel([
            FieldPanel('youtube_link', classname="col-12"),
            DocumentChooserPanel('newsletter', classname="col-12"),
        ], "Links"),
        MultiFieldPanel([
            FieldPanel('location', classname="col-12"),
            FieldPanel('showmap', classname="col-12"),
            FieldPanel('lat', classname="col-6"),
            FieldPanel('lon', classname="col-6"),
        ], "Location"),
    ]

    search_fields = [
        index.SearchField('title'),
        index.SearchField('speaker'),
    ]

    @property
    def events_page(self):
        return self.get_parent().specific

    def get_absolute_url(self):
        return self.get_url()
    
    @property
    def thumb_image(self):
        try:
            return self.image.get_rendition('fill-120x120').img_tag()
        except:
            return ''

    def __str__(self):
        return '{}'.format(self.title)

    def get_context(self, request):
        context = super().get_context(request)
        context['request'] = request
        context['event'] = EventPage.objects.get(semester=self.semester, slug=self.slug)
        return context
    
    parent_page_types = [EventsPage]

    template = 'pages/event_page.html'
