from django.conf import settings
from django.utils.module_loading import import_string
from wagtail_modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register
from birdsong.options import CampaignAdmin  # Re-enabled with forked wagtail-birdsong
from birdsong.models import Contact  # Re-enabled with forked wagtail-birdsong

from .filters import ContactFilter
from .models import NewsletterEmail, LSHNewsletter

class ContactAdmin(ModelAdmin):
    model = Contact
    menu_label = 'Abonnenten'
    menu_icon = 'user'
    #list_diplay = ('email')

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
