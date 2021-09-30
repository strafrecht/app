from django import forms

class QuestionForm(forms.Form):
    answer = forms.IntegerField(label='Answer ID', max_length=5)
