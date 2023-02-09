from wagtail.contrib.modeladmin.options import ModelAdminGroup, ModelAdmin, modeladmin_register
from .models import *

class TandemExamAdmin(ModelAdmin):
    model = TandemExam
    menu_label = 'Klausuren'
    menu_icon = 'list-ul'
    list_display = ('id', 'name', 'difficulty', 'approved', 'created_at', 'updated_at')
    search_fields = ('name', 'id')
    ordering = ['-created_at']

class ExamSolutionAdmin(ModelAdmin):
    model = ExamSolution
    menu_label = 'Lösungen'
    menu_icon = 'list-ul'
    list_display = ('id', 'exam', 'state', 'user', 'correction_by', 'created_at', 'updated_at')
    list_filter = ('state',)
    search_fields = ('exam', 'id')
    ordering = ['-created_at']

@modeladmin_register
class TandemExamMenuAdmin(ModelAdminGroup):
    menu_label = 'Tandemklausuren'
    menu_icon = 'folder'
    items = (TandemExamAdmin, ExamSolutionAdmin)
