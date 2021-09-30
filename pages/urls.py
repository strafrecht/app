from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path, include
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.search, name='search'),
]

