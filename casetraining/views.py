from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.cache import cache_page
from django.core.cache import cache
import hashlib

from wiki.models import Article, ArticleRevision, URLPath

from .models import Casetraining

def index(request):
    casetrainings = Casetraining.objects.order_by('name')
    if not request.user.is_staff:
        casetrainings = casetrainings.filter(approved=True)

    return render(request, "casetraining/index.html", {
        'banner': '/media/original_images/ohnediefrau.png',
        "advanced":  casetrainings.filter(difficulty="advanced"),
        "beginner":  casetrainings.filter(difficulty="beginner"),
        "shortcase": casetrainings.filter(difficulty="shortcase"),
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
    modified = Article.objects.order_by('-modified').first().modified
    hash = hashlib.md5(str(modified).encode('utf-8')).hexdigest()
    result = cache.get_or_set("wiki_categories", _wiki_categories_list, timeout=(60 * 60), version=hash)
    return JsonResponse(result, safe=False)

def _wiki_categories_list():
    articles = filter(lambda x: x.other_read, Article.objects.all())
    return list(map(_wiki_article, articles))

def _wiki_article(article):
    return {
        "id": article.id,
        "title": article.current_revision.title,
        "url": article.get_absolute_url(),
    }
