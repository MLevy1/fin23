from django import forms

from django.forms import ModelForm

from django.forms.widgets import DateInput

from fin.models import (
	Account, 
	Category, 
	Payee, 
	L1Group, 
	GroupedCat
)

from django.contrib.admin.widgets import AdminDateWidget

class TransQueryForm(forms.Form):
	sel_payee = forms.ModelChoiceField(queryset=Payee.objects.all(), required=False, label='Payee')
	sel_account = forms.ModelChoiceField(queryset=Account.objects.all(), required=False, label='Account')
	sel_category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, label='Category')
	sel_l1 = forms.ModelChoiceField(queryset=L1Group.objects.all(), required=False, label='L1 Group')	
	sel_min_tdate = forms.DateField(required=False, label='Min Date', widget=AdminDateWidget(attrs={'format': 'yyyy-mm-dd','type':'date'}))
	sel_max_tdate = forms.DateField(required=False, label='Max Date', widget=AdminDateWidget(attrs={'format': 'yyyy-mm-dd','type':'date'}))
	
	def __init__(self, *args, **kwargs):
		super(TransQueryForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			new_data = {
				"class": 'form-control',
			}
				
			self.fields [str(field)]. widget.attrs.update(
				new_data
			)