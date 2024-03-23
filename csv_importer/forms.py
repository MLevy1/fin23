from django import forms

SOURCE_CHOICES = (
    ("V", "Capital One Venture"),
    ("P", "PNC Credit"),
    ("A", "Ally Bank"),
    ("C", "Chase Credit"),
)

class UploadFileForm(forms.Form):
    source = forms.ChoiceField(choices = SOURCE_CHOICES)
    file = forms.FileField()
