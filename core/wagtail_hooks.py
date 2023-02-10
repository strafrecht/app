from wagtail.contrib.modeladmin.helpers import AdminURLHelper, ButtonHelper
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.core import hooks
from wiki.models import ArticleRevision

from django.templatetags.static import static
from django.utils.html import format_html

from .models import Submission, Profile

#@hooks.register('before_serve_document')
#def serve_pdf(document, request):
#    if document.file_extension != 'pdf':
#        print("HERE")
#        return  # Empty return results in the existing response
#    print("HERE")
#    response = HttpResponse(document.file.read(), content_type='application/pdf')
#    print(document.file.name)
#    response['Content-Disposition'] = 'filename="' + document.file.name.split('/')[-1] + '"'
#    if request.GET.get('download', False) in [True, 'True', 'true']:
#        response['Content-Disposition'] = 'attachment; ' + response['Content-Disposition']
#  return response

@hooks.register("insert_global_admin_css", order=100)
def global_admin_css():
    """Add /static/css/custom.css to the admin."""
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static("css/wagtail.css")
    )

class SubmissionButtonHelper(ButtonHelper):
    def get_buttons_for_obj(self, obj, **kwargs):
        url_helper = AdminURLHelper(self.model)

        def button(action_url, label, classnames):
            return {
                'url': action_url,
                'label': label,
                'title': label,
                'classname': 'button button-small ' + classnames
            }

        buttons = [
            button(url_helper.get_action_url("edit", instance_pk=obj.id),
                   'Edit', 'button-secondary icon icon-edit'),
            button(url_helper.get_action_url("delete", instance_pk=obj.id),
                   'Delete', 'button-danger icon icon-trash'),
            button(obj.url
                   , 'View', 'button-secondary icon icon-view')
        ]
        return buttons


@modeladmin_register
class SubmissionAdmin(ModelAdmin):
    menu_label = 'Einreichungen'
    menu_order = 201
    model = Submission
    list_display = ('submitted_by', 'reviewed_by', 'content_type', 'content_object', 'message', 'status', 'created', 'updated',)
    list_filter = ('status',)
    ordering = ['-created']
    button_helper_class = SubmissionButtonHelper

@modeladmin_register
class ProfileAdmin(ModelAdmin):
    menu_label = 'Profile'
    menu_order = 200
    menu_icon = "user"
    model = Profile
    list_display = ["user", "rewards"]
    ordering = ["rewards"]

@modeladmin_register
class ArticleAdmin(ModelAdmin):
    model = ArticleRevision
    menu_label = "Wiki Articles"
    menu_icon = "placeholder"
    menu_order = 290
    # add_to_settings_menu = False
    # exclude_from_explorer = False
    list_display = ('id', 'revision_number', 'title', 'user', 'user_message', 'created', 'modified')
    # search_fields = ("email", "full_name",)
    search_fields = ('title', 'id')
    ordering = ['-created']
