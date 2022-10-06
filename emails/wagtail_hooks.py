from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from birdsong.options import CampaignAdmin
from birdsong.models import Contact

from .filters import ContactFilter
from .models import NewsletterEmail, LSHNewsletter

# You may want to add your own modeladmin here to list/edit/add contacts
@modeladmin_register
class ContactAdmin(ModelAdmin):
    model = Contact
    menu_label = 'NL Adressen'
    menu_icon = 'user'
    list_diplay = ('email', 'tags') # FIXME: tag sdoes not work

@modeladmin_register
class LSHNewsletterAdmin(CampaignAdmin):
    campaign = LSHNewsletter
    menu_label = 'LSH Newsletter'
    menu_icon = 'mail'
    menu_order = 200
    contact_class = Contact
    contact_filter_class = ContactFilter
