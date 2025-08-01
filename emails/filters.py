from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django_filters import FilterSet
from django_filters.filters import AllValuesFilter, CharFilter
from birdsong.models import Contact  # Re-enabled with forked wagtail-birdsong


class ContactFilter(FilterSet):
    email = CharFilter(lookup_expr='icontains', label='Email contains')
    single_email = forms.EmailField(
        required=False,
        label='Send to single email address',
        help_text='Enter an email address to send to a single recipient (will be created if it doesn\'t exist)'
    )

    class Meta:
        model = Contact
        fields = ('email',)

    def __init__(self, data=None, *args, **kwargs):
        super().__init__(data, *args, **kwargs)
        # Add the single_email field to the form
        self.form.fields['single_email'] = forms.EmailField(
            required=False,
            label='Send to single email address',
            help_text='Enter an email address to send to a single recipient (will be created if it doesn\'t exist)'
        )

    @property
    def qs(self):
        """Override to handle single email sending"""
        # Check if single_email is provided
        if hasattr(self, 'data') and self.data and self.data.get('single_email'):
            single_email = self.data.get('single_email').strip()
            if single_email:
                try:
                    validate_email(single_email)
                    # Get or create the contact
                    contact, created = Contact.objects.get_or_create(email=single_email)
                    return Contact.objects.filter(pk=contact.pk)
                except ValidationError:
                    # Invalid email, return empty queryset
                    return Contact.objects.none()

        # Otherwise, use the normal filtering
        return super().qs
