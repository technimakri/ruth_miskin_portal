from django import forms
from django.forms import FileField


class CSVUploadForm(forms.Form):
    csv_file = FileField()
