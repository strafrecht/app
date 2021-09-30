from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register
from wagtail.core import hooks

from .models import Question, QuestionVersion

from django.templatetags.static import static
from django.utils.html import format_html
from django.http import HttpResponse

from wagtail.core import hooks

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


class QuestionAdmin(ModelAdmin):
    model = Question
    menu_label = 'Fragen'
    menu_icon = 'folder'
    list_display = ('id', 'user')


class QuestionVersionAdmin(ModelAdmin):
    model = QuestionVersion
    menu_label = 'Fragen Versionen'
    menu_icon = 'folder'
    list_display = ('question', 'title', 'description', 'categories', 'approved', 'answers')


class MCTAdmin(ModelAdminGroup):
    menu_label = 'MCT'
    menu_icon = 'folder'
    items = (QuestionAdmin, QuestionVersionAdmin)


modeladmin_register(MCTAdmin)