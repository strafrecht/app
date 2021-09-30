# Wagtail
from wagtail.core import fields
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
# Local
from .column_blocks import ColumnBlocks

class BasePage(Page):
    class Meta:
        abstract = True

    content = fields.StreamField(ColumnBlocks)
    content_panels = [
        FieldPanel('title'),
        StreamFieldPanel('content')
    ]
