from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return "{}".format(self.name)


class Deck(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    wiki_category = models.ForeignKey('wiki.Article', on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.name)


class Flashcard(models.Model):

    front_side = models.CharField(max_length=500)
    back_side = models.CharField(max_length=500)
    deck = models.ForeignKey(Deck, models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    probability = models.IntegerField(default=100)

    def __str__(self):
        # return str(self.front_side) + '' + str(self.back_side) + '' + str(self.deck.name)
        return "{} - {} - {}".format(self.front_side, self.back_side, self.deck.name)
        # return F"{self.front_side} {self.back_side} {self.deck.name}"
