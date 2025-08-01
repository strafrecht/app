from django.conf import settings
from django.utils.module_loading import import_string
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import re_path
from django.utils.translation import gettext as _
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from wagtail_modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register
from wagtail_modeladmin.helpers import AdminURLHelper, ButtonHelper
from wagtail_modeladmin.views import IndexView
from birdsong.options import CampaignAdmin  # Re-enabled with forked wagtail-birdsong
from birdsong.models import Contact  # Re-enabled with forked wagtail-birdsong

from .filters import ContactFilter
from .models import NewsletterEmail, LSHNewsletter


class ContactButtonHelper(ButtonHelper):
    """Custom button helper for Contact admin to add bulk actions."""

    def get_buttons_for_obj(self, obj, **kwargs):
        """Get buttons for individual contact objects."""
        buttons = super().get_buttons_for_obj(obj, **kwargs)
        return buttons

    def get_buttons_for_listing(self, **kwargs):
        """Add bulk delete button to the listing page."""
        buttons = super().get_buttons_for_listing(**kwargs)

        # Add bulk delete button
        bulk_delete_button = {
            'url': self.url_helper.get_action_url('bulk_delete_page'),
            'label': _('Bulk Delete'),
            'title': _('Delete multiple subscribers'),
            'classname': 'button button-secondary icon icon-bin',
        }

        buttons.append(bulk_delete_button)
        return buttons


class ContactAdmin(ModelAdmin):
    model = Contact
    menu_label = 'Abonnenten'
    menu_icon = 'user'
    list_display = ('email',)
    search_fields = ('email',)
    ordering = ['-email']
    button_helper_class = ContactButtonHelper
    index_template_name = 'modeladmin/birdsong/contact/index.html'

    def get_admin_urls_for_registration(self):
        """Register custom admin URLs for bulk actions."""
        urls = super().get_admin_urls_for_registration()

        def gen_url(pattern, view, name=None):
            if not name:
                name = pattern
            return re_path(
                self.url_helper.get_action_url_pattern(pattern),
                view,
                name=self.url_helper.get_action_url_name(name),
            )

        urls = (
            gen_url("bulk_delete", self.bulk_delete_view),
            gen_url("bulk_delete_page", self.bulk_delete_page_view),
        ) + urls

        return urls

    def bulk_delete_page_view(self, request):
        """Show bulk delete page with contact selection."""
        contacts = Contact.objects.all().order_by('email')

        # Apply search filter if provided
        search_query = request.GET.get('q', '')
        if search_query:
            contacts = contacts.filter(email__icontains=search_query)

        # Apply tag filter if provided
        tag_filter = request.GET.get('tags__id__exact', '')
        if tag_filter:
            contacts = contacts.filter(tags__id=tag_filter)

        context = {
            'contacts': contacts,
            'search_query': search_query,
            'tag_filter': tag_filter,
            'bulk_delete_url': self.url_helper.get_action_url('bulk_delete'),
            'back_url': self.url_helper.get_action_url('index'),
        }

        return render(request, 'emails/bulk_delete_contacts.html', context)

    def bulk_delete_view(self, request):
        """Handle bulk delete action."""
        if request.method == 'POST':
            contact_ids = request.POST.getlist('contact_ids')
            if contact_ids:
                deleted_count = Contact.objects.filter(id__in=contact_ids).count()
                Contact.objects.filter(id__in=contact_ids).delete()
                messages.success(
                    request,
                    _("Successfully deleted {} subscriber(s).").format(deleted_count)
                )
            else:
                messages.warning(request, _("No subscribers selected for deletion."))

        # Redirect back to the contact list
        return redirect(self.url_helper.get_action_url('index'))

class LSHNewsletterAdmin(CampaignAdmin):
    model = LSHNewsletter
    menu_label = 'LSH'
    menu_icon = 'mail'
    contact_class = Contact
    contact_filter_class = ContactFilter

    # Use configured backend class with fallback
    @property
    def backend_class(self):
        backend_class_path = getattr(settings, 'BIRDSONG_BACKEND_CLASS', 'birdsong.backends.smtp.SMTPEmailBackend')
        try:
            return import_string(backend_class_path)
        except ImportError:
            # Fallback to SMTP backend if SES backend fails to import
            fallback_path = getattr(settings, 'BIRDSONG_FALLBACK_BACKEND', 'birdsong.backends.smtp.SMTPEmailBackend')
            return import_string(fallback_path)

@modeladmin_register
class NewsletterMenuAdmin(ModelAdminGroup):
    menu_label = 'Newsletter'
    menu_icon = 'folder'
    items = (LSHNewsletterAdmin, ContactAdmin)
