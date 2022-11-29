from django.urls import path, include
from rest_framework import routers

from . import views

app_name = "quiz"

router = routers.DefaultRouter()
router.register(r'question-versions', views.QuestionVersionViewSet)
router.register(r'answers', views.AnswerViewSet)
router.register(r'quizzes', views.QuizViewSet)
router.register(r'user-answers', views.UserAnswerViewSet)
router.register(r'choices', views.ChoiceViewSet)

urlpatterns = [
    # show quiz index
    path('', views.index, name='index'),
    # show quiz
    path('category/<int:category_id>/question/<int:question_id>/', views.quiz, name='show'),
    # redirect to quiz for given category
    path('category/<int:category_id>/', views.quiz_for_category, name='for_category'),
    # finish quiz
    path('category/<int:category_id>/finish/', views.quiz_finish, name='finish'),
    # create new question
    path('new_question/', views.new_question, name='new_question'),
    # edit question
    path('edit_question/<int:question_id>/', views.edit_question, name='edit_question'),
    # POST question
    path('create_question/', views.QuestionCreateOrUpdateSet.as_view(), name='post_question'),

    # FIXME: what is the emeaning of this?
    path('question/<int:question_id>/', views.detail, name='detail'),
    # Get tree for dropdown in add_question
    path('api/category_tree/', views.get_category_tree, name='get_category_tree'),
    path('api/json/', include(router.urls)),
]
