import json

from django import forms
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from wagtail.admin.staticfiles import versioned_static
from wagtail.admin.widgets import AdminChooser
#from wagtail.admin.widgets.button import ListingButton


class AdminPollChooser(AdminChooser):

    def __init__(self, model, **kwargs):
        self.target_model = model
        name = self.target_model._meta.verbose_name
        self.choose_one_text = _('Choose %s') % name
        self.choose_another_text = _('Choose another %s') % name
        self.link_to_chosen_text = _('Edit this %s') % name

        super().__init__(**kwargs)

    def render_html(self, name, value, attrs):
        instance, value = self.get_instance_and_id(self.target_model, value)

        original_field_html = super().render_html(name, value, attrs)

        return render_to_string("widgets/poll_chooser.html", {
            'widget': self,
            'model_opts': self.target_model._meta,
            'original_field_html': original_field_html,
            'attrs': attrs,
            'value': value,
            'item': instance,
        })

    def render_js_init(self, id_, name, value):
        model = self.target_model

        return "createPollChooser({id}, {model});".format(
            id=json.dumps(id_),
            model=json.dumps('{app}/{model}'.format(
                app=model._meta.app_label,
                model=model._meta.model_name)))

    @property
    def media(self):
        return forms.Media(js=[
            versioned_static('js/poll_chooser_modal.js'),
            versioned_static('js/poll_chooser.js'),
        ])


#class SnippetListingButton(ListingButton):
#    pass

"""
from __future__ import absolute_import, unicode_literals

import json
from django.contrib.contenttypes.models import ContentType

from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from wagtail.admin.widgets import AdminChooser


class AdminPollChooser(AdminChooser):
    target_content_type = None

    class Media:
        js = ['js/poll_chooser.js']

    def __init__(self, content_type=None, **kwargs):
        model = kwargs.pop('model', None)
        self.choose_one_text = (_('Choose a poll'))
        self.choose_another_text = (_('Choose another poll'))
        self.link_to_chosen_text = (_('Edit this poll'))

        super(AdminPollChooser, self).__init__(**kwargs)
        if content_type is not None:
            self.target_content_type = content_type
        elif model is not None:
            self.target_content_type = ContentType.objects.get_for_model(model)
        else:
            raise RuntimeError("Unable to set model from both content_type and model")

    def render_html(self, name, value, attrs):
        model_class = self.target_content_type.model_class()
        instance, value = self.get_instance_and_id(model_class, value)

        original_field_html = super(AdminPollChooser, self).render_html(name, value, attrs)

        return render_to_string("widgets/poll_chooser.html", {
            'widget': self,
            'original_field_html': original_field_html,
            'attrs': attrs,
            'value': value,
            'item': instance,
        })

    def render_js_init(self, id_, name, value):
        return "createPollChooser({id});".format(id=json.dumps(id_))
"""
