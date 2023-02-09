from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.http import HttpResponse

from wiki.models import ArticleRevision
from wiki.models.article import Article

from core.models import Submission
from quiz.models import Quiz, UserAnswer
from .forms import SignupForm
from .models import Bookmark

@login_required
def index(request):
    return render(request, "profiles/index.html", {
        "banner": "/media/images/login.original.jpg",
        "profile": request.user.profile
    })

@login_required
def bookmarks(request):
    return render(request, "profiles/bookmarks.html", {
        "banner": "/media/images/login.original.jpg",
        "bookmarks": request.user.bookmarks.order_by('-created').all()
    })

@login_required
def bookmarks_create(request, article_id):
    article = Article.objects.get(id=article_id)
    bookmark = request.user.bookmarks.filter(content_id=article.id,
                                             content_type=ContentType.objects.get_for_model(Article).id).first()
    if not bookmark:
        bookmark = request.user.bookmarks.create(content_object=article)
    return HttpResponse(201)

@login_required
def bookmarks_delete(request, article_id):
    bookmark = request.user.bookmarks.filter(content_id=article_id,
                                             content_type=ContentType.objects.get_for_model(Article).id).first().delete()
    return HttpResponse(200)

@login_required
def flashcards(request):
    return render(request, "profiles/flashcards.html", {"banner": "/media/images/login.original.jpg"})

@login_required
def quizzes(request):
    filter_by = request.GET.get('filter_by', 'all')
    order_by = request.GET.get('order_by', 'created-new')

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
    # FIXME: order by score is not implemented
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
        "order": order_by,
    })

@login_required
def submissions(request):
    submissions = Submission.objects.filter(
        submitted_by_id=request.user.id,
    ).order_by('-created')
    return render(request, "profiles/submissions.html", {
        "banner": "/media/images/login.original.jpg",
        "submissions": submissions
    })

@login_required
def quiz_summary(request, id):
    quiz = Quiz.objects.get(pk=id)

    quiz_summary = []

    user_answers = UserAnswer.objects.filter(quiz=quiz)

    for user_answer in user_answers:
        # FIXME: this does not work as the users answers are not saved
        # for choice in get_choices(user_answer):
        for choice in user_answer.choice_set.all():
            title = choice.answer.question_version.title
            ans_val = choice.answer
            found_val = [dictionary for dictionary in quiz_summary if dictionary["question"] == title]
            rep_index = next((index for (index, dictionary) in enumerate(quiz_summary) if dictionary["question"] == title), None)
            if len(found_val):
                #The list is not empty
                ans_list = quiz_summary[rep_index]["answer"]
                ans_list.append(ans_val)
                ans_list = list(dict.fromkeys(ans_list))
                quiz_summary[rep_index] = dict(
                    question=title,
                    answer=ans_list
                )

            else:
                quiz_summary.append(
                    dict(
                        question=title,
                        answer=[ans_val]
                    )
                )

    return render(request, "profiles/quiz_summary.html", {
        "banner": "/media/images/login.original.jpg",
        "quiz": quiz,
        "quiz_summary": quiz_summary
    })

def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, "Registrierung erfolgreich.")
            return redirect("/")
        messages.error(request, "Registrierung nicht erfolgreich. Bitte die Angaben korrigieren.")
    else:
        form = SignupForm()
    return render(request, 'profiles/register.html', {'form': form})

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.info(request, f"Du bist jetzt als {username} angemeldet.")
                # create user profile if missing
                if not user.profile:
                    Profile.objects.create(user=user)
                if request.GET.get("next", None):
                    return redirect(request.GET["next"])
                return redirect("profile:index")
            messages.error(request,"Falscher Benutzername oder Passwort.")
    else:
        form = AuthenticationForm()
    return render(request=request, template_name="profiles/login.html", context={"login_form":form})

def logout(request):
    auth_logout(request)
    messages.success(request, "Erfolgreich abgemeldet.")
    return redirect("/")
