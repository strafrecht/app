from django.db import models
from django.contrib.auth.models import User
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel

from core.models import Submission
from core.edit_handlers import ReadOnlyPanel
"""
Each category has several decks and each deck has a number of flashcards (flipcards).

app workflow:
First a user go to the profile section in the website, click flashcards
sub menu and start creating first a category, then the decks related to
the category and finally the cards associated to each deck.

goal:
to use the flashcards to study and memorize their content. all cards, decks and
categories are personal for the user, they only show up to the user that
created them. a learning mode is also created, there you have a final score
on how good you memorized the flashcards (similar to anki).

Category in this case is NOT the wiki category. The wiki category can be added
from the wiki.Article model
"""


class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(self.name)


class Deck(ClusterableModel):

    class Meta:
        verbose_name = "Flashcard-Deck"

    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    submission = models.ForeignKey(Submission, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    wiki_category = models.ForeignKey('wiki.Article', on_delete=models.SET_NULL, null=True, blank=True, related_name='flashcard_decks')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    panels = [
        FieldPanel('name'),
        ReadOnlyPanel('user', heading="Current question version"),
        FieldPanel('approved'),
        FieldPanel('wiki_category'),
        InlinePanel('flashcards',heading='Flashcards'),
    ]

    def __str__(self):
        return "{}".format(self.name)

    def title(self):
        return self.__str__()


class Flashcard(ClusterableModel):
    deck = ParentalKey(Deck, on_delete=models.CASCADE, related_name='flashcards')
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    front_side = models.CharField(max_length=500)
    back_side = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    panels = [
        FieldPanel('user'),
        FieldPanel('front_side'),
        FieldPanel('back_side'),
    ]

    def __str__(self):
        return "{} - {} - {}".format(self.front_side, self.back_side, self.deck.name)
