from django import forms
from wiki.editors.base import BaseEditor

class ModernWidget(forms.Widget):
    template_name = 'wiki/forms/modern.html'

    def __init__(self, attrs=None):
        default_attrs = {
            'class': 'modern',
            'rows': '10',
            'cols': '40',
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

class ModernAdminWidget(ModernWidget):
    template_name = 'wiki/forms/modern-admin.html'

class Modern(BaseEditor):
    editor_id = 'modern'

    def get_admin_widget(self, instance=None):
        return ModernAdminWidget()

    def get_widget(self, instance=None):
        return ModernWidget()

    class AdminMedia:
        css = {
            'all': (
            )
        }
        js = (
        )

    class Media:
        css = {
            'all': (
            )
        }
        js = (
        )
