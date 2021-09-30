from django.urls import path, include
from . import views

app_name = 'feedback'

urlpatterns = [
    path('', views.index, name='index'),
    path('form/', views.form, name='form'),
    path('save/', views.save, name='save'),
    path('<int:suggestion_id>/<slug:slug>/', views.detail, name='detail'),
    path('<int:suggestion_id>/<slug:slug>/vote', views.vote, name='vote'),
]
