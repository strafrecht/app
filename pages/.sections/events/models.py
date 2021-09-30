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
    
@register_snippet
class Events(models.Model):
    EVENT_TYPE_CHOICES = [
        ('tacheles', 'Tacheles'),
        ('sonstige', 'Sonstige')
    ]

    SEMESTER_TYPE_CHOICES = [
        ('2024_2', 'Wintersemester 2024/2025'),
        ('2024_1', 'Sommersemester 2024'),
        ('2023_2', 'Wintersemester 2023/2024'),
        ('2023_1', 'Sommersemester 2023'),
        ('2022_2', 'Wintersemester 2022/2023'),
        ('2022_1', 'Sommersemester 2022'),
        ('2021_2', 'Wintersemester 2021/2022'),
        ('2021_1', 'Sommersemester 2021'),
        ('2020_2', 'Wintersemester 2020/2021'),
        ('2020_1', 'Sommersemester 2020'),
        ('2019_2', 'Wintersemester 2019/2020'),
        ('2019_1', 'Sommersemester 2019'),
        ('2018_2', 'Wintersemester 2018/2019'),
        ('2018_1', 'Sommersemester 2018'),
        ('2017_2', 'Wintersemester 2017/2018'),
        ('2017_1', 'Sommersemester 2017'),
        ('2016_2', 'Wintersemester 2016/2017'),
        ('2016_1', 'Sommersemester 2016'),
        ('2015_2', 'Wintersemester 2015/2016'),
        ('2015_1', 'Sommersemester 2015'),
        ('2014_2', 'Wintersemester 2014/2015'),
        ('2014_1', 'Sommersemester 2014'),
        ('2013_2', 'Wintersemester 2013/2014'),
        ('2013_1', 'Sommersemester 2013'),
        ('2012_2', 'Wintersemester 2012/2013'),
        ('2012_1', 'Sommersemester 2012'),
        ('2011_2', 'Wintersemester 2011/2012'),
        ('2011_1', 'Sommersemester 2011'),
        ('2010_2', 'Wintersemester 2010/2011'),
        ('2010_1', 'Sommersemester 2010'),
    ]

    name = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateTimeField()
    semester = models.CharField(
        choices=SEMESTER_TYPE_CHOICES,
        default='ss2021',
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
    speaker = models.CharField(max_length=255, null=True, blank=True)
    youtube_link = models.CharField(max_length=500, null=True, blank=True)
    newsletter_link = models.CharField(max_length=500, null=True, blank=True)
    type = models.CharField(
        choices=EVENT_TYPE_CHOICES,
        default='tacheles',
        max_length=255,
        blank=True
    )
    description = RichTextField(blank=True)
    speaker_description = RichTextField(blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    showmap = models.BooleanField(default=False)
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)

    panels = [
        MultiFieldPanel([
            FieldPanel('name', classname="col-12"),
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
            FieldPanel('speaker', classname="col-12"),
            FieldPanel('speaker_description', classname="col-12"),
        ], "Speaker"),
        MultiFieldPanel([
            FieldPanel('youtube_link', classname="col-12"),
            FieldPanel('newsletter_link', classname="col-12"),
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
    def thumb_image(self):
        try:
            return self.image.get_rendition('fill-120x120').img_tag()
        except:
            return ''

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
