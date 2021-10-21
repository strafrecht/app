from django.db import models

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.images.models import Image
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtailmodelchooser.edit_handlers import ModelChooserPanel
from modelcluster.fields import ParentalKey
from wagtailpolls.models import Poll

class JurcoachFooter(Orderable):
    page = ParentalKey('pages.JurcoachPage', related_name='jurcoachfooter')
    footeritem_headline = models.CharField('Überschrift', max_length=200, null=True, blank=True)
    footeritem_text = RichTextField(null=True, blank=True, verbose_name='Text')
    footeritem_linktext = models.CharField('Verlinkter Text', max_length=200, null=True, blank=True)
    footeritem_linkurl = models.CharField('Link', max_length=200, null=True, blank=True)

    panels = [FieldPanel('footeritem_headline', classname="col-12"),
             FieldPanel('footeritem_text', classname="col-12"),
             FieldPanel('footeritem_linktext', classname="col-12"),
             FieldPanel('footeritem_linkurl', classname="col-12"),]

class JurcoachCarousel(Orderable):
    page = ParentalKey('pages.JurcoachPage', related_name='jurcoachcarousel')
    illustration_choices = [
        ('falltraining', 'Falltraining'),
        ('wiki', 'Problemfeld-Wiki'),
        ('mct', 'Multiple-Choice-Test'),
        ('klausurdatenbank', 'Klausurdatenbank'),
        ('rechtsprechung', 'Höchstrichterliche Rechtsprechung'),
    ]
    illustration = models.CharField(
        'Auswahl der Illustration',
        choices=illustration_choices,
        max_length=255,
        blank=True
    )
    carousel_description = RichTextField(null=True, blank=True, verbose_name='Text')
    carousel_link_text = models.CharField('Verlinkter Text', max_length=200, null=True, blank=True)
    carousel_link_url = models.CharField('Link', max_length=250, null=True, blank=True)

    panels = [FieldPanel('illustration', classname="col-12"),
             FieldPanel('carousel_description', classname="col-12"),
             FieldPanel('carousel_link_text', classname="col-12"),
             FieldPanel('carousel_link_url', classname="col-12"),]
    
class JurcoachPage(Page):
    body = RichTextField(blank=True)
    header = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Graffito-Bild im Header'
    )
    header_headline = RichTextField(blank=True, verbose_name='Mit Graffito unterlegte Überschrift')
    header_slogan = RichTextField(blank=True, verbose_name='Mit Graffito unterlegter Untertitel')
    intro_headline = models.CharField('Intro-Überschrift', max_length=200, null=True, blank=True)
    intro_text = RichTextField(blank=True, verbose_name='Intro-Text')
    carousel_headline = models.CharField('Slider-Überschrift', max_length=200, null=True, blank=True)
    contribution_headline = models.CharField('Mitmachfunktionen-Überschrift', max_length=200, null=True, blank=True)
    contribution_description = RichTextField(null=True, blank=True, verbose_name='Mitmachfunktionen-Beschreibung')
    
    poll = models.ForeignKey(
        Poll,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    def get_context(self, request):
        context = super().get_context(request)
        context['poll'] = self
        return context
    
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [ImageChooserPanel('header'),
            FieldPanel('header_headline', classname="col-12"),
            FieldPanel('header_slogan', classname="col-12")],
            heading='Header',
        ),
        MultiFieldPanel(
            [FieldPanel('intro_headline', classname="col-12"),
            FieldPanel('intro_text', classname="col-12")],
            heading='Intro',
        ),
        MultiFieldPanel(
            [FieldPanel('carousel_headline', classname="col-12"),
            InlinePanel('jurcoachcarousel', max_num=10, min_num=0, label='Slide')],
            heading='Slider',
        ),
        MultiFieldPanel(
            [FieldPanel('contribution_headline', classname="col-12"),
            FieldPanel('contribution_description', classname="col-12")],
            heading='Mitmachfunktionen',
        ),
        MultiFieldPanel(
            [InlinePanel('jurcoachfooter', max_num=3, min_num=0, label='Footer Column'),
             ModelChooserPanel('poll')],
            heading='Footer',
        ),
    ]
    
