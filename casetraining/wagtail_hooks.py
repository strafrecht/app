from wagtail.contrib.modeladmin.options import ModelAdminGroup, modeladmin_register
from treemodeladmin.options import TreeModelAdmin
from .models import *

class CasetrainingAdmin(TreeModelAdmin):
    model = Casetraining
    menu_label = 'Fälle'
    menu_icon = 'list-ul'

class CaseStepProblemAreaAdmin(TreeModelAdmin):
    model = CaseStepProblemArea
    menu_label = 'CaseStepProblemArea'
    menu_icon = 'list-ul'

@modeladmin_register
class CasetrainingMenuAdmin(ModelAdminGroup):
    menu_label = 'Falltraining'
    menu_icon = 'folder'
    items = (CasetrainingAdmin, CaseStepProblemAreaAdmin)

# FIXME: move to django admin ...
# https://schinckel.net/2016/04/30/multi-table-inheritance-and-the-django-admin/
