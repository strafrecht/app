from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
# from treemodeladmin.options import TreeModelAdmin  # Temporarily disabled for Wagtail 3.0 upgrade
from .models import *


class FlashcardAdmin(ModelAdmin):  # Temporarily changed from TreeModelAdmin for Wagtail 3.0 upgrade
    model = Flashcard
    list_display = ('id',)

@modeladmin_register
class DeckAdmin(ModelAdmin):  # Temporarily changed from TreeModelAdmin for Wagtail 3.0 upgrade
    model = Deck
    menu_label = 'Flashcard-Decks'
    menu_icon = 'list-ul'
    list_display = ('id', 'submission', 'approved', 'name', 'wiki_category', 'user', 'created', 'updated')
    search_fields = ('name', 'id')
    ordering = ['-created']
    # child_field = 'flashcard_set'  # TreeModelAdmin specific - temporarily disabled
    # child_model_admin = FlashcardAdmin  # TreeModelAdmin specific - temporarily disabled
