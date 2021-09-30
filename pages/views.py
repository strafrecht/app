import json

from django.contrib.auth.models import User 
from django.http import JsonResponse
from django.shortcuts import render
#from pages.models import Node, Exams
from wagtail.core.models import Page
from wagtail.search.models import Query
from pages.models.news import ArticlePage
from pages.models.sessions import SessionPage

#def categories(request):
#    root = Node.objects.first()
#    categories = root.get_descendants()
#    serialized = [{'id': c.pk, 'name': c.name, 'text': c.name} for c in categories]
#    data = json.dumps(serialized)
#    return JsonResponse(data)

def search(request):
    # Search
    query = request.GET.get('query', None)
    results = []

    if query:
        results.append({'name': 'News', 'items': ArticlePage.objects.live().filter(is_evaluation=False).search(query)})
        results.append({'name': 'Abstimmungen', 'items': ArticlePage.objects.live().filter(is_evaluation=True).search(query)})
        #results.append({'name': 'Lehre', 'items': SessionPage.objects.live().search(query)})

        # Log the query so Wagtail can suggest promoted results
        Query.get(query).add_hit()
    else:
        results = Page.objects.none()

    # Render template
    return render(request, 'pages/search_results.html', {
        'query': query,
        'results': results,
    })
