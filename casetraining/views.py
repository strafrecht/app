from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.cache import cache_page
import hashlib
import json

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

def free_text_mail(request, id):
    case = get_object_or_404(Casetraining, pk=id)
    data = json.loads(request.body)
    email = data.get('email')
    config = data.get('config')
    answers = data.get('answers')

    # return if no answers given
    if len(answers) == 0: return HttpResponse(201)

    subject = "Korrektur-Anfrage: {title}".format(title=str(case))
    text = """
    Falltraining:
    {site}/falltraining/show/{id}

    Absender: {email}

    """.format(site=settings.SITE_URL,
               id=id,
               email=email)
    for index, question in enumerate(config, start=0):
        if len(answers) < index + 1: break

        text += """
        {question}

        {answer}
        """.format(index=index + 1,
                   question=question.get("text"),
                   answer=answers[index])

    send_mail(
        subject=subject,
        message=text,
        from_email='jukol@strafrecht-online.de',
        recipient_list=['jukol@strafrecht-online.de'],
        fail_silently=False,
    )
    return HttpResponse(201)

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
