# https://github.com/wagtail/wagtail/issues/2893

from django.forms.utils import pretty_name
from django.utils.html import format_html
from wagtail.admin.panels import Panel


class ReadOnlyPanel(Panel):
    def __init__(self, attr, *args, **kwargs):
        self.attr = attr
        super().__init__(*args, **kwargs)

    def clone(self):
        return self.__class__(
            attr=self.attr,
            heading=self.heading,
            classname=self.classname,
            help_text=self.help_text,
        )

    class BoundPanel(Panel.BoundPanel):
        def __init__(self, panel, instance, request, form, prefix):
            super().__init__(panel, instance, request, form, prefix)
            self.attr = panel.attr

        def render_html(self, parent_context=None):
            value = getattr(self.instance, self.attr)
            if callable(value):
                value = value()

            label = self.heading or self.attr.replace('_', ' ').title()
            help_text = getattr(self.panel, 'help_text', '')

            html = format_html(
                '<div class="w-field">'
                '<label class="w-field__label">{}</label>'
                '<div class="w-field__input">'
                '<div class="w-field__readonly" style="padding: 8px 12px; background-color: #f5f5f5; border: 1px solid #ddd; border-radius: 4px; color: #666;">'
                '{}'
                '</div>'
                '</div>'
                '{}'
                '</div>',
                label,
                value or '—',
                format_html('<div class="w-field__help"><div class="help">{}</div></div>', help_text) if help_text else ''
            )

            return html
