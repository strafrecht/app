from django.db import models
from django.contrib.auth.models import User
from itertools import groupby
import datetime

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.core import blocks
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, FieldRowPanel, MultiFieldPanel, InlinePanel, TabbedInterface, ObjectList
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.documents.models import Document
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from wagtailcolumnblocks.blocks import ColumnsBlock
from wagtailautocomplete.edit_handlers import AutocompletePanel

from pages.models.sidebar import (
    SidebarTitleBlock,
    SidebarSimpleBlock,
    SidebarBorderBlock,
    SidebarImageTextBlock,
    SidebarPollChooser,
    SidebarSearchBlock,
)
from django.shortcuts import get_object_or_404, render

# Content Blocks
class ArticleListBlock(blocks.StructBlock):
    class Meta:
        template = 'blocks/widgets/news_list.html'

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        news_article_pages = ArticlePage.objects.filter(live=True, is_evaluation=False).order_by('-date')

        years = []
        keys = []

        for key, group in groupby(news_article_pages, lambda x: x.date.year):
            years.append({"year": key, "articles": list(group)})
            keys.append(key)

        context['groups'] = years
        return context
class EvaluationListBlock(blocks.StructBlock):
    class Meta:
        template = 'blocks/widgets/news_list.html'

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        news_article_pages = ArticlePage.objects.filter(live=True, is_evaluation=True).order_by('-date')

        years = []
        keys = []

        for key, group in groupby(news_article_pages, lambda x: x.date.year):
            years.append({"year": key, "articles": list(group)})
            keys.append(key)

        context['groups'] = years
        return context
# Content Blocks
class ArticlesContentBlocks(blocks.StreamBlock):
    richtext = blocks.RichTextBlock(label="Formatierter Text")
    article_list_block = ArticleListBlock(label="Auflistung aller News-Artikel")
    evaluation_list_block = EvaluationListBlock(label="Auflistung aller Abstimmungsauswertungen")

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        return context
class EvaluationsContentBlocks(blocks.StreamBlock):
    richtext = blocks.RichTextBlock(label="Formatierter Text")
    evaluation_list_block = EvaluationListBlock(label="Auflistung aller Abstimmungsauswertungen")
class NewslettersContentBlocks(blocks.StreamBlock):
    richtext = blocks.RichTextBlock(label="Formatierter Text")
# Sidebar Blocks
class ArticleSidebarBlocks(blocks.StreamBlock):
    sidebar_title = SidebarTitleBlock(label="Grau unterlegte Überschrift")
    sidebar_simple = SidebarSimpleBlock(label="Schlichter Text")
    sidebar_image_text = SidebarImageTextBlock(label="Bild links, Text rechts")
    sidebar_poll = SidebarPollChooser(label="Abstimmung")
    sidebar_search = SidebarSearchBlock(label="Suchfeld")
class NewsletterSidebarBlocks(blocks.StreamBlock):
    sidebar_title = SidebarTitleBlock(label="Grau unterlegte Überschrift")
    sidebar_simple = SidebarSimpleBlock(label="Schlichter Text")
    sidebar_border = SidebarBorderBlock(label="Grau umrandeter Kasten")
    sidebar_poll = SidebarPollChooser(label="Abstimmung")

# Other
class PageTag(TaggedItemBase):
    content_object = ParentalKey(
        Page, related_name='tagged_items', on_delete=models.CASCADE
    )

# Index Pages
class ArticlesPage(RoutablePageMixin, Page):
    class Meta:
        verbose_name="News-Index-Seite"
        verbose_name_plural="News-Index-Seiten"

    content = StreamField([
        ('content', ArticlesContentBlocks(label="Hauptspalte")),
    ], block_counts={
        'content': {'min_num': 1, 'max_num': 1},
    }, verbose_name="Hauptspalte")

    sidebar = StreamField(ArticleSidebarBlocks(required=False), verbose_name="Seitenleiste")

    content_panels = [
        FieldPanel('title'),
        FieldRowPanel([
            FieldPanel('content', classname='col8'),
            FieldPanel('sidebar', classname='col4'),
        ], classname='full')
    ]

    template = 'page.html'

    @route(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/(?P<slug>[\w-]+)/?$')
    def article_by_date(self, request, year, month, day, slug):
        article = get_object_or_404(
            ArticlePage,
            slug=slug
        )
        return article.serve(request)


# Pages
class ArticlePage(Page):
    class Meta:
        verbose_name="News-Artikel"
        verbose_name_plural="News-Artikel"

    allow_comments = models.BooleanField(default=False, verbose_name="Kommentare erlaubt")
    author = models.ForeignKey("People", on_delete=models.SET_NULL, related_name='+', null=True, blank=True, verbose_name="Autor*in")
    date = models.DateField('Datum')
    body = RichTextField(blank=True, verbose_name="Inhalt")
    tags = ClusterTaggableManager(through=PageTag, blank=True)
    is_evaluation = models.BooleanField(default=False, verbose_name="Abstimmungsauswertung")

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.FilterField('is_evaluation'),
    ]
    autocomplete_search_field = 'name'

    #sidebar = StreamField([
    #    ('sidebar', ArticleSidebarBlocks(required=False)),
    #], block_counts={
    #    'sidebar': {'min_num': 0, 'max_num': 1},
    #})
    sidebar = StreamField(ArticleSidebarBlocks(required=False), blank=True, verbose_name="Seitenleiste")

    content_panels = [
        FieldPanel('allow_comments'),
        FieldPanel('author'),
        FieldPanel('date'),
        FieldPanel('is_evaluation'),
        FieldPanel('tags'),
        FieldPanel('title'),
        FieldRowPanel([
            FieldPanel('body', classname='col8'),
            FieldPanel('sidebar', classname='col4'),
        ], classname='full'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname='settings'),
    ])

    @property
    def articles_page(self):
        return self.get_parent().specific

    def get_absolute_url(self):
        return self.get_url()

    def get_context(self, request):
        context = super().get_context(request)
        context['request'] = request
        context['poll'] = False
        for block in self.sidebar.stream_data:
            for child in block['value']:
                print(child)
                if child == 'sidebar_poll':
                    context['poll'] = int(child['value']['poll'])
        return context

    @classmethod
    def get_poll(self):
        print(self.sidebar)

    def author_name(self):
        return "{} {}".format(self.author.first_name, self.author.last_name)

    #def set_url_path(self, parent):
    #    # initially set the attribute self.url_path using the normal operation
    #    super().set_url_path(parent=parent)
    #    self.url_path = self.url_path.replace(
    #        self.slug, '{:%Y/%m/%d/}'.format(self.date_published) + self.slug
    #    )

    parent_page_types = [ArticlesPage]

    content_panels = Page.content_panels + [
        FieldPanel('author'),
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags')
        ], heading="Article information"),
        FieldPanel('body', classname='full'),
    ]

    template = 'pages/news_article_page.html'

class EvaluationsPage(Page):
    class Meta:
        verbose_name="Abstimmungen-Index-Seite"
        verbose_name_plural="Abstimmungen-Index-Seiten"

    def get_context(self, request):
        context = super().get_context(request)
        context['request'] = request
        return context

    content = StreamField([
        ('content', EvaluationsContentBlocks(label="Hauptspalte")),
    ], block_counts={
        'content': {'min_num': 1, 'max_num': 1},
    }, verbose_name="Hauptspalte")

    sidebar = StreamField([
        ('sidebar', ArticleSidebarBlocks(required=False, label="Seitenleiste")),
    ], block_counts={
        'sidebar': {'min_num': 0, 'max_num': 1},
    }, verbose_name="Seitenleiste")

    content_panels = [
        FieldPanel('title'),
        FieldRowPanel([
            FieldPanel('content', classname='col8'),
            FieldPanel('sidebar', classname='col4'),
        ], classname='full')
    ]

class NewslettersPage(Page):
    class Meta:
        verbose_name="Newsletter-Seite"
        verbose_name_plural="Newsletter-Seiten"

    content = StreamField([
        ('content', NewslettersContentBlocks(label="Hauptspalte")),
    ], block_counts={
        'content': {'min_num': 1, 'max_num': 1},
    }, verbose_name="Hauptspalte")

    sidebar = StreamField([
        ('sidebar', NewsletterSidebarBlocks(required=False, label="Seitenleiste")),
    ], block_counts={
        'sidebar': {'min_num': 0, 'max_num': 1},
    }, verbose_name="Seitenleiste")

    content_panels = [
        FieldPanel('title'),
        FieldRowPanel([
            FieldPanel('content', classname='col8'),
            FieldPanel('sidebar', classname='col4'),
        ], classname='full')
    ]

    template = 'pages/base_page.html'

    def get_context(self, request):
        context = super().get_context(request)
        return context

    def get_semester(self, doc):
        date_string = doc.filename.split("Lehrstuhlnewsletter20vom20")[-1].split(".pdf")[0]
        d = datetime.datetime.strptime(date_string, '%d.%m.%Y')

        if d.month in [4, 5, 6, 7, 8, 9]:
            title = "SS-{}".format(d.year)
            return {"title": title, "year": d.year}
        else:
            if d.month in [1, 2, 3]:
                title = "WS-{}".format(d.year - 1)
                return {"title": title, "year": d.year - 1}
            else:
                title = "WS-{}".format(d.year)
                return {"title": title, "year": d.year}
