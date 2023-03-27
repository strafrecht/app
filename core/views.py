import html2text
import json
import logging
import os
import urllib.parse

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core import serializers
from wagtail.documents.models import Document
from wiki.models import Article

from pages.models.exams import Exams
from core.seed import start

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
    	'situation': exam.sachverhalt_dl and exam.sachverhalt_dl.url or exam.sachverhalt_link,
    	'solution': exam.loesung_dl and exam.loesung_dl.url or exam.loesung_link,
    } for exam in exams]

    return JsonResponse({'data': data})

# newsletter subscription

from django.core.mail import send_mail
from django.urls import reverse
from django.utils.crypto import get_random_string, salted_hmac
from django.conf import settings
from birdsong.models import Contact

def newsletter_subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            hashed_email = salted_hmac(settings.SECRET_KEY, email.lower()).hexdigest()
            confirmation_url = request.build_absolute_uri(reverse('newsletter_confirm', args=[hashed_email, email]))
            text = """
Bitte Bestätigen Sie ihre Anmeldung zum LSH-Newsletter über folgenden Link:
{confirmation_url}

Falls Sie die Anmeldung zum Newsletter nicht angefordert haben,
können Sie diese E-Mail ignorieren.

Dein Jurcoach-Team
            """.format(confirmation_url=confirmation_url)
            send_mail(
                'Bestätigung der Anmeldung zum LSH-Newsletter',
                text,
                settings.BIRDSONG_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            messages.success(request, f"Wir senden Dir eine Bestätigungs-E-Mail für die Anmeldung zu.")
        else:
            messages.info(request, f"E-Mail-Adresse fehlt.")
    else:
        return HttpResponseBadRequest('Only POST requests allowed.')

    return redirect("/archiv/lsh-newsletter/")


def newsletter_confirm(request, hashed_email, email):
    computed_hash = salted_hmac(settings.SECRET_KEY, email.lower()).hexdigest()
    if hashed_email == computed_hash:
        Contact.objects.create(email=email)
        messages.success(request, f"Du wurdest für den LSH-Newsletter eingetragen.")
    else:
        messages.error(request, f"Der Bestätigungslink ist nicht korrekt.")

    return redirect("/archiv/lsh-newsletter/")
