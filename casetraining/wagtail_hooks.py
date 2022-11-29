from wagtail.contrib.modeladmin.options import ModelAdminGroup, modeladmin_register
from treemodeladmin.options import TreeModelAdmin
from .models import Casetraining

class CasetrainingAdmin(TreeModelAdmin):
    model = Casetraining
    menu_label = 'Fälle'
    menu_icon = 'list-ul'

@modeladmin_register
class CasetrainingMenuAdmin(ModelAdminGroup):
    menu_label = 'Falltraining'
    menu_icon = 'folder'
    items = (CasetrainingAdmin,)
