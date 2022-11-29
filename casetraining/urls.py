from django.urls import path, include
from . import views

app_name = "casetraining"

urlpatterns = [
    path("", views.index, name='index'),
    path('show/<int:case_id>', views.show, name='show'),
]
