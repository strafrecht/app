from django import template

register = template.Library()

#@register.inclusion_tag('pages/tags/sidebars.html', takes_context=True)
#def sidebars(context):
#    return {
#        'sidebars': Sidebar.objects.all(),
#        'request': context['request'],
#    }

def prettify(value):
    """Removes all values of arg from the given string"""
    return value.replace('%20', ' ').replace('.pdf', '')

def banner(page):
    #parent = page.get_parent() if hasattr(page, 'get_parent') else None
    #parent = page.get_ancestors().first().get_first_child().get_first_child()

    if hasattr(page, 'get_ancestors'):
        parent = page.get_ancestors().first().get_first_child().get_first_child()
    else:
        parent = page.get_parent() if hasattr(page, 'get_parent') else None

    if hasattr(page, 'slug'):
        if page.slug == "lehre" or parent.slug == "lehre":
            return "/media/images/affe.original.jpg"

    if hasattr(page, 'header') and page.header is not None:
        return page.header.file.url
    elif hasattr(parent, 'genericpage') and parent.genericpage.header is not None:
        return parent.genericpage.header.file.url
    elif hasattr(parent, 'header') and parent.header is not None:
        return parent.header.file.url
    else:
        return False
#page.get_parent().header
#page.get_ancestors().first().get_first_child().get_first_child()

register.filter('prettify', prettify)
register.filter('banner', banner)
