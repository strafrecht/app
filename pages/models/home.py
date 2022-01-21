from django.db import models

# Wagtail
from wagtail.core import blocks, fields
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, FieldRowPanel, MultiFieldPanel

# 3rd Party
from wagtailcolumnblocks.blocks import ColumnsBlock
# Local
from pages.models.news import ArticlePage
from pages.models.sidebar import (
    SidebarTitleBlock,
    SidebarSimpleBlock,
    SidebarBorderBlock,
    SidebarImageTextBlock,
    SidebarCalendarTextBlock,
    SidebarHeaderBlock,
    SidebarPollChooser,
    SidebarSubscribeBlock,
    SidebarEventBlock
)

from wagtail.images.models import Image
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import FieldPanel



    # Content Blocks
class HomeNewsBlock(blocks.StructBlock):
    class Meta:
        template = 'blocks/widgets/news_block.html'

    def get_context(self, *a, **kw):
        ctx = super().get_context(*a, **kw)
        ctx['articles'] = ArticlePage.objects.order_by('-date')[0:4]
        #ctx['articles'] = []#NewsItem.objects.all()[0:4]
        return ctx

class HomeJurcoachBlock(blocks.StructBlock):
    class Meta:
        template = 'blocks/widgets/home_jurcoach.html'
        

class CollapseBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=True)
    content = blocks.RichTextBlock(label="Formatierter Text")
    class Meta:
        icon = 'fa-compress'
        template = 'blocks/sidebar/collapsible.html'
        label = 'Ausklappbares Element'
        
class FlipcardBlock(blocks.StructBlock):
    front = blocks.RichTextBlock(label="Vorderseite")
    back = blocks.RichTextBlock(label="Rückseite")
    class Meta:
        icon = 'fa-graduation-cap'
        template = 'blocks/widgets/flipcard.html'
        label = 'Flipcard'

# Sidebar Blocks
class ContentBlocks(blocks.StreamBlock):
    richtext = blocks.RichTextBlock(label="Formatierter Text")
    collapse_block = CollapseBlock(label="Ausklappbares Element")
    flipcard_block = FlipcardBlock(label="Flipcard")
    home_news_block = HomeNewsBlock(label="Vier letzte News-Beiträge")
    home_jurcoach_block = HomeJurcoachBlock(label="Jurcoach-Startseiten-Widget")

class SidebarBlocks(blocks.StreamBlock):
    sidebar_title = SidebarTitleBlock(label="Grau unterlegte Überschrift")
    sidebar_simple = SidebarSimpleBlock(label="Schlichter Text")
    sidebar_border = SidebarBorderBlock(label="Grau umrandeter Kasten")
    sidebar_image_text = SidebarImageTextBlock(label="Bild links, Text rechts")
    sidebar_header = SidebarHeaderBlock(label="Bild oben, Text darunter")
    sidebar_calendar_text = SidebarCalendarTextBlock(label="Kalender links, Text rechts")
    sidebar_poll = SidebarPollChooser(label="Abstimmung")
    sidebar_subscribe = SidebarSubscribeBlock()
    sidebar_event = SidebarEventBlock()

# Pages
#class ColumnBlocks(blocks.StreamBlock):
#    """
#    All the root level blocks you can use
#    """
#    columns = ColumnsBlock(
#        # Blocks you want to allow within each column
#         Blocks(),
#         # Two columns in admin, first twice as wide as the second
#         ratios=(1, 1),
#         # Used for grouping related fields in the streamfield field picker
#         group="Columns",
#         # 12 column frontend grid (this is the default, so can be omitted)
#         grid_width=12,
#         # Override the frontend template
#         template='blocks/columnsblock.html',
#     )
#
#     def get_context(self, request):
#         context = super().get_context(request)
#         context['request'] = request
#         return contex

class BasePage(Page):
    header = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Graffito-Bild im Header"
    )

    class Meta:
        abstract = True

    #def get_context(self, request):
    #    context = super().get_context(request)
    #    context['request'] = request
    #    return contex

    content = StreamField([
        ('content', ContentBlocks(label="Hauptspalte")),
    ], block_counts={
        'content': {'min_num': 1, 'max_num': 1},
    }, verbose_name="Hauptspalte")

    sidebar = StreamField([
        ('sidebar', SidebarBlocks(required=False, label="Seitenleiste")),
    ], block_counts={
        'sidebar': {'min_num': 0, 'max_num': 1},
    }, verbose_name="Seitenleiste")

    content_panels = [
        FieldPanel('title'),
        ImageChooserPanel('header'),
        FieldRowPanel([
            FieldPanel('content', classname='col8'),
            FieldPanel('sidebar', classname='col4'),
        ], classname='full')
    ]

    template = 'page.html'

class GenericPage(BasePage):
    class Meta:
        verbose_name = "Generische Seite"
        
    def get_context(self, request):
        context = super().get_context(request)
        context['request'] = request
        return context

    content_panels = BasePage.content_panels
    template = BasePage.template


class HomePage(BasePage):
    class Meta:
        verbose_name = "Startseite"
        #abstract = True

    def get_context(self, request):
        context = super().get_context(request)
        context['request'] = request
        #context['block_name'] =
        return context

    content_panels = BasePage.content_panels
    template = BasePage.template
