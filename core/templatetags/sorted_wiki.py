from django import template

register = template.Library()

@register.filter
def sorted_wiki(children, urlpath):

    # key is path of wiki entry, value is array of slugs in desired order
    custom_order = {
        "": ["at", "bt", "rechtsprechung", "offene-problemfelder"],
        "at/": ["tb", "rw", "schuld", "irrtum", "taeterschaft", "teilnahme", "versuch", "fahrlaessig", "unterl"],
    }

    ordered = custom_order.get(urlpath.path)

    if not ordered:
        return children

    return sorted(children, key=lambda child: ordered.index(child.slug) if child.slug in ordered else 999, reverse=False)
