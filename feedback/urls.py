from django.urls import path, include
from . import views

app_name = 'feedback'

urlpatterns = [
    path('', views.index, name='index'),
    path('form/', views.form, name='form'),
    path('save/', views.save, name='save'),
    path('<int:suggestion_id>/<slug:slug>/', views.detail, name='detail'),
    path('<int:suggestion_id>/<slug:slug>/vote', views.vote, name='vote'),

    path('widget', views.widget_index, name='widget_index'),
    path('widget/form/', views.widget_form, name='widget_form'),
    path('widget/save/', views.widget_save, name='widget_save'),
    path('widget/<int:suggestion_id>/<slug:slug>/', views.widget_detail, name='widget_detail'),
    path('widget/<int:suggestion_id>/<slug:slug>/vote', views.widget_vote, name='widget_vote'),
]
