from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404


@permission_required('wagtailadmin.access_admin')
def results2(request, poll_pk):
    from ..models import Poll, Vote

    poll = get_object_or_404(Poll, pk=poll_pk)
    votes = Vote.objects.filter(question__poll=poll)
    total_votes = votes.count()

    return render(request, 'wagtailpolls/poll_results_2.html', {
        'poll': poll,
        'total_votes': total_votes,
    })
