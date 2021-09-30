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

register.filter('prettify', prettify)
