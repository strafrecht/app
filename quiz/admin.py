from django.db import models
from django.contrib import admin
from pagedown.widgets import AdminPagedownWidget

from .models import Question, QuestionVersion, AnswerVersion, Quiz, UserAnswer, Choice

class AnswerInline(admin.TabularInline):
    model = AnswerVersion
    extra = 0

    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'user')

    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }


class QuestionVersionAdmin(admin.ModelAdmin):
    list_display = ('question_id', 'title')
    inlines = [AnswerInline]

    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0

    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }

class UserAnswerAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]

    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget}
    }

class UserAnswerInline(admin.TabularInline):
    model = UserAnswer
    extra = 0

    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }

class QuizAdmin(admin.ModelAdmin):
    inlines = [UserAnswerInline]

    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget}
    }


admin.site.register(QuestionVersion, QuestionVersionAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(UserAnswer, UserAnswerAdmin)
