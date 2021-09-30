from django.db import models

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField

from wagtailnews.models import NewsIndexMixin, AbstractNewsItem, AbstractNewsItemRevision
from wagtailnews.decorators import newsindex
#from pages.models.base import BasePage

# The decorator registers this model as a news index
@newsindex
class NewsIndex(NewsIndexMixin, Page):
    # Add extra fields here, as in a normal Wagtail Page class, if required
    newsitem_model = 'NewsItem'

class NewsItem(AbstractNewsItem):
    # NewsItem is a normal Django model, *not* a Wagtail Page.
    # Add any fields required for your page.
    # It already has ``date`` field, and a link to its parent ``NewsIndex`` Page
    title = models.CharField(max_length=255)
    body = RichTextField()

    panels = [
        FieldPanel('title', classname='full title'),
        FieldPanel('body', classname='full'),
    ] + AbstractNewsItem.panels

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return self.url()


class NewsItemRevision(AbstractNewsItemRevision):
        newsitem = models.ForeignKey(NewsItem, related_name='revisions', on_delete=models.CASCADE)