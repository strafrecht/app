from __future__ import unicode_literals, absolute_import

from django.urls import include, re_path
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from wagtail import hooks
from . import urls
from wagtail.admin.menu import MenuItem


@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        re_path(r'^polls/', include(urls)),
    ]


@hooks.register('construct_main_menu')
def construct_main_menu(request, menu_items):
    menu_items.append(
        MenuItem(_('Polls'), reverse('wagtailpolls_index'),
                 classname='icon icon-group', order=250)
    )
