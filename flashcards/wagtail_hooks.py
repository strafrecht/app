from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from treemodeladmin.options import TreeModelAdmin
from .models import *


class FlashcardAdmin(TreeModelAdmin):
    model = Flashcard
    list_display = ('id',)

@modeladmin_register
class DeckAdmin(TreeModelAdmin):
    model = Deck
    menu_label = 'Flashcard-Decks'
    menu_icon = 'list-ul'
    list_display = ('id', 'submission', 'approved', 'name', 'wiki_category', 'user', 'created', 'updated')
    search_fields = ('name', 'id')
    ordering = ['-created']
    child_field = 'flashcard_set'
    child_model_admin = FlashcardAdmin
