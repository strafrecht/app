from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse

from wiki.models import Article, URLPath

from .models import Casetraining

def index(request):
    return render(request, "casetraining/index.html", {
        'banner': '/media/original_images/ohnediefrau.png',
        "advanced": Casetraining.objects.filter(difficulty="advanced"),
        "beginner": Casetraining.objects.filter(difficulty="beginner"),
        "shortcase": Casetraining.objects.filter(difficulty="shortcase"),
    })

def new(request):
    return render(request, "casetraining/new.html", {
        'banner': '/media/original_images/ohnediefrau.png',
    })

def show(request, case_id):
    case = get_object_or_404(Casetraining, pk=case_id)
    return render(request, "casetraining/show.html", {
        'banner': '/media/original_images/ohnediefrau.png',
        "case": case,
    })

def wiki_categories(request):

    articles = filter(lambda x: x.other_read, Article.objects.all())

    return JsonResponse(list(map(_wiki_article, articles)), safe=False)

def _wiki_article(article):
    return {
        "id": article.id,
        "title": article.current_revision.title,
        "url": article.get_absolute_url(),
    }
