from django.urls import path, include
from rest_framework import routers, viewsets, serializers
import json

from . import views
from .models import *

app_name = "casetraining"

class CaseStepProblemAreaSerializer(serializers.ModelSerializer):

    class Meta:
        model = CaseStepProblemArea
        fields = ["article", "weight"]

class CaseStepSerializer(serializers.ModelSerializer):
    config = serializers.SerializerMethodField(read_only=True)

    def get_config(self, obj):
        if (obj.step_type == "problem_areas"):
            return CaseStepProblemAreaSerializer(obj.problem_areas.all(), many=True).data

        if obj.config == "":
            return None

        return json.loads(obj.config)

    class Meta:
        model = CaseStep
        fields = ["step_type", "config"]

class CasetrainingSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField(read_only=True)
    steps = serializers.SerializerMethodField(read_only=True)

    def get_user_name(self, obj):
        return str(obj.user)

    def get_steps(self, obj):
        return CaseStepSerializer(obj.steps.order_by('position').all(), many=True).data

    class Meta:
        model = Casetraining
        fields = "__all__"

# FIXME: security
class CasetrainingViewSet(viewsets.ModelViewSet):
    serializer_class = CasetrainingSerializer

    def get_queryset(self):
        return Casetraining.objects.all()

router = routers.DefaultRouter()
router.register(r'case', CasetrainingViewSet, basename='case')

urlpatterns = [
    path("", views.index, name="index"),
    path("new/", views.new, name="new"),
    path("show/<int:case_id>/", views.show, name="show"),
    path('api/wiki_categories', views.wiki_categories, name='wiki_categories'),
    path("api/", include(router.urls)),
]
