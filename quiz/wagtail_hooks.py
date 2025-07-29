from django.urls import re_path
from wagtail_modeladmin.helpers import AdminURLHelper, ButtonHelper
from wagtail_modeladmin.options import ModelAdminGroup, ModelAdmin, modeladmin_register
# from treemodeladmin.options import TreeModelAdmin  # Temporarily disabled for Wagtail 3.0 upgrade
from django.shortcuts import redirect

from .models import Question, QuestionVersion

class QuestionVersionButtonHelper(ButtonHelper):
    def get_buttons_for_obj(self, question_version, **kwargs):
        url_helper = AdminURLHelper(self.model)

        def button(action_url, label, classnames):
            return {
                'url': url_helper.get_action_url(action_url, instance_pk=question_version.id),
                'label': label,
                'title': label,
                'classname': 'button button-small ' + classnames
            }

        buttons = [
            button('edit', 'Edit', 'button-secondary icon icon-edit'),
            button('delete', 'Delete', 'button-danger icon icon-trash'),
        ]

        if not question_version.is_current():
            buttons += [button('approve', 'Publish', 'button-secondary icon icon-view')]

        return buttons


class QuestionVersionAdmin(ModelAdmin):  # Temporarily changed from TreeModelAdmin for Wagtail 3.0 upgrade
    model = QuestionVersion
    menu_label = 'Fragen Versionen'
    menu_icon = 'list-ul'
    # parent_field = 'question'  # TreeModelAdmin specific - temporarily disabled
    list_display = ('id', 'question', 'is_current', 'user', 'created', 'title', 'description')
    search_fields = ('id',)
    ordering = ['-id']
    button_helper_class = QuestionVersionButtonHelper

    def get_admin_urls_for_registration(self):
        urls = super().get_admin_urls_for_registration()

        def gen_url(pattern, view, name=None):
            if not name:
                name = pattern
            return re_path(
                self.url_helper.get_action_url_pattern(pattern),
                view,
                name=self.url_helper.get_action_url_name(name)
            )
        urls = (
            gen_url('approve', self.approve),
        ) + urls

        return urls

    def approve(self, request, instance_pk):
        question_version = self.model.objects.get(pk=instance_pk)
        question_version.approve()

        return redirect(request.META.get('HTTP_REFERER'))

class QuestionAdmin(ModelAdmin):  # Temporarily changed from TreeModelAdmin for Wagtail 3.0 upgrade
    model = Question
    menu_label = 'Fragen Index'
    menu_icon = 'list-ul'
    # child_field = 'questionversion_set'  # TreeModelAdmin specific - temporarily disabled
    # child_model_admin = QuestionVersionAdmin  # TreeModelAdmin specific - temporarily disabled
    list_display = ('id', 'category', 'order', 'user', 'approved', 'created', 'updated')
    search_fields = ('id',)
    list_filter = ('category',)
    ordering = ['category', 'id']

@modeladmin_register
class QuestionMenuAdmin(ModelAdminGroup):
    menu_label = 'MCT'
    menu_icon = 'folder'
    items = (QuestionAdmin, QuestionVersionAdmin)
