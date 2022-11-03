from django.urls import path, include
from . import views
from rest_framework import routers

urlpatterns = [
    path('scrape/', views.scrape, name='scrape'),
    path('exams/', views.exams, name='exams'),
    path('search/wiki/', views.search_wiki, name='search_wiki'),
    path('search/wiki/<str:query>', views.search_wiki, name='search_wiki'),

    path('api/exams', views.api_exams, name='api_exams'),
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('<str:semester>/<str:slug>/<str:filename>', views.pdf, name='pdf'),
]
