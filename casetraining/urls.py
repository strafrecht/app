from django.urls import path, include
from rest_framework import routers

from . import views

app_name = "casetraining"

router = routers.DefaultRouter()
router.register(r'case', views.CasetrainingViewSet, basename='case')

urlpatterns = [
    path("", views.index, name="index"),
    path("show/<int:case_id>", views.show, name="show"),
    path("api/", include(router.urls)),
]
