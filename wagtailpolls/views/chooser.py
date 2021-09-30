from __future__ import absolute_import, unicode_literals

import json

from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.core.paginator import Paginator
from six import text_type
from django.utils.translation import ugettext as _
from wagtail.admin.forms.search import SearchForm as AdminSearchForm
from wagtail.admin.modal_workflow import render_modal_workflow
from wagtail.search.backends import get_search_backend
from wagtail.search.index import class_is_indexed

from ..forms import SearchForm
from ..models import Poll
from ..pagination import paginate


@permission_required('wagtailadmin.access_admin')  # further permissions are enforced within the view
def index(request):
	poll_list = Poll.objects.all()
	search_form = SearchForm()

	paginator, page = paginate(
		request,
		Poll.objects.all(),
		per_page=8)

	return render(request, 'wagtailpolls/index.html', {
		'page': page,
		'paginator': paginator,
		'poll_list': poll_list,
		'search_form': search_form,
	})


@permission_required('wagtailadmin.access_admin')  # further permissions are enforced within the view
def search(request):
	poll_list = Poll.objects.all()
	search_form = SearchForm(request.GET or None)

	if search_form.is_valid():
		query = search_form.cleaned_data['query']
		poll_list = poll_list.search(query)

	else:
		paginator, page = paginate(
			request,
			Poll.objects.all(),
			per_page=8)

	paginator, page = paginate(
		request,
		poll_list,
		per_page=20)

	return render(request, 'wagtailpolls/search.html', {
		'page': page,
		'paginator': paginator,
		'poll_list': poll_list,
		'search_form': search_form,
	})


def choose(request):
	model = Poll

	items = Poll.objects.all()

	if not items.ordered:
	    items = items.order_by('pk')

	# Search
	is_searchable = class_is_indexed(model)
	is_searching = False
	search_query = None

	if is_searchable and 'q' in request.GET:
		search_form = AdminSearchForm(request.GET, placeholder=_("Search %(snippet_type_name)s") % {
			'snippet_type_name': model._meta.verbose_name
		})

		if search_form.is_valid():
			search_query = search_form.cleaned_data['q']

			search_backend = get_search_backend()
			items = search_backend.search(search_query, items)
			is_searching = True

	else:
		search_form = AdminSearchForm()

	# Pagination
	paginator = Paginator(items, per_page=25)
	paginated_items = paginator.get_page(request.GET.get('p'))

	# If paginating or searching, render "results.html"
	if request.GET.get('results', None) == 'true':
		return render(request, "wagtailpolls/results.html", {
			'model_opts': model._meta,
			'items': paginated_items,
			'query_string': search_query,
			'is_searching': is_searching,
		})

	return render_modal_workflow(
		request,
		'wagtailpolls/choose.html', None,
		{
			'model_opts': model._meta,
			'snippet_type_name': 'Poll',
			'items': paginated_items,
			'is_searchable': True,
			'search_form': search_form,
			'query_string': search_query,
			'is_searching': is_searching,
		}, json_data={'step': 'choose'}
	)


def chosen(request, id):
	model = Poll
	item = get_object_or_404(model, id=id)

	snippet_data = {
		'id': str(item.pk),
		'string': str(item),
		'edit_link': reverse('wagtailpolls_edit', args=(item,))
	}

	return render_modal_workflow(
		request,
		None, None,
		None, json_data={'step': 'chosen', 'result': snippet_data}
	)
