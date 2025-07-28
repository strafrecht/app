from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from treemodeladmin.options import TreeModelAdmin  # Re-enabled for Wagtail 6.x - testing compatibility
from .models import *


class FlashcardAdmin(TreeModelAdmin):  # Re-enabled TreeModelAdmin for Wagtail 6.x testing
    model = Flashcard
    parent_field = 'deck'  # TreeModelAdmin specific - flashcard belongs to deck
    list_display = ('id',)

@modeladmin_register
class DeckAdmin(TreeModelAdmin):  # Re-enabled TreeModelAdmin for Wagtail 6.x testing
    model = Deck
    menu_label = 'Flashcard-Decks'
    menu_icon = 'list-ul'
    list_display = ('id', 'submission', 'approved', 'name', 'wiki_category', 'user', 'created', 'updated')
    search_fields = ('name', 'id')
    ordering = ['-created']
    child_field = 'flashcards'  # TreeModelAdmin specific - deck has many flashcards (related_name)
    child_model_admin = FlashcardAdmin  # TreeModelAdmin specific - child admin for flashcards
