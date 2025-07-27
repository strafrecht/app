from wagtail import blocks, fields
from wagtail.images.blocks import ImageChooserBlock
from colorfield.widgets import ColorWidget  # Replacement for wagtail_color_panel
# from wagtailmodelchooser.blocks import ModelChooserBlock  # Temporarily disabled for Wagtail 3.0 upgrade
# from wagtailmodelchooser.edit_handlers import ModelChooserPanel  # Temporarily disabled for Wagtail 3.0 upgrade
# from wagtailpolls.models import Poll  # Temporarily disabled for Django 5.x compatibility

# Custom color block using django-colorfield widget
class ColorBlock(blocks.CharBlock):
    def __init__(self, **kwargs):
        self.widget = ColorWidget()
        super().__init__(**kwargs)

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
    color = ColorBlock(default="#333d44")  # Replaced wagtail_color_panel with django-colorfield
    image = ImageChooserBlock()
    content = blocks.RichTextBlock(required=False)

    class Meta:
        template = 'blocks/sidebar/header.html'

class SidebarPollChooser(blocks.StructBlock):
    # poll = ModelChooserBlock('wagtailpolls.Poll')  # Temporarily disabled for Wagtail 3.0 upgrade
    poll = blocks.CharBlock(help_text="Poll ID (temporary replacement)")  # Temporary replacement

    class Meta:
        template = 'blocks/sidebar/poll.html'

    def get_context(self, value, parent_context=None):
        ctx = super().get_context(value, parent_context=parent_context)
        # Temporary implementation for Wagtail 3.0 upgrade
        try:
            # Handle different types of poll values after Wagtail 3.0 upgrade
            if isinstance(value['poll'], str):
                poll_id = int(value['poll'])
            elif isinstance(value['poll'], int):
                poll_id = value['poll']
            else:
                # Assume it's a model instance with an id attribute
                poll_id = value['poll'].id
            # ctx['page'] = {'poll': Poll.objects.get(id=poll_id)}  # Temporarily disabled for Django 5.x compatibility
            ctx['page'] = {'poll': None}  # Temporary fallback
        except (ValueError, AttributeError):  # Poll.DoesNotExist temporarily removed
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
