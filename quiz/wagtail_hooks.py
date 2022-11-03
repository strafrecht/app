from wagtail.contrib.modeladmin.options import ModelAdminGroup, modeladmin_register
from treemodeladmin.options import TreeModelAdmin

from .models import Question, QuestionVersion

class QuestionVersionAdmin(TreeModelAdmin):
    menu_label = 'Fragen Version'
    menu_icon = 'list-ul'
    model = QuestionVersion
    parent_field = 'question'
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
