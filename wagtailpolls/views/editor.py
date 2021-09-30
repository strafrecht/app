from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils.text import capfirst
from django.urls import reverse
from django.template.response import TemplateResponse
from functools import lru_cache

from wagtail.admin import messages
from wagtail.admin.edit_handlers import (ObjectList, extract_panel_definitions_from_model_class)
from wagtail.core import hooks
from wagtail.core.models import Page
from wagtail.snippets.permissions import get_permission_name, user_can_edit_snippet_type

def get_snippet_model_from_url_params(app_name, model_name):
	"""
	Retrieve a model from an app_label / model_name combo.
	Raise Http404 if the model is not a valid snippet type.
	"""
	try:
		model = apps.get_model(app_name, model_name)
	except LookupError:
		raise Http404
	if model not in get_snippet_models():
		# don't allow people to hack the URL to edit content types that aren't registered as snippets
		raise Http404

	return model	

SNIPPET_EDIT_HANDLERS = {}

def get_poll_edit_handler(model):
	if model not in SNIPPET_EDIT_HANDLERS:
		if hasattr(model, 'edit_handler'):
			edit_handler = model.edit_handler
		else:
			panels = extract_panel_definitions_from_model_class(model)
			edit_handler = ObjectList(panels)

		SNIPPET_EDIT_HANDLERS[model] = edit_handler.bind_to(model=model)
	return SNIPPET_EDIT_HANDLERS[model]

@permission_required('wagtailadmin.access_admin')  # further permissions are enforced within the view
def create(request):
	from ..models import Poll
	model = Poll

	permission = get_permission_name('add', model)
	if not request.user.has_perm(permission):
		return permission_denied(request)

	for fn in hooks.get_hooks('before_create_snippet'):
		result = fn(request, model)
		if hasattr(result, 'status_code'):
			return result

	instance = model()
	edit_handler = get_poll_edit_handler(model)
	edit_handler = edit_handler.bind_to(request=request)
	form_class = edit_handler.get_form_class()

	if request.method == 'POST':
		form = form_class(request.POST, request.FILES, instance=instance)

		if form.is_valid():
			form.save()

			messages.success(
				request,
				_("%(snippet_type)s '%(instance)s' created.") % {
					'snippet_type': capfirst(model._meta.verbose_name),
					'instance': instance
				},
				buttons=[
					messages.button(reverse(
						#'wagtailsnippets:edit', args=(app_label, model_name, quote(instance.pk))
						'wagtailpolls_edit', args=(instance.id,)
					), _('Edit'))
				]
			)

			for fn in hooks.get_hooks('after_create_snippet'):
				result = fn(request, instance)
				if hasattr(result, 'status_code'):
					return result

			return redirect('wagtailpolls_index')
		else:
			messages.validation_error(
				request, _("The snippet could not be created due to errors."), form
			)
	else:
		form = form_class(instance=instance)

	edit_handler = edit_handler.bind_to(instance=instance, form=form)

	return TemplateResponse(request, 'wagtailpolls/create.html', {
		'model_opts': model._meta,
		'edit_handler': edit_handler,
		'form': form,
	})	


@permission_required('wagtailadmin.access_admin')  # further permissions are enforced within the view
def edit(request, poll_pk):
	from ..models import Poll
	model = Poll
	poll = get_object_or_404(Poll, pk=poll_pk)

	permission = get_permission_name('change', model)
	if not request.user.has_perm(permission):
		return permission_denied(request)

	instance = poll

	for fn in hooks.get_hooks('before_edit_snippet'):
		result = fn(request, instance)
		if hasattr(result, 'status_code'):
			return result

	edit_handler = get_poll_edit_handler(Poll)
	edit_handler = edit_handler.bind_to(instance=instance, request=request)
	form_class = edit_handler.get_form_class()

	if request.method == 'POST':
		form = form_class(request.POST, request.FILES, instance=instance)

		if form.is_valid():
			form.save()

			messages.success(
				request,
				_("%(snippet_type)s '%(instance)s' updated.") % {
					'snippet_type': capfirst(model._meta.verbose_name),
					'instance': instance
				},
				buttons = [
					messages.button(reverse(
						'wagtailpolls_edit', args=(poll,)
					), _('Edit'))
				]
			)

			for fn in hooks.get_hooks('after_edit_snippet'):
				result = fn(request, instance)
				if hasattr(result, 'status_code'):
					return result

			return redirect('wagtailpolls_index')
		else:
			messages.validation_error(
				request, _("The snippet could not be saved due to errors."), form
			)

	else:
		form = form_class(instance=instance)

	edit_handler = edit_handler.bind_to(form=form)

	return TemplateResponse(request, 'wagtailpolls/edit.html', {
		'modal_opts': model._meta,
		'instance': instance,
		'poll': instance,
		'edit_handler': edit_handler,
		'form': form
	})

	#return render(request, 'wagtailpolls/edit.html', {
	#	'poll': poll,
	#	'form': form,
	#	'edit_handler': edit_handler,
	#})


@permission_required('wagtailadmin.access_admin')  # further permissions are enforced within the view
def delete(request, poll_pk):
	from ..models import Poll

	poll = get_object_or_404(Poll, pk=poll_pk)

	if request.method == 'POST':
		poll.delete()
		return redirect('wagtailpolls_index')

	return render(request, 'wagtailpolls/delete.html', {
		'poll': poll,
	})


@permission_required('wagtailadmin.access_admin')  # further permissions are enforced within the view
def copy(request, poll_pk):
	from ..models import Poll

	poll = Poll.objects.get(id=poll_pk)

	if request.method == 'POST':
		poll.pk = None
		poll.save()
		return redirect('wagtailpolls_index')

	return render(request, 'wagtailpolls/copy.html', {
		'poll': poll,
	})
