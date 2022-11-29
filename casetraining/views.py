from django.shortcuts import render

from pages.models.jurcoach import JurcoachPage

from .models import Casetraining

def index(request):
    header_image = JurcoachPage.objects.last().header
    return render(request, "casetraining/index.html", {
        "header_image": header_image,
        "advanced": Casetraining.objects.filter(difficulty="advanced"),
        "beginner": Casetraining.objects.filter(difficulty="beginner"),
        "shortcase": Casetraining.objects.filter(difficulty="shortcase"),
    })
