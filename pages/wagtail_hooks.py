from django.utils.html import format_html
from django.templatetags.static import static
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineStyleElementHandler, BlockElementHandler, InlineEntityElementHandler
from wagtail.core import hooks
from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register
)
import wagtail.admin.rich_text.editors.draftail.features as draftail_features

from pages.models.news import ArticlePage
from pages.models.people import People
from pages.models.events import EventPage
from pages.models.sessions import SessionPage
from pages.models.exams import Exams

class PeopleModelAdmin(ModelAdmin):
    model = People
    menu_label = 'Personen'
    menu_icon = 'user'
    menu_order= 202
    list_display = ('last_name', 'first_name', 'status', 'role')

class EventsModelAdmin(ModelAdmin):
    model = EventPage
    menu_label = 'Events'
    menu_icon = 'site'
    menu_order= 201
    list_display = ('title', 'speaker_description_html', 'date')

class ArticlesModelAdmin(ModelAdmin):
    model = ArticlePage
    menu_label = 'News-Artikel'
    menu_icon = 'doc-full'
    menu_order= 201
    list_display = ('date', 'title', 'author')

class SessionsModelAdmin(ModelAdmin):
    model = SessionPage
    menu_label = 'Lehrveranstaltungen'
    menu_icon = 'date'
    menu_order= 200
    list_display = ('semester', 'name', 'speaker')

class ExamsModelAdmin(ModelAdmin):
    model = Exams
    menu_label = 'Klausurdatenbank'
    menu_icon = 'edit'
    menu_order= 200
    list_display = ('date', 'type', 'difficulty', 'problems_html')

#modeladmin_register(NodeAdmin)
modeladmin_register(PeopleModelAdmin)
modeladmin_register(EventsModelAdmin)
modeladmin_register(ArticlesModelAdmin)
modeladmin_register(SessionsModelAdmin)
modeladmin_register(ExamsModelAdmin)

# pages/news/polls/poll-eval/sessions/events/people/newsletter email/

@hooks.register("insert_global_admin_css", order=100)
def global_admin_css():
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static("css/columns.css")
    )

@hooks.register("insert_global_admin_css", order=100)
def global_admin_css():
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static("css/wagtail/sessions.css")
    )

@hooks.register('construct_main_menu')
def hide_snippets_menu_item(request, menu_items):
  for item in menu_items: print("XXX: {}".format(item.name))
  menu_items[:] = [item for item in menu_items if item.name not in ['snippets', 'images', 'documents', 'categories', 'contacts', 'Polls']]

@hooks.register('register_rich_text_features')
def register_roofline_feature(features):
    feature_name = 'roofline'
    type_ = 'roofline'

    control = {
        'type': type_,
        'label': '⛅',
        'description': 'Dachzeile',
        'element': 'p',
    }

    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.BlockFeature(control, css={'all': ['base.css']})
    )

    features.register_converter_rule('contentstate', feature_name, {
        'from_database_format': {'p[class=roofline]': BlockElementHandler(type_)},
        'to_database_format': {'block_map': {type_: {'element': 'p', 'props': {'class': 'roofline'}}}},
    })

    features.default_features.append('roofline')

@hooks.register('register_rich_text_features')
def register_revised_label_feature(features):
    feature_name = 'revised_label'
    type_ = 'revised_label'

    control = {
        'type': type_,
        'label': '♻️',
        'description': 'Überarbeitet Label',
        'element': 'span',
    }

    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.BlockFeature(control, css={'all': ['base.css']})
    )

    features.register_converter_rule('contentstate', feature_name, {
        'from_database_format': {'p[label revised]': BlockElementHandler(type_)},
        'to_database_format': {'block_map': {type_: {'element': 'div', 'props': {'class': 'label revised'}}}},
    })

    features.default_features.append('revised_label')

@hooks.register('register_rich_text_features')
def register_new_label_feature(features):
    feature_name = 'new_label'
    type_ = 'new_label'

    control = {
        'type': type_,
        'label': '☝️',        
        'description': 'Neu Label',        
        'element': 'div',
    }

    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.BlockFeature(control, css={'all': ['base.css']})
    )

    features.register_converter_rule('contentstate', feature_name, {
        'from_database_format': {'p[class=label new]': BlockElementHandler(type_)},
        'to_database_format': {'block_map': {type_: {'element': 'div', 'props': {'class': 'label new'}}}},
    })

    features.default_features.append('new_label')

@hooks.register('register_rich_text_features')
def register_underline_feature(features):
    feature_name = 'underline'
    type_ = 'underline'

    control = {
        'type': type_,
        'label': 'U',
        'description': 'Underline',
    }

    features.register_editor_plugin(
        'draftail', feature_name,
        draftail_features.InlineStyleFeature(control)
    )

    features.register_converter_rule('contentstate', feature_name, {
        'from_database_format': {'span[style="text-decoration: underline"]': InlineStyleElementHandler(type_)},
        'to_database_format': {'block_map': {type_: {'element': 'div', 'props': {'class': 'underline'}}}},
    })

    features.default_features.append('underline')
