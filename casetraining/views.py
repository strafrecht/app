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

def show(request, case_id):
    case = get_object_or_404(Casetraining, pk=case_id)
    return render(request, "casetraining/show.html", {
        'banner': '/media/original_images/ohnediefrau.png',
        "case": case,
    })

def wiki_categories(request):
    return JsonResponse(_wiki_articles(request, URLPath.root()))

def _wiki_articles(request, node):
    if not node.article.other_read:
        return None

    return {
        "id": node.article.id,
        "title": node.article.current_revision.title,
        "url": reverse('wiki:root') + node.path,
        "children": [_wiki_articles(request, child) for child in node.article.get_children(user_can_read=request.user, articles__article__current_revision__deleted=False)]
    }
