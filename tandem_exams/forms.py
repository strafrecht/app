from django import forms
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
import magic
import os

# our pdf validator
# https://stackoverflow.com/questions/3648421/only-accept-a-certain-file-type-in-filefield-server-side

def validate_is_pdf(file):
    valid_mime_types = ['application/pdf']
    file_mime_type = magic.from_buffer(file.read(1024), mime=True)
    if file_mime_type not in valid_mime_types:
        raise ValidationError('Falscher Dateityp. Bitte ein PDF hochladen.')
    valid_file_extensions = ['.pdf']
    ext = os.path.splitext(file.name)[1]
    if ext.lower() not in valid_file_extensions:
        raise ValidationError('Falsche Dateiendung. Bitte eine Datei mit der Endung "pdf" hochladen.')

class ExamSolutionForm(forms.Form):
    file = forms.FileField(validators=(validate_is_pdf,), label="Gutachten")

    helper = FormHelper()
    helper.use_custom_control = True

class ExamCorrectionForm(forms.Form):
    correction = forms.FileField(validators=(validate_is_pdf,), label="Ausgefüllten Korrekturbogen hochladen")

    helper = FormHelper()
    helper.use_custom_control = True
