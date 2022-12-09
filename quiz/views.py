from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny
from rest_framework import generics, mixins, viewsets

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from wiki.models import Article, URLPath

from pages.models.jurcoach import JurcoachPage
from .models import Question, QuestionVersion, AnswerVersion, Quiz, UserAnswer, Choice
from .serializers import *


def index(request):
    header_image = JurcoachPage.objects.last().header
    # FIXME: remove not used headline + slogan
    header_headline = JurcoachPage.objects.all().last().header_headline
    header_slogan = JurcoachPage.objects.all().last().header_slogan
    return render(request, "quiz/index.html", {
        "categories_at": get_categories("at"),
        "categories_bt": get_categories("bt"),
        "header_image": header_image,
        "header_headline": header_headline,
        "header_slogan": header_slogan
    })

def new_question(request):
    category_id = request.GET.get('category_id')
    category = get_object_or_404(Article, id=category_id)
    return render(request, 'question/new.html', { "user": request.user, "category": category })

def edit_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'question/edit.html', { "user": request.user, "question": question })

def quiz_finish(request, category_id):
    category = get_object_or_404(Article, id=category_id)
    quiz = Quiz.objects.filter(category__id=category.id).filter(user__id=request.user.id).filter(completed=False).first()
    quiz.completed = True
    quiz.save()

    return render(request, 'quiz/finished.html', {'category': category})

# retake quizz redirect (called from profile/quizzes)
def quiz_for_category(request, category_id):
    category = get_object_or_404(Article, id=category_id)
    question = get_questions(URLPath.objects.get(article=category.id)).first()
    return HttpResponseRedirect('/quiz/category/{}/question/{}/?state=start'.format(category.id, question.id))

# FIXME: what is the emeaning of this?
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'core/question.html', {'question': question})

def quiz(request, category_id, question_id):
    category = get_object_or_404(Article, id=category_id)
    question = get_object_or_404(Question, id=question_id)
    questions = get_questions(URLPath.objects.get(article=category.id))

    if request.user.id:
        user = request.user
    else:
        user = User.objects.get(username="anonym")

    if request.method == 'POST':
        # FIXME: anonymous users overwrite their quizes (was hat sich hier jemand gedacht?)
        quiz = Quiz.objects.filter(category__id=category.id).filter(user__id=user.id).filter(completed=False).last()
        user_answer = UserAnswer(
            question=question,
            quiz=quiz,
        )
        user_answer.save()

        for answer in request.POST.getlist('answer'):
            choice = Choice(
                user_answer=user_answer,
                answer=AnswerVersion.objects.get(pk=answer)
            )
            choice.save()

        if request.POST.get('state') == 'finished':
            quiz.completed = True
            quiz.save()

            if request.user.is_anonymous:
                return HttpResponseRedirect('/quiz')
            else:
                return HttpResponseRedirect('/profile/quizzes')
        else:
            next_question = questions.filter(id__gt=question_id).first()
            return HttpResponseRedirect('/quiz/category/{}/question/{}/'.format(category.id, next_question.id))
        #else:
        #    request.session['category'][category_id]['question'][question_id]['answer'][answer_id]
    else:
        # If user starts a new quiz, create quiz object
        if request.GET.get('state') == 'start':
            quiz = Quiz(
                completed=False,
                category=category,
                user=user,
            )
            quiz.save()
            question = questions[0]

        question_version = question.current
        return render(request, 'quiz/show.html', {
            'banner': '/media/original_images/ohnediefrau.png',
            'category': category,
            'question_version': question_version,
            'questions': questions,
            'categories_at': get_categories("at"),
            'categories_bt': get_categories("bt"),
        })


class QuestionCreateOrUpdateSet(mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = QuestionSerializer

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny,]

    def post(self, request, *args, **kwargs):
        data = request.data
        question_id = data.get("question_id")
        user = request.user if request.user.id else None

        if question_id:
            # we have an update to a question
            question = get_object_or_404(Question, pk=question_id)
            message = "New question: %s" % question.category.get_absolute_url()
        else:
            # a new question
            category = get_object_or_404(Article, pk=data.get("categories"))
            question = Question.objects.create(
                user=user,
                category=category,
            )
            message = "Question update: %s" % question.category.get_absolute_url()

        question_version = QuestionVersion.objects.create(
            question=question,
            title=data.get("title"),
            description=data.get("description"),
            user=user,
        )

        for answer in data.get("answers"):
            question_version.answers.create(
                text=answer.get("text"),
                correct=answer.get("correct")
            )

        question_version.save()

        if request.user.is_superuser:
            question_version.approve()
        else:
            Submission.objects.create(content_object=question_version, submitted_by=user, message=message)

        return JsonResponse(data={"success": True}, status=200)

# class QuestionOnlyViewSet(viewsets.ModelViewSet):
#     queryset = Question.objects.all()
#     serializer_class = QuestionOnlySerializer
#     permission_classes = [AllowAny]

class QuestionVersionViewSet(viewsets.ModelViewSet):
    queryset = QuestionVersion.objects.all()
    serializer_class = QuestionVersionSerializer
    permission_classes = [AllowAny]


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = AnswerVersion.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [AllowAny]


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [AllowAny]


class UserAnswerViewSet(viewsets.ModelViewSet):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer
    permission_classes = [AllowAny]


class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [AllowAny]

def get_category_tree(request):
    tree = {
            "id": "cat",
            "label": "Quiz-Teil",
            "children": [
                {
                    "id": "at",
                    "label": "Allgemeiner Teil",
                    "children": [_tree_entry(child) for child in get_categories("at")],
                },
                {
                    "id": "bt",
                    "label": "Besonderer Teil",
                    "children": [_tree_entry(child) for child in get_categories("bt")],
                },
            ]
    }

    return JsonResponse(tree)

def _tree_entry(category):
    return {
        "id": category["category"].article.id,
        "label": category["category"].article.current_revision.title,
    }

def get_questions(cat):
    questions_set = [cat.article.questions.all()] + [sub.article.questions.all() for sub in cat.get_children()]
    ids = []
    for questions in questions_set:
        for question in questions:
            if question.approved and question.current:
                ids.append(question.id)
    return Question.objects.filter(id__in=ids).order_by('id')

def get_categories(slug):
    cat = URLPath.get_by_path(slug)

    categories = []

    for child in cat.get_children():
        questions = get_questions(child)
        if len(questions) == 0:
            continue

        category = {
            "category": child,
            "first": questions[0],
            "questions": [questions],
        }
        categories.append(category)

    categories.sort(key=lambda c: c["category"].path)

    return categories
