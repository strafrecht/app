from django.db import models
from birdsong.blocks import DefaultBlocks
from birdsong.models import Campaign
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.fields import StreamField

# Create your models here.
class NewsletterEmail(Campaign):
    body = StreamField(DefaultBlocks())

    panels = Campaign.panels + [
        StreamFieldPanel('body'),
    ]

# Create your models here.
class LSHNewsletter(Campaign):
    body = StreamField(DefaultBlocks())

    panels = Campaign.panels + [
        StreamFieldPanel('body'),
    ]
