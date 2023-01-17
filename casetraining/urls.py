from django.db.models import Q
from django.urls import path, include
from rest_framework import routers, viewsets, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
import json

from . import views
from .models import *

app_name = "casetraining"

class AdminCasetrainingSerializer(serializers.ModelSerializer):
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

class UserCasetrainingSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    def get_steps(self, obj):
        if not obj.steps or obj.steps == "":
            return None

        return json.loads(obj.steps)

    def get_user_name(self, obj):
        return str(obj.user)

    def get_user(self):
        return self.fields["user"].get_default()

    def save(self, **kwargs):
        print(self)
        print(kwargs)
        print("self.validated_data")
        print(self.validated_data)
        print("self.instance")
        print(self.instance)
        # users can't update approved cases
        if self.instance and self.instance.approved:
            raise Exception("not allowed (case is approved)")

        # users can't update submitted cases
        if self.instance and self.instance.submission:
            raise Exception("not allowed (case is submitted)")

        if not self.get_user().is_anonymous:
            kwargs["user"] = self.get_user()
        #
        result = super().save(**kwargs)
        print(result.name)
        return result

    class Meta:
        model = Casetraining
        fields = "__all__"
        read_only_fields =  ('approved', 'submission')

# FIXME: security
class CasetrainingViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.request.user.is_staff:
            return AdminCasetrainingSerializer
        return UserCasetrainingSerializer

    def get_queryset(self):
        # staff has access to all cases
        if self.request.user.is_staff:
            return Casetraining.objects.all()
        # users have access to own cases and all approved cases
        # anonymous users can access all other anonymous users cases
        return Casetraining.objects.filter(Q(user=self.request.user.id) | Q(approved=True))

    @action(detail=True, methods=['put'])
    def submit(self, request, pk=None):
        obj = self.get_object()
        if obj.submission:
            return Response({'submission': obj.submission.id})

        user = None
        if not request.user.is_anonymous:
            user = request.user
        obj.submission = Submission.objects.create(content_object=obj, submitted_by=user, message="Fall eingereicht")
        obj.save()
        return Response({'submission': obj.submission.id})


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'case', CasetrainingViewSet, basename='case')

urlpatterns = [
    path("", views.index, name="index"),
    path("new/", views.new, name="new"),
    path("show/<int:case_id>/", views.show, name="show"),
    path('api/wiki_categories', views.wiki_categories, name='wiki_categories'),
    path("api/", include(router.urls)),
]
