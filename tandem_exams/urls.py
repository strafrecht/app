from django.urls import path

from . import views

app_name = "tandem_exams"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:id>/", views.show, name="show"),
    path("<int:id>/new/", views.new_solution, name="new_solution"),
    path("<int:id>/new_correction/", views.new_correction, name="new_correction"),
]
