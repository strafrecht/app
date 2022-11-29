from django.shortcuts import render, get_object_or_404

from pages.models.jurcoach import JurcoachPage

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
