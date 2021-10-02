from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.images.models import Image
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import FieldPanel
from wagtailmodelchooser.blocks import ModelChooserBlock
from wagtailmodelchooser.edit_handlers import ModelChooserPanel
from wagtailpolls.models import Poll


class PollChooser():
    poll = ModelChooserPanel('wagtailpolls.Poll')

    class Meta:
        template = 'blocks/sidebar/poll.html'

    def get_context(self, value, parent_context=None):
        ctx = super().get_context(value, parent_context=parent_context)
        ctx['page'] = {'poll': Poll.objects.get(id=1)}
        return ctx

class JurcoachPage(Page):
    body = RichTextField(blank=True)
    header = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        ImageChooserPanel('header'),
        PollChooser()
    ]
    
