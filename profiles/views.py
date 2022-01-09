from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from core.models import Quiz, Question, QuestionVersion, UserAnswer, AnswerVersion
from wiki.models import ArticleRevision
from .forms import SignupForm

@login_required
def profile(request):
    if request.session.has_key('username'):
        posts = request.session['username']
        query = User.objects.filter(username=posts)
        return render(request, 'profiles/profile.html', {"query":query})
    else:
        return render(request, 'profiles/login.html', {})

@login_required
def index(request):
    quizzes = Quiz.objects.filter(user__id=request.user.id).filter(completed=True)
    return render(request, "profiles/index.html", {
        "banner": "/media/images/login.original.jpg",
        "quizzes": quizzes
    })

@login_required
def flashcards(request):
    return render(request, "profiles/flashcards.html", {"banner": "/media/images/login.original.jpg"})

@login_required
def quizzes(request):
    filter_by = request.GET.get('filter_by', 'all')
    order_by = request.GET.get('order_by', 'created')

    print(filter_by)
    print(order_by)

    query = Quiz.objects.filter(user__id=request.user.id)

    if filter_by == 'completed':
        query = query.filter(completed=True)
    elif filter_by == 'incomplete':
        query = query.filter(completed=False)
    else:
        query = query

    if order_by == 'updated-new':
        query = query.order_by('-updated')
    elif order_by == 'updated-old':
        query = query.order_by('updated')
    elif order_by == 'created-new':
        query = query.order_by('-created')
    elif order_by == 'created-old':
        query = query.order_by('created')
    elif order_by == 'score-high':
        query = query.order_by('created')
    elif order_by == 'score-low':
        query = query.order_by('created')
    else:
        query = query

    #quizzes = Quiz.objects.filter(user__id=request.user.id).order_by('-created')
    quizzes = query.all()
    return render(request, "profiles/quizzes.html", {
        "banner": "/media/images/login.original.jpg",
        "quizzes": quizzes,
        "filter": filter_by,
        "order": order_by
    })

@login_required
def wiki(request):
    revisions = ArticleRevision.objects.filter(user__id=request.user.id)
    return render(request, "profiles/wiki.html", {
        "banner": "/media/images/login.original.jpg",
        "revisions": revisions
    })

@login_required
def quiz_summary(request, id):
    quiz = Quiz.objects.get(pk=id)
    return render(request, "profiles/quiz_summary.html", {
        "banner": "/media/images/login.original.jpg",
        "quiz": quiz
    })

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password =  request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            request.session['username'] = username
            return redirect("profile:index")
    return render(request, 'profiles/login.html', {})

def register(request):
    form = SignupForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        for item in request.POST.items(): print(item)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            return redirect('/')
        else:
            print(form.errors)
    return render(request, 'profiles/register.html', {'form': form})


def logout(request):
    auth_logout(request)
    return render(request, 'profiles/login.html', {})
