from django.shortcuts import render

from pages.models.jurcoach import JurcoachPage

def index(request):
    header_image = JurcoachPage.objects.last().header
    return render(request, "casetraining/index.html", {
        "header_image": header_image,
    })
