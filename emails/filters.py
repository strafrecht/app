from django_filters import FilterSet
from django_filters.filters import AllValuesFilter

from birdsong.models import Contact


class ContactFilter(FilterSet):
    email = AllValuesFilter()

    class Meta:
        model = Contact
        fields = ('email',)
