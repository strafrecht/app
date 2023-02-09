from django import template
from django.contrib.contenttypes.models import ContentType
from wiki.models.article import Article

register = template.Library()

@register.filter
def has_bookmark(user, article):
    return user.bookmarks.filter(content_id=article.id,
                                 content_type=ContentType.objects.get_for_model(Article).id).exists()

@register.filter
def bookmark_class(user, article):
    if has_bookmark(user, article):
        return "bookmark-present"
    else:
        return "bookmark-absent"

@register.filter
def class_to_name(instance):
    name = instance._meta.verbose_name
    if name == "article revision":
        name = "Problemfeldwiki"
    return name

@register.filter
def submission_bg_color(instance):
    if instance.status == "APPROVED":
        return "success"

    if instance.status == "REJECTED":
        return "danger"

    return "info"

@register.filter
def submission_fg_color(instance):
    if instance.status == "APPROVED":
        return "text-black"

    if instance.status == "REJECTED":
        return "text-white"

    return "text-white"
