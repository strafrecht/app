from django.contrib import admin

from .models import Suggestion, SuggestionVote

class SuggestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'user', 'votes']
    prepopulated_fields = {'slug': ('title',)}

class VoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'ip']

admin.site.register(Suggestion, SuggestionAdmin)
admin.site.register(SuggestionVote, VoteAdmin)
