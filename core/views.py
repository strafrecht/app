import html2text
import json
import logging
import os
from django.http import HttpResponse
import urllib.parse

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from tqdm import tqdm
from markdownify import markdownify as md
from bs4 import BeautifulSoup
from collections import deque
from time import sleep
from itertools import chain

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.core import serializers
from wagtail.documents.models import Document
from wiki.models import Article, ArticleRevision, URLPath
from core.models import Question, QuestionVersion, AnswerVersion, Quiz, UserAnswer, Choice
from pages.models.exams import Exams
from pages.models.jurcoach import JurcoachPage
from pages.models.sessions import SessionPage
from core.seed import start

from rest_framework import viewsets, permissions, mixins, generics, response
from .serializers import QuestionSerializer, ChoiceSerializer, UserAnswerSerializer, QuizSerializer, AnswerSerializer, \
    QuestionVersionSerializer, QuestionOnlySerializer

logger = logging.getLogger('django')

def transform_to_filename(semester, slug, filename):
    local_filename = '{semester}_{filename}'.format(
        semester=semester,
        slug=slug,
        filename=filename
    )
    return local_filename

def pdf(request, semester, slug, filename):
    #local_filename = transform_to_filename(semester, slug, filename)
    #local_filename = urlencode(filename)
    local_filename = urllib.parse.quote(filename)

    if local_filename:
        print("NEXT")
        print(local_filename)
        document = Document.objects.filter(
            file__endswith=local_filename
        ).first()
        if document.file_extension != 'pdf':
            return  # Empty return results in the existing response
        response = HttpResponse(document.file.read(), content_type='application/pdf')
        print(document.file.name)
        response['Content-Disposition'] = 'filename="' + document.file.name.split('/')[-1] + '"'
        if request.GET.get('download', False) in [True, 'True', 'true']:
            response['Content-Disposition'] = 'attachment; ' + response['Content-Disposition']
        return response
    else:
        return HttpResponseNotFound('<h1>File not found</h1>')

def index(request):
    header_image = JurcoachPage.objects.all().last().header
    header_headline = JurcoachPage.objects.all().last().header_headline
    header_slogan = JurcoachPage.objects.all().last().header_slogan
    return render(request, "core/quiz.html", {
        "categories_at": get_categories("at"),
        "categories_bt": get_categories("bt"),
        "header_image": header_image,
        "header_headline": header_headline,
        "header_slogan": header_slogan
    })

# FIXME: what is the emeaning of this?
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'core/question.html', {'question': question})

# retake quizz redirect (called from profile/quizzes)
def category(request, category_id):
    category = get_object_or_404(Article, id=category_id)
    question = get_questions(URLPath.objects.get(article=category.id)).first()
    return HttpResponseRedirect('/quiz/category/{}/question/{}/?state=start'.format(category.id, question.id))

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

        question_version = question.current()
        return render(request, 'core/category_question.html', {
            'banner': '/media/original_images/ohnediefrau.png',
            'category': category,
            'question_version': question_version,
            'questions': questions,
            'categories_at': get_categories("at"),
            'categories_bt': get_categories("bt"),
        })

# FIXME: what is the emeaning of this?
def category_summary(request, category_id):
    category = get_object_or_404(Article, id=category_id)
    quiz = Quiz.objects.filter(category__id=category.id).filter(user__id=request.user.id).filter(completed=False).first()
    quiz.completed = True
    quiz.save()

    return render(request, 'core/category_summary.html', {'category': category})

def scrape(request):
    return start(request)

def exams(request):
    return render(request, 'pages/exam_table.html', {
        'banner': '/media/original_images/ohnediefrau.png',
    })

def search_wiki(request, query = False):
    from django.contrib.postgres.search import SearchVector, TrigramSimilarity, TrigramDistance
    #articles = Article.objects.annotate(
    #    #similarity=TrigramSimilarity('current_revision__title', query),
    #    distance=TrigramDistance('current_revision__content', query),
    #).filter(distance__gt=0.7).order_by('distance')

    if query:
        results = Article.objects.annotate(
            search=SearchVector(
            #'current_revision__title',
            'current_revision__content',
            ),
        ).filter(search__icontains=query)
    else:
        results = Article.objects.all()

    articles = [{
        'title': article.current_revision.title,
        'url': article.get_absolute_url(),
        'content': article.current_revision.content,
        #'breadcrumb': " / ".join([ancestor.article.current_revision.title for ancestor in article.ancestor_objects()])
    } for article in results if sum(1 for x in article.get_children()) == 0 and article.id != 1]

    # get breadcrumb
    # filter by content

    return JsonResponse({'data': articles})

def api_exams(request):
    exams = Exams.objects.all()

    data = [{
    	'id': exam.id,
    	'type': exam.type,
    	'datetime': exam.date,
    	'difficulty': exam.difficulty,
    	'paragraphs': exam.paragraphs,
    	'problems': exam.problems,
    	'situation': exam.sachverhalt_link,
    	'solution': exam.loesung_link,
    } for exam in exams]

    return JsonResponse({'data': data})

def get_questions(cat):
    questions_set = [cat.article.questions.all()] + [sub.article.questions.all() for sub in cat.get_children()]
    ids = []
    for questions in questions_set:
        for question in questions:
            if question.current():
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

def add_question(request):
    category_id = request.GET.get('category_id')
    category = get_object_or_404(Article, id=category_id)
    return render(request, 'core/add_question.html', { "user": request.user, "category": category })

def edit_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'core/edit_question.html', { "user": request.user, "question": question })

class QuestionViewSet(mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = QuestionSerializer

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny,]

    def post(self, request, *args, **kwargs):
        data = request.data
        question_id = data.get("question_id")

        if question_id:
            # we have an update to a question
            question = get_object_or_404(Question, pk=question_id)
        else:
            # a new question
            category = get_object_or_404(Article, pk=data.get("categories"))

            question = Question.objects.create(
                user=request.user,
                category=category,
            )

        question_version = QuestionVersion.objects.create(
            question=question,
            title=data.get("title"),
            description=data.get("description"),
            user=request.user,
            approved=False,
        )

        for answer in data.get("answers"):
            question_version.answers.create(
                text=answer.get("text"),
                correct=answer.get("correct")
            )

        question_version.save()

        if request.user.is_superuser:
            question_version.approve()

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
        "label": category["category"].article.articlerevision_set.first().title,
    }
