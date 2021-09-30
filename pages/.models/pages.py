from django.db import models
from django.shortcuts import render
from django.contrib.auth.models import User

from itertools import groupby
import datetime

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable
from wagtail.documents.models import Document
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, TabbedInterface, ObjectList
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from wagtail.core import blocks, fields
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail_color_panel.fields import ColorField
from wagtail_color_panel.edit_handlers import NativeColorPanel
from wagtail_color_panel.blocks import NativeColorBlock

from wagtailcolumnblocks.blocks import ColumnsBlock

from wagtailpolls.models import Poll
from wagtailpolls.edit_handlers import PollChooserPanel
#from news.models import NewsItem

from pages.models.sidebar import (
    SidebarTitleBlock,
    SidebarSimpleBlock,
    SidebarBorderBlock,
    SidebarImageTextBlock,
    SidebarCalendarTextBlock,
    SidebarHeaderBlock,
    SidebarPollBlock,
    SidebarSubscribeBlock,
    SidebarEventBlock
)
# Sidebar
class ContentBlocks(blocks.StreamBlock):
    """
    The blocks you want to allow within each ColumnBlocks column.
    """

    text = blocks.RichTextBlock()

    sidebar_title = SidebarTitleBlock()
    sidebar_simple = SidebarSimpleBlock()
    sidebar_border = SidebarBorderBlock()
    sidebar_image_text = SidebarImageTextBlock()
    sidebar_calendar_text = SidebarCalendarTextBlock()
    sidebar_header = SidebarHeaderBlock()
    sidebar_poll = SidebarPollBlock()
    sidebar_subscribe = SidebarSubscribeBlock()
    sidebar_event = SidebarEventBlock()

# Content
class ColumnBlocks(blocks.StreamBlock):
    """
    All the root level blocks you can use
    """
    column_2_1 = ColumnsBlock(
        # Blocks you want to allow within each column
        ContentBlocks(),
        # Two columns in admin, first twice as wide as the second
        ratios=(2, 1),
        # Used for grouping related fields in the streamfield field picker
        group="Columns",
        # 12 column frontend grid (this is the default, so can be omitted)
        grid_width=12,
        # Override the frontend template
        template='blocks/columnsblock.html',
    )

    def get_context(self, request):
        context = super().get_context(request)
        context['request'] = request
        return contex

class BasePage(Page):
    class Meta:
        abstract = True

    content = fields.StreamField(ColumnBlocks)
    content_panels = [
        FieldPanel('title'),
        StreamFieldPanel('content')
    ]

class BasePage(Page):
    class Meta:
        abstract = True

    content = fields.StreamField(ColumnBlocks)
    content_panels = [
        FieldPanel('title'),
        StreamFieldPanel('content')
    ]