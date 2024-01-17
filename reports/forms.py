from django import forms

from django.forms import ModelForm

from fin.models import (
	Account, 
	Category, 
	Payee, 
	L1Group, 
	GroupedCat
)

class TransQueryForm(forms.Form):
	sel_payee = forms.ModelChoiceField(queryset=Payee.objects.all())
	sel_account = forms.ModelChoiceField(queryset=Account.objects.all())
	sel_category = forms.ModelChoiceField(queryset=Category.objects.all())
	sel_l1 = forms.ModelChoiceField(queryset=L1Group.objects.all())