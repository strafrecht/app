from wagtail.core import blocks, fields
from wagtail.images.blocks import ImageChooserBlock
from wagtail_color_panel.blocks import NativeColorBlock
from wagtailmodelchooser.blocks import ModelChooserBlock
from wagtailmodelchooser.edit_handlers import ModelChooserPanel
from wagtailpolls.models import Poll

class SidebarTitleBlock(blocks.StructBlock):
    content = blocks.RichTextBlock()

    class Meta:
        template = 'blocks/sidebar/title.html'

class SidebarSimpleBlock(blocks.StructBlock):
    content = blocks.RichTextBlock()

    class Meta:
        template = 'blocks/sidebar/simple.html'

class SidebarBorderBlock(blocks.StructBlock):
    content = blocks.RichTextBlock()

    class Meta:
        template = 'blocks/sidebar/border.html'

class SidebarImageTextBlock(blocks.StructBlock):
    content = blocks.RichTextBlock()
    image = ImageChooserBlock()

    class Meta:
        template = 'blocks/sidebar/image_text.html'

class SidebarCalendarTextBlock(blocks.StructBlock):
    content = blocks.RichTextBlock()
    calendar = blocks.DateBlock(format="%Y-%m-%d")

    class Meta:
        template = 'blocks/sidebar/calendar_text.html'

class SidebarHeaderBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    color = NativeColorBlock('color', default="#333d44")
    image = ImageChooserBlock()
    content = blocks.RichTextBlock(required=False)

    class Meta:
        template = 'blocks/sidebar/header.html'

class SidebarPollChooser(blocks.StructBlock):
    poll = ModelChooserBlock('wagtailpolls.Poll')

    class Meta:
        template = 'blocks/sidebar/poll.html'

    def get_context(self, value, parent_context=None):
        ctx = super().get_context(value, parent_context=parent_context)
        ctx['page'] = {'poll': Poll.objects.get(id=1)}
        return ctx

class SidebarSubscribeBlock(blocks.StructBlock):
    class Meta:
        template = 'blocks/sidebar/subscribe.html'

class SidebarEventBlock(blocks.StructBlock):
    class Meta:
        template = 'blocks/sidebar/event.html'
