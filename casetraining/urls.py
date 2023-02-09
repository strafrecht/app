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

    def get_user_name(self, obj):
        return str(obj.user)

    class Meta:
        model = Casetraining
        fields = "__all__"

class UserCasetrainingSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    def get_user_name(self, obj):
        return str(obj.user)

    def get_user(self):
        return self.fields["user"].get_default()

    def save(self, **kwargs):
        # users can't update approved cases
        if self.instance and self.instance.approved:
            raise Exception("not allowed (case is approved)")

        # users can't update submitted cases
        if self.instance and self.instance.submission:
            raise Exception("not allowed (case is submitted)")

        if not self.get_user().is_anonymous:
            kwargs["user"] = self.get_user()

        return super().save(**kwargs)

    class Meta:
        model = Casetraining
        fields = "__all__"
        read_only_fields = ('approved', 'submission',)

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
        obj.save()
        user = None
        if not request.user.is_anonymous:
            user = request.user
        url = "/falltraining/show/%s/" % str(obj.id)
        obj.submission = Submission.objects.create(
            content_object=obj,
            submitted_by=user,
            message="Fall eingereicht",
            url=url,
        )
        obj.save()
        return Response({'submission': obj.submission.id})


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'case', CasetrainingViewSet, basename='case')

urlpatterns = [
    path("", views.index, name="index"),
    path("new/", views.new, name="new"),
    path("show/<int:case_id>/", views.show, name="show"),
    path('api/wiki_categories', views.wiki_categories, name='wiki_categories'),
    path('api/free_text_mail/<int:id>/', views.free_text_mail, name='free_text_mail'),
    path("api/", include(router.urls)),
]
