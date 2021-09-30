from django.db.models import Count
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponseRedirect
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from .models import Suggestion, SuggestionVote

# Create your views here.
@csrf_exempt
@xframe_options_exempt
def index(request):
    suggestions = Suggestion.objects.all().annotate(votes=Count('suggestionvote')).order_by('-votes')
    ip = get_ip(request)
    voted = [s.id for s in Suggestion.objects.filter(suggestionvote__ip=ip)]
    return render(request, 'feedback/index.html', {'suggestions': suggestions, 'voted': voted})

@csrf_exempt
@xframe_options_exempt
def form(request):
    return render(request, 'feedback/form.html') 

@csrf_exempt
@xframe_options_exempt
def save(request):
    user = User.objects.get(username="Anonym")
    suggestion = Suggestion(title=request.POST.get('title'), description=request.POST.get('description'), user=user)
    suggestion.save()
    print(suggestion)
    return HttpResponseRedirect(reverse('feedback:index'))

@csrf_exempt
@xframe_options_exempt
def detail(request, suggestion_id, slug):
    suggestion = Suggestion.objects.filter(id=suggestion_id)
    return render(request, 'feedback/detail.html', {'suggestion': suggestion})

@csrf_exempt
@xframe_options_exempt
def vote(request, suggestion_id, slug):
    ip_address = get_ip(request)
    suggestion = get_object_or_404(Suggestion, pk=suggestion_id) 

    try:
        vote = suggestion.suggestionvote_set.get(ip=ip_address)
    except (KeyError, SuggestionVote.DoesNotExist):
        print('except')
        vote = SuggestionVote(suggestion=suggestion, ip=ip_address)
        vote.save()
        return HttpResponseRedirect(reverse('feedback:index'))
    else:
        print('else')
        vote.delete()
        return HttpResponseRedirect(reverse('feedback:index'))


def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip
