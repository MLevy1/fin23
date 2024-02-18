from django import forms

from .models import Csv

class UploadFileForm(forms.Form):
    file = forms.FileField()

class CsvModelForm(forms.ModelForm):
    class Meta:
        model = Csv
        fields = ('file_name',)

