from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel

##### Website #####
class WebsiteIndexPage(Page):
    intro = RichTextField(blank=True)

    def get_context(self, request):
        context = super().get_context(request)
        websitepages = self.get_children().live().order_by('-first_published_at')
        context['websitepages'] = websitepages
        return context

class WebsitePageTag(TaggedItemBase):
    content_object = ParentalKey(
        'WebsitePage', related_name='tagged_items', on_delete=models.CASCADE
    )

class WebsitePageSidebarPlacement(Orderable, models.Model):
    page = ParentalKey('website.WebsitePage', on_delete=models.CASCADE, related_name='sidebar_placements')
    sidebar = models.ForeignKey('website.Sidebar', on_delete=models.CASCADE, related_name='+')

    class Meta:
        verbose_name = "advert placement"
        verbose_name_plural = "advert placements"
        
    panels = [
        SnippetChooserPanel('sidebar'),
    ]

    def __str__(self):
        return self.page.title + " -> sidebar"

class WebsitePage(Page):
    date = models.DateField('Post date')
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=WebsitePageTag, blank=True)

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags')
        ], heading="Website information"),
        FieldPanel('intro'),
        FieldPanel('body', classname='full'),
        InlinePanel('sidebar_placements', label='Sidebar'),
        InlinePanel('gallery_images', label='Gallery images'),
    ]

class WebsitePageGalleryImage(Orderable):
    page = ParentalKey(WebsitePage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]

@register_snippet
class Sidebar(models.Model):
    name = models.CharField(max_length=100)
    text = RichTextField(blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('text'),
        ImageChooserPanel('image'),
    ]

    def __str__(self):
        return self.name
