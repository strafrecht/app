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

from pages.models.sidebar import (
    SidebarTitleBlock,
    SidebarImageTextBlock,
)

# Content Blocks
class ArticleListBlock(blocks.StructBlock):
    class Meta:
        template = 'blocks/widgets/news_list.html'

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        news_article_pages = ArticlePage.objects.filter(live=True).order_by('-date')

        years = []
        keys = []

        for key, group in groupby(news_article_pages, lambda x: x.date.year):
            years.append({"year": key, "articles": list(group)})
            keys.append(key)

        context['groups'] = years
        return context
class EvaluationListBlock(blocks.StructBlock):
    def get_context(self, request):
        context = super().get_context(request)
        news_evaluation_pages = NewsArticlePage.objects.filter(live=True).order_by('-date')

        years = []
        keys = []

        for key, group in groupby(news_evaluation_pages, lambda x: x.date.year):
            years.append({"year": key, "articles": list(group)})
            keys.append(key)

        context['groups'] = years
        return context
class NewsNewsletterBlock(blocks.StructBlock):
    class Meta:
        template = 'blocks/widgets/news_newsletter.html'

    def get_context(self, *a, **kw):
        context = super().get_context(*a, **kw)
        newsletters = Document.objects.filter(tags__name='newsletter')
        semesters = []
        keys = []

        for key, group in groupby(newsletters, get_semester):
            semesters.append({"semester": key["title"], "year": key["year"], "newsletters": list(group)})

        semesters = sorted(semesters, key=lambda x: x['year'], reverse=True)
        context['semesters'] = semesters
        return context


    def get_semester(doc):
        date_string = doc.filename.split("Lehrstuhlnewsletter20vom20")[-1].split(".pdf")[0]
        d = datetime.datetime.strptime(date_string, '%d.%m.%Y')

        if d.month in [4, 5, 6, 7, 8, 9]:
            title = "SS {}".format(d.year)
            return {"title": title, "year": d.year}
        else:
            if d.month in [1, 2, 3]:
                title = "WS {}".format(d.year - 1)
                return {"title": title, "year": d.year - 1}
            else:
                title = "WS {}".format(d.year)
                return {"title": title, "year": d.year}

# Sidebar Blocks
class ArticlesContentBlocks(blocks.StreamBlock):
    richtext = blocks.RichTextBlock()
    article_list_block = ArticleListBlock()

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        return context
class EvaluationsContentBlocks(blocks.StreamBlock):
    richtext = blocks.RichTextBlock()
    evaluation_list_block = EvaluationListBlock()
class SidebarBlocks(blocks.StreamBlock):
    sidebar_title = SidebarTitleBlock()
    sidebar_image_text = SidebarImageTextBlock()

# Pages
class ArticlesPage(Page):

    content = StreamField([
        ('content', ArticlesContentBlocks()),
    ], block_counts={
        'content': {'min_num': 1, 'max_num': 1},
    })

    sidebar = StreamField([
        ('sidebar', SidebarBlocks(required=False)),
    ], block_counts={
        'sidebar': {'min_num': 0, 'max_num': 1},
    })

    content_panels = [
        FieldPanel('title'),
        FieldRowPanel([
            FieldPanel('content', classname='col8'),
            FieldPanel('sidebar', classname='col4'),
        ], classname='full')
    ]

    template = 'page.html'


class EvaluationsPage(Page):
    def get_context(self, request):
        context = super().get_context(request)
        context['request'] = request
        return context

    content = StreamField([
        ('content', EvaluationsContentBlocks()),
    ], block_counts={
        'content': {'min_num': 1, 'max_num': 1},
    })

    sidebar = StreamField([
        ('sidebar', SidebarBlocks(required=False)),
    ], block_counts={
        'sidebar': {'min_num': 0, 'max_num': 1},
    })

    content_panels = [
        FieldPanel('title'),
        FieldRowPanel([
            FieldPanel('content', classname='col8'),
            FieldPanel('sidebar', classname='col4'),
        ], classname='full')
    ]

    template = 'page.html'
    
class PageTag(TaggedItemBase):
    content_object = ParentalKey(
        Page, related_name='tagged_items', on_delete=models.CASCADE
    )

class ArticlePage(Page):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='+', null=True, blank=True)
    date = models.DateField('Post date')
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=PageTag, blank=True)
    is_evaluation = models.BooleanField(default=False)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    sidebar = StreamField([
        ('sidebar', SidebarBlocks(required=False)),
    ], block_counts={
        'sidebar': {'min_num': 0, 'max_num': 1},
    })

    content_panels = [
        FieldRowPanel([
            FieldRowPanel([
                FieldPanel('title', classname='full'),
                FieldPanel('body', classname='full'),
                MultiFieldPanel([
                    FieldPanel('date', classname='col6'),
                    FieldPanel('tags', classname='col6')
                ]),
            ], classname='d-flex flex-column col8'),
            FieldRowPanel([
                FieldPanel('sidebar', classname='full'),
            ], classname='d-flex flex-column col4')
        ], classname='article-edit-form full'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname='settings'),
    ])

    def get_absolute_url(self):
        return self.get_url()

    def get_context(self, request):
        context = super().get_context(request)
        context['request'] = request
        return context

    def author_name(self):
        return "{} {}".format(self.author.first_name, self.author.last_name)

    content_panels = Page.content_panels + [
        FieldPanel('author'),
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags')
        ], heading="Article information"),
        FieldPanel('body', classname='full'),
    ]

class NewsNewsletterPage(Page):
    def get_context(self, request):
        context = super().get_context(request)
        newsletters = Document.objects.filter(tags__name='newsletter')
        semesters = []
        keys = []

        for key, group in groupby(newsletters, get_semester):
            semesters.append({"semester": key["title"], "year": key["year"], "newsletters": list(group)})

        semesters = sorted(semesters, key=lambda x: x['year'], reverse=True)
        context['semesters'] = semesters
        return context

    def get_semester(doc):
            date_string = doc.filename.split("Lehrstuhlnewsletter20vom20")[-1].split(".pdf")[0]
            d = datetime.datetime.strptime(date_string, '%d.%m.%Y')

            if d.month in [4,5,6,7,8,9]:
                title = "SS-{}".format(d.year)
                return {"title": title, "year": d.year}
            else:
                if d.month in [1,2,3]:
                    title = "WS-{}".format(d.year-1)
                    return {"title": title, "year": d.year-1}
                else:
                    title = "WS-{}".format(d.year)
                    return {"title": title, "year": d.year}

