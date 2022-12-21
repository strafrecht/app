from django.urls import path, include
from rest_framework import routers, viewsets, serializers
import json

from . import views
from .models import *

app_name = "casetraining"

class CasetrainingSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField(read_only=True)
    #steps = serializers.SerializerMethodField(read_only=False)

    def get_steps(self, obj):

        if not obj.steps or obj.steps == "":
            return None

        return json.loads(obj.steps)

    def get_user_name(self, obj):
        return str(obj.user)

    class Meta:
        model = Casetraining
        fields = "__all__"

# FIXME: security
class CasetrainingViewSet(viewsets.ModelViewSet):
    serializer_class = CasetrainingSerializer

    def get_queryset(self):
        return Casetraining.objects.all()

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'case', CasetrainingViewSet, basename='case')

urlpatterns = [
    path("", views.index, name="index"),
    path("new/", views.new, name="new"),
    path("show/<int:case_id>/", views.show, name="show"),
    path('api/wiki_categories', views.wiki_categories, name='wiki_categories'),
    path("api/", include(router.urls)),
]
