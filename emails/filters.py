from django_filters import FilterSet
from django_filters.filters import AllValuesFilter

from birdsong.models import Contact


class ContactFilter(FilterSet):
    campaign = AllValuesFilter()
    email = AllValuesFilter()
    receipt = AllValuesFilter()

    class Meta:
        model = Contact
        fields = ('campaign', 'email', 'receipt',)
