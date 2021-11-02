from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import redirect
from core.models import Quiz, Question, UserAnswer, Choice
from wiki.models import ArticleRevision
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    quizzes = Quiz.objects.filter(user__id=request.user.id).filter(completed=True)
    return render(request, "profiles/index.html", {"quizzes": quizzes})

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
        "quizzes": quizzes,
        "filter": filter_by,
        "order": order_by
    })

def wiki(request):
    revisions = ArticleRevision.objects.filter(user__id=request.user.id)
    return render(request, "profiles/wiki.html", {"revisions": revisions})

def quiz_summary(request, id):
    quiz = Quiz.objects.get(pk=id)
    quiz_summary = []

    user_answers = UserAnswer.objects.filter(quiz=quiz)

    for user_answer in user_answers:
        # print(get_choices(user_answer))
        for choice in get_choices(user_answer):
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

    return render(request, "profiles/quiz_summary.html", {"quiz": quiz, "quiz_summary": quiz_summary})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password =  request.POST['password']
        post = User.objects.filter(username=username)
        if post:
            username = request.POST['username']
            request.session['username'] = username
            return redirect("profile:index")
        else:
            return render(request, 'profiles/login.html', {})
    return render(request, 'profiles/login.html', {})

def register(request):
    if request.session.has_key('username'):
        posts = request.session['username']
        query = User.objects.filter(username=posts)
        return render(request, 'profiles/index.html', {"query":query})
    else:
        return render(request, 'profiles/register.html', {})

def profile(request):
    if request.session.has_key('username'):
        posts = request.session['username']
        query = User.objects.filter(username=posts)
        return render(request, 'profiles/profile.html', {"query":query})
    else:
        return render(request, 'profiles/login.html', {})

def logout(request):
    try:
        del request.session['username']
    except:
     pass
    return render(request, 'profiles/login.html', {})
