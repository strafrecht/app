from django.urls import path
from . import views

app_name = 'profile'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('flashcards/', views.flashcards, name='flashcards'),
    path('quizzes/', views.quizzes, name='quizzes'),
    path('quiz/<id>', views.quiz_summary, name='quiz_summary'),
    path('wiki/', views.wiki, name='wiki'),
]
