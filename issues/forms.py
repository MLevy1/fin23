from django import forms
from django.forms import ModelForm

class AddIssue(ModelForm):
	class Meta:
		model = Issue
		fields = "__all__"