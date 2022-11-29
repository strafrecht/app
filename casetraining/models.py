from django.db import models
from django.contrib.auth.models import User

class Casetraining(models.Model):

    DIFFICULTY_CHOICES = [
        ('shortcase',  'Shortcase'),
        ('beginner',   'Beginner'),
        ('advanced',   'Advanced'),
    ]

    name = models.CharField(max_length=100)
    difficulty = models.CharField(choices=DIFFICULTY_CHOICES, max_length=100, blank=False, null=False)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return "{} ({})".format(self.name, self.difficulty)
