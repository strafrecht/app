from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register
from wagtail.core import hooks
from wiki.models import Article, ArticleRevision

from .models import Question, QuestionVersion, Submission

from django.templatetags.static import static
from django.utils.html import format_html
from django.http import HttpResponse

from wagtail.core import hooks
from treemodeladmin.options import TreeModelAdmin

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


# class QuestionAdmin(ModelAdmin):
#     model = Question
#     menu_label = 'Fragen'
#     menu_icon = 'folder'
#     list_display = ('id', 'user')


# class QuestionVersionAdmin(ModelAdmin):
#     model = QuestionVersion
#     menu_label = 'Fragen Versionen'
#     menu_icon = 'folder'
#     list_display = ('question', 'title', 'description', 'categories', 'approved', 'answers')


# class MCTAdmin(ModelAdminGroup):
#     menu_label = 'MCT'
#     menu_icon = 'folder'
#     items = (QuestionAdmin, QuestionVersionAdmin)


# @modeladmin_register
class SubmissionAdmin(TreeModelAdmin):
    menu_label = 'Einreichungen'
    model = Submission
    parent_field = 'question_version'
    list_display = ('submitted_by', 'reviewed_by', 'article_revision', 'question_version', 'status', 'message')


# @modeladmin_register
class QuestionVersionAdmin(TreeModelAdmin):
    menu_label = 'Fragen Version'
    menu_icon = 'list-ul'
    model = QuestionVersion
    parent_field = 'question'
    child_field = 'submission_set'
    child_model_admin = SubmissionAdmin
    list_display = ('question', 'title', 'description', 'categories', 'approved', 'user')


# @modeladmin_register
class QuestionAdmin(TreeModelAdmin):
    menu_label = 'Fragen Index'
    menu_icon = 'list-ul'
    model = Question
    child_field = 'questionversion_set'
    child_model_admin = QuestionVersionAdmin
    list_display = ('filepath', 'slug')


class QuestionMenuAdmin(ModelAdminGroup):
    menu_label = 'Fragen'
    menu_icon = 'folder'
    items = (QuestionAdmin, QuestionVersionAdmin)


class ArticleAdmin(ModelAdmin):
    model = ArticleRevision
    menu_label = "Wiki Articles"
    menu_icon = "placeholder"
    # menu_order = 290
    # add_to_settings_menu = False
    # exclude_from_explorer = False
    list_display = ('created', 'modified')
    # search_fields = ("email", "full_name",)


modeladmin_register(SubmissionAdmin)
modeladmin_register(QuestionMenuAdmin)
modeladmin_register(ArticleAdmin)


# modeladmin_register(MCTAdmin)