from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from treemodeladmin.options import TreeModelAdmin
from .models import *

@modeladmin_register
class CasetrainingAdmin(ModelAdmin):
    model = Casetraining
    menu_label = 'Falltraining'
    menu_icon = 'list-ul'
    list_display = ('id', 'submission', 'name', 'difficulty', 'approved', 'user', 'created_at', 'updated_at')
    search_fields = ('title', 'id')
    ordering = ['-created_at']
