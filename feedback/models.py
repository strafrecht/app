from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class Suggestion(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):   
        self.slug = slugify(self.title)
        super(Suggestion, self).save(*args, **kwargs)

    def votes(self):
        return self.vote_set.count()

class SuggestionVote(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING)
    ip = models.CharField(blank=True, max_length=15)
    suggestion = models.ForeignKey(Suggestion, on_delete=models.CASCADE)
    vote_date = models.DateTimeField(auto_now_add=True)
