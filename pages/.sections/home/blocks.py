# Wagtail
from wagtail.core import blocks

from pages.sections.news.models import ArticlePage

# Local
#from pages.sections.news.base import NewsItem

class HomeNewsBlock(blocks.StructBlock):
    class Meta:
        template = 'blocks/widgets/news_block.html'

    def get_context(self, *a, **kw):
        ctx = super().get_context(*a, **kw)
        ctx['articles'] = ArticlePage.objects.all()[0:4]
        #ctx['articles'] = []#NewsItem.objects.all()[0:4]
        return ctx

class HomeJurcoachBlock(blocks.StructBlock):
    class Meta:
        template = 'blocks/widgets/home_jurcoach.html'