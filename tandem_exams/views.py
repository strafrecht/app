from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404

from .models import *
from .forms import ExamSolutionForm, ExamCorrectionForm
import profiles.views as profiles

def index(request):
    exams = TandemExam.objects.order_by('name').filter(approved=True)

    return render(request, "tandem_exams/index.html", {
        'banner': '/media/original_images/ohnediefrau.png',
        "advanced":  exams.filter(difficulty="advanced"),
        "beginner":  exams.filter(difficulty="beginner"),
    })

def show(request, id):
    exam = get_object_or_404(TandemExam, pk=id, approved=True)
    solutions = []
    form = None
    if not request.user.is_anonymous:
        solutions = request.user.exam_solutions.filter(exam=exam)
        if solutions.count() == 0:
            form = ExamSolutionForm()

    return render(request, "tandem_exams/show.html", {
        'banner': '/media/original_images/ohnediefrau.png',
        "exam": exam,
        "form": form,
        "solutions": solutions,
    })

@login_required
def new_solution(request, id):
    exam = get_object_or_404(TandemExam, pk=id, approved=True)
    if request.method == 'POST':
        form = ExamSolutionForm(request.POST, request.FILES)
        if form.is_valid():
            instance = ExamSolution(exam=exam,
                                    user=request.user)
            # we have to save it first and assign the file later,
            # so the object has a pk
            instance.save()
            instance.file = request.FILES['file']
            instance.save()
            if instance.find_tandem_partner():
                messages.success(request, "Gutachten erfolgreich hochgeladen. Ein anderes Gutachten wurde Dir zur Korrektur zugewiesen. Du findest das Gutachten in deinem Profil.")
            else:
                messages.success(request, "Gutachten erfolgreich hochgeladen. Wir schicken eine Nachricht, sobald ein:e Tandempartner:in gefunden wurde.")
            return redirect("tandem_exams:show", id=exam.id)
    else:
        form = ExamSolutionForm()
    return render(request, "tandem_exams/show.html", {
        'banner': '/media/original_images/ohnediefrau.png',
        "exam": exam,
        "form": form,
    })

@login_required
def new_correction(request, id):
    solution = get_object_or_404(ExamSolution, pk=id,
                                 correction_by=request.user,
                                 state="ACCEPTED")
    form = ExamCorrectionForm(request.POST, request.FILES)
    if form.is_valid():
        solution.upload_correction(
            request.FILES['correction'],
        )
        messages.success(request, "Korrektur erfolgreich hochgeladen.")
        return redirect("profile:tandem_exams")
    return profiles.tandem_exams(request, id, form)
