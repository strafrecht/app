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

@modeladmin_register
class NewsletterMenuAdmin(ModelAdminGroup):
    menu_label = 'Newsletter'
    menu_icon = 'folder'
    items = (LSHNewsletterAdmin, ContactAdmin)
