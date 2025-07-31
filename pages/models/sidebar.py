from wagtail import blocks, fields
from wagtail.images.blocks import ImageChooserBlock
from wagtail_color_panel.blocks import NativeColorBlock  # Re-enabled for Wagtail 6.x - Native color picker
from wagtailmodelchooser.blocks import ModelChooserBlock  # Re-enabled for Wagtail 6.x - Model choosers
from wagtailpolls.models import Poll  # Re-enabled for Wagtail 6.x - Poll model for chooser

# Legacy ColorBlock for migration compatibility
class ColorBlock(NativeColorBlock):
    """Legacy ColorBlock for migration compatibility - maps to NativeColorBlock"""
    pass

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
    color = NativeColorBlock(default="#333d44")  # Re-enabled wagtail-color-panel for native color picker
    image = ImageChooserBlock()
    content = blocks.RichTextBlock(required=False)

    class Meta:
        template = 'blocks/sidebar/header.html'

class SidebarPollChooser(blocks.StructBlock):
    poll = ModelChooserBlock('wagtailpolls.Poll')  # Re-enabled for Wagtail 6.x - Model chooser for polls

    class Meta:
        template = 'blocks/sidebar/poll.html'

    def get_context(self, value, parent_context=None):
        ctx = super().get_context(value, parent_context=parent_context)
        # Re-enabled poll functionality for Wagtail 6.x
        try:
            # Handle different types of poll values after Wagtail upgrade
            if isinstance(value['poll'], str):
                poll_id = int(value['poll'])
            elif isinstance(value['poll'], int):
                poll_id = value['poll']
            else:
                # Assume it's a model instance with an id attribute
                poll_id = value['poll'].id
            ctx['page'] = {'poll': Poll.objects.get(id=poll_id)}
        except (ValueError, AttributeError, Poll.DoesNotExist):
            ctx['page'] = {'poll': None}
        return ctx

class SidebarSubscribeBlock(blocks.StructBlock):
    class Meta:
        template = 'blocks/sidebar/subscribe.html'

class SidebarEventBlock(blocks.StructBlock):
    class Meta:
        template = 'blocks/sidebar/event.html'

class SidebarSearchBlock(blocks.StructBlock):
    class Meta:
        template = 'blocks/sidebar/search.html'
