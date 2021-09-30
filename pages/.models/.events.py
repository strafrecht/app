from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

class EventsIndexPage(Page):
    def get_content(self, request):
        events = EventPage.objects.all()
        context['events'] = events
        return context

class EventPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'website.EventPage', related_name='tagged_items', on_delete=models.CASCADE
    )

class EventPage(Page):
    EVENT_TYPE_CHOICES = [
        ('tacheles', 'Tacheles'),
        ('sonstige', 'Sonstige')
    ]
    event_date = models.DateField()
    tags = ClusterTaggableManager(through=EventPageTag, blank=True)
    poster = models.ImageField(null=True, blank=True)
    speaker = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(
        choices=EVENT_TYPE_CHOICES,
        default='tacheles',
        max_length=255,
        blank=True
    )
    description = RichTextField(blank=True)
    speaker_description = RichTextField(blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('event_date'),
            FieldPanel('description'),
        ], heading='Event'),
        MultiFieldPanel([
            FieldPanel('type'),
            InlinePanel('poster_image'),
        ], heading='Extra'),
        MultiFieldPanel([
            FieldPanel('speaker'),
            FieldPanel('speaker_description'),
        ], heading='Speakers'),
        MultiFieldPanel([
            FieldPanel('location'),
            FieldPanel('lat'),
            FieldPanel('lon'),
        ], heading='Location'),
    ]

class EventPagePosterImage(Orderable):
    page = ParentalKey(EventPage, on_delete=models.CASCADE, related_name='poster_image')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    panels = [
        ImageChooserPanel('image'),
    ]
