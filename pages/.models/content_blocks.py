# Wagtail
from wagtail.core import blocks, fields
# 3rd Party
from wagtailcolumnblocks.blocks import ColumnsBlock
# Local
from .sidebar import (
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

from pages.sections.home.blocks import HomeJurcoachBlock
from pages.sections.home.blocks import HomeNewsBlock
from pages.sections.news.blocks import NewsListAll
from pages.sections.news.blocks import NewsNewsletterBlock
from pages.sections.events.blocks import EventsListAll

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

    home_news_block = HomeNewsBlock()
    news_list_all = NewsListAll()
    events_list_all = EventsListAll()
    home_jurcoach_block = HomeJurcoachBlock()
    news_newsletter_block = NewsNewsletterBlock()