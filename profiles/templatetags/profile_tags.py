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
