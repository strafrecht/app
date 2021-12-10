from django.contrib import admin
from .models import Deck, Flashcard

"""
Registration of models in Django Admin
"""

class DeckAdmin(admin.ModelAdmin):
    pass


class FlashcardAdmin(admin.ModelAdmin):
      list_display = ['deck', "front_side", "probability"]


admin.site.register(Deck, DeckAdmin)
admin.site.register(Flashcard, FlashcardAdmin)  #register models in site