from __future__ import absolute_import, unicode_literals

from django.urls import re_path
from .views import chooser, editor, results

#app_name = 'wagtailpolls'

urlpatterns = [
    # Choosers
    re_path(r'^choose/$', chooser.choose, name='wagtailpolls_choose'),
    re_path(r'^choose/(\w+)/(\w+)/$', chooser.choose, name='wagtailpolls_choose_specific'),
    re_path(r'^choose/(\d+)/$', chooser.chosen, name='wagtailpolls_chosen'),

    # General Urls
    re_path(r'^$', chooser.index, name='wagtailpolls_index'),
    re_path(r'^search/$', chooser.search, name='wagtailpolls_search'),
    re_path(r'^create/$', editor.create, name='wagtailpolls_create'),
    re_path(r'^edit/(?P<poll_pk>.*)/$', editor.edit, name='wagtailpolls_edit'),
    re_path(r'^delete/(?P<poll_pk>.*)/$', editor.delete, name='wagtailpolls_delete'),
    re_path(r'^copy/(?P<poll_pk>.*)/$', editor.copy, name='wagtailpolls_copy'),
    re_path(r'^results/(?P<poll_pk>.*)/$', results.results, name='wagtailpolls_results'),
    re_path(r'^results2/(?P<poll_pk>.*)/$', results2.results2, name='wagtailpolls_results_2'),
]
