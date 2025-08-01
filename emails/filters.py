from django_filters import FilterSet
from django_filters.filters import AllValuesFilter, CharFilter
from birdsong.models import Contact  # Re-enabled with forked wagtail-birdsong


class ContactFilter(FilterSet):
    email = CharFilter(lookup_expr='icontains', label='Email contains')

    class Meta:
        model = Contact
        fields = ('email',)
