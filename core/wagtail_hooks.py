from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register
from wagtail.core import hooks
from wiki.models import Article, ArticleRevision

from django.templatetags.static import static
from django.utils.html import format_html
from django.http import HttpResponse

from wagtail.core import hooks
from treemodeladmin.options import TreeModelAdmin

from .models import Question, QuestionVersion, Submission

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

@modeladmin_register
class SubmissionAdmin(ModelAdmin):
    menu_label = 'Einreichungen'
    model = Submission
    list_display = ('submitted_by', 'reviewed_by', 'article_revision', 'message', 'status', 'created', 'updated',)
    list_filter = ('status',)
    ordering = ['-created']

class QuestionVersionAdmin(TreeModelAdmin):
    menu_label = 'Fragen Version'
    menu_icon = 'list-ul'
    model = QuestionVersion
    parent_field = 'question'
    child_field = 'submission_set'
    child_model_admin = SubmissionAdmin
    list_display = ('question', 'title', 'description', 'categories', 'approved', 'user')

class QuestionAdmin(TreeModelAdmin):
    menu_label = 'Fragen Index'
    menu_icon = 'list-ul'
    model = Question
    child_field = 'questionversion_set'
    child_model_admin = QuestionVersionAdmin
    list_display = ('filepath', 'slug')

@modeladmin_register
class QuestionMenuAdmin(ModelAdminGroup):
    menu_label = 'Fragen'
    menu_icon = 'folder'
    items = (QuestionAdmin, QuestionVersionAdmin)

@modeladmin_register
class ArticleAdmin(ModelAdmin):
    model = ArticleRevision
    menu_label = "Wiki Articles"
    menu_icon = "placeholder"
    # menu_order = 290
    # add_to_settings_menu = False
    # exclude_from_explorer = False
    list_display = ('id', 'revision_number', 'title', 'user', 'user_message', 'created', 'modified')
    # search_fields = ("email", "full_name",)
    search_fields = ('title', 'id')
    ordering = ['-created']
