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
from .models import Question, QuestionVersion, AnswerVersion, Quiz, UserAnswer, Choice
from pages.models.exams import Exams
from pages.models.jurcoach import JurcoachPage
from pages.models.sessions import SessionPage
from .seed import start

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
    categories_at = get_at_categories()
    categories_bt = get_bt_categories()
    header_image = JurcoachPage.objects.all().last().header
    header_headline = JurcoachPage.objects.all().last().header_headline
    header_slogan = JurcoachPage.objects.all().last().header_slogan
    return render(request, "core/quiz.html", {
        "categories_at": categories_at,
        "categories_bt": categories_bt,
        "header_image": header_image,
        "header_headline": header_headline,
        "header_slogan": header_slogan
    })

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'core/question.html', {'question': question})

def category(request, category_id):
    category = get_object_or_404(Article, id=category_id)
    questions = Question.objects.filter(category_id=category_id)
    return render(request, 'core/category.html', {'category': category, 'questions': questions})

def category_question(request, category_id, question_id):
    category = get_object_or_404(Article, id=category_id)

    if request.method == 'POST':
        question_id = request.POST['question-id']

        if request.user:
            question = Question.objects.get(pk=question_id)

            if request.user.id:
                user = User.objects.get(pk=request.user.id)
            else:
                user = User.objects.get(username="anonym")

            quiz = Quiz.objects.filter(category__id=category.id).filter(user__id=user.id).filter(completed=False).last()

            user_answer = UserAnswer(
                question=question,
                quiz=quiz,
            )
            user_answer.save()

            logger.error(request.POST)
            for answer in request.POST.getlist('answer'):
                choice = Choice(
                    user_answer=user_answer,
                    answer=AnswerVersion.objects.get(pk=answer)
                )
                choice.save()

            questions = _get_questions_for_category(category_id)

            next_question = questions.filter(id__gt=question_id).first()

            #return render(request, 'core/category_question.html', {'category': category, 'question': next_question, 'questions': questions})
            if request.POST.get('state') == 'finished':
                quiz.completed = True
                quiz.save()

                return HttpResponseRedirect('/profile/quizzes')
            else:
                return HttpResponseRedirect('/quiz/category/{}/question/{}'.format(category.id, next_question.id))
        else:
            request.session['category'][category_id]['question'][question_id]['answer'][answer_id]
    else:
        category = get_object_or_404(Article, id=category_id)

        id = category_id
        # Get article object
        article_schuld = Article.objects.get(pk=id)
        # Get target article's URLPath
        path_schuld = URLPath.objects.get(article=article_schuld.id)
        # Get URLPath descendants
        schuld_descendants = path_schuld.get_descendants()
        # Get Article IDs
        ids = [path.article.id for path in schuld_descendants]
        # Get questions
        questions = Question.objects.filter(category_id=id) | Question.objects.filter(category_id__in=ids)
        question = Question.objects.get(pk=question_id)
        # user
        if request.user.id:
            user = User.objects.get(pk=request.user.id)
        else:
            user = User.objects.get(username="anonym")

        # If user starts a new quiz, create quiz object
        if request.GET.get('state') == 'start':
            quiz = Quiz(
                completed=False,
                category=category,
                user=user,
            )
            quiz.save()

            question = questions.first()

        #question_version = QuestionVersion.objects.first()
        question_version = question.questions.all().first()

        question = question_version

        categories_at = get_at_categories()
        categories_bt = get_bt_categories()

        return render(request, 'core/category_question.html', {
            'banner': '/media/original_images/ohnediefrau.png',
            'category': category,
            'question': question,
            'questions': questions,
            'categories_at': get_at_categories(),
            'categories_bt': get_bt_categories(),
            #'categories': get_bt_categories() if '/bt' in category.get_absolute_url() else get_at_categories()
        })

def category_summary(request, category_id):
    category = get_object_or_404(Article, id=category_id)
    user_id = request.user.id
    quiz = Quiz.objects.filter(category__id=category.id).filter(user__id=user_id).filter(completed=False).first()
    quiz.completed = True
    quiz.save()

    return render(request, 'core/category_summary.html', {'category': category})

def _get_questions_for_category(category_id):
    id = category_id
    # Get article object
    article_schuld = Article.objects.get(pk=id)
    # Get target article's URLPath
    path_schuld = URLPath.objects.get(article=article_schuld.id)
    # Get URLPath descendants
    schuld_descendants = path_schuld.get_descendants()
    # Get Article IDs
    ids = [path.article.id for path in schuld_descendants]
    # Get questions
    questions = Question.objects.filter(category_id=id) | Question.objects.filter(category_id__in=ids)
    return questions.order_by('id')


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

def get_first_at(cat):
    categories = [child for child in cat.get_descendants()]
    question_set = [sub.article.question_set.all() for sub in categories if len(sub.article.question_set.all()) > 0]
    pre = [[q for q in question] for question in question_set]
    result = list(chain.from_iterable(pre))
    if len(result) > 0:
        return result[0]
    else:
        Question.objects.first()

def get_first_bt(cat):
    cur_question_set = cat.article.question_set.all()
    question_set = [sub.article.question_set.all() for sub in cat.get_descendants() if len(sub.article.question_set.all()) > 0]

    pre = [[q for q in question] for question in question_set]
    result = list(chain.from_iterable(pre)) + [question for question in list(cur_question_set)]

    if len(result) > 0:
        return result[0]
    else:
        #print("YYY")
        Question.objects.first()

def get_at_categories():
    at = URLPath.objects.filter(slug='at').last()
    grundlagen = URLPath.objects.filter(slug='grundlagen').first()

    categories = [
        {"category": child,
        "first": get_first_at(child),
        "questions": [
            [
                question for question in sub.article.question_set.all() if len(sub.article.question_set.all()) > 1
            ] for sub in child.get_descendants() if len(child.get_descendants()) > 0
        ]} for child in at.get_children()]

    categories.insert(0, {
        "category": grundlagen,
        "first": grundlagen.article.question_set.first(),
        "questions": [
            question for question in grundlagen.article.question_set.all() if len(grundlagen.article.question_set.all()) > 1
        ]
    })

    return categories

def get_bt_categories():
    bt = URLPath.objects.filter(slug='bt').last()

    categories = [
        {"category": child,
        "first": get_first_bt(child),
        "questions": [
            [
            question for question in child.article.question_set.all() if len(child.article.question_set.all()) > 0
        ]
    ]} for child in bt.get_children()]

    categories.sort(key=lambda c: c["category"].path)

    return categories


# @login_required(login_url="/profile/login")
def add_question(request):
    user = request.user
    return render(request, 'core/add_question.html', {"user": user})


class QuestionViewSet(mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = QuestionSerializer

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny,]

    def post(self, request, *args, **kwargs):
        data = request.data
        categories = Article.objects.filter(id__in=data.get("categories"))

        if request.user.is_authenticated:
            question = Question(user=request.user)
        else:
            question = Question()
        question.save()

        question_version = QuestionVersion.objects.create(
            question=question,
            title=data.get("title"),
            description=data.get("description")
        )

        question_version.categories.set(categories)
        question_version.save()

        for answer in data.get("answers"):
            AnswerVersion.objects.create(
                question_version=question_version,
                text=answer.get("text"),
                correct=answer.get("correct")
            )

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
    root = URLPath.objects.first()
    tree = create_categories(root)
    return JsonResponse(tree)

def create_categories(category):
    return {
        "id": category.article.id,
        "label": category.article.articlerevision_set.first().title,
        "children": [create_categories(child) for child in category.get_children() if len(category.get_children()) > 0]
    }
