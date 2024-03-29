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
    path('bookmarks/', views.bookmarks, name='bookmarks'),
    path('bookmarks/create/<article_id>', views.bookmarks_create, name='bookmarks_create'),
    path('bookmarks/delete/<article_id>', views.bookmarks_delete, name='bookmarks_delete'),
    path('submissions/', views.submissions, name='submissions'),
    path('tandemklausuren/', views.tandem_exams, name='tandem_exams'),
]
