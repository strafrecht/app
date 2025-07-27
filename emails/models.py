from django.db import models
from birdsong.blocks import DefaultBlocks  # Re-enabled with forked wagtail-birdsong
from birdsong.models import Campaign  # Re-enabled with forked wagtail-birdsong

from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel

# Create your models here.
class NewsletterEmail(Campaign):
    body = StreamField(DefaultBlocks())

    panels = Campaign.panels + [
        FieldPanel('body'),
    ]

# Create your models here.
class LSHNewsletter(Campaign):
    body = StreamField(DefaultBlocks())

    panels = Campaign.panels + [
        FieldPanel('body'),
    ]
