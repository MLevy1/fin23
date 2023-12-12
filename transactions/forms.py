from django import forms

from django.forms import ModelForm

from fin.models import (
	Account, 
	Category, 
	Payee, 
	L1Group, 
	GroupedCat,
)

from .models import (
	Transaction,
	SubTransaction,
)

from django.contrib.admin.widgets import AdminDateWidget

class AddTransaction(ModelForm):
	class Meta:
		model = Transaction
		widgets = {
			'tdate': forms.DateInput(attrs={'format': 'yyyy-mm-dd','type':'date'}),
		}
		fields = "__all__"
		
	def __init__(self, *args, **kwargs):
			super(AddTransaction, self).__init__(*args, **kwargs)			

			# Filter active accounts and payees
			self.fields['account'].queryset = Account.objects.filter(active=True)
			self.fields['payee'].queryset = Payee.objects.filter(active=True)

class AddTransactionAll(ModelForm):
	class Meta:
		model = Transaction
		widgets = {
			'tdate': forms.DateInput(attrs={'format': 'yyyy-mm-dd','type':'date'}),
		}
		fields = "__all__"
		
	def __init__(self, *args, **kwargs):
			super(AddTransactionAll, self).__init__(*args, **kwargs)			

			# Filter active accounts and payees
			self.fields['account'].queryset = Account.objects.all()
			self.fields['payee'].queryset = Payee.objects.all()

class TransForm(forms.ModelForm):
	required_css_class = 'required-field'
	class Meta:
		model = Transaction
		
		widgets = {
			'tdate': forms.DateInput(attrs={'format': 'yyyy-mm-dd','type':'date'}),
		}

		fields = [
			'tid', 
			'tdate', 
			'account', 
			'payee', 
			'match', 
			'oldCat', 
			'oldPayee', 
			'note',
		]
		
	def __init__(self, *args, **kwargs):
		super(TransForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			new_data = {
				"class": 'form-control',
			}
				
			self.fields [str(field)]. widget.attrs.update(
				new_data
			)		

			# Filter active accounts and payees
			self.fields['account'].queryset = Account.objects.all()
			self.fields['payee'].queryset = Payee.objects.all()

class TransSubTransForm(forms.ModelForm):
	class Meta:
		model = SubTransaction
		fields = ['category', 'groupedcat', 'amount', 'note']
		
	def __init__(self, *args, **kwargs):
		super(TransSubTransForm, self).__init__(*args, **kwargs)
		
		print(self.instance.groupedcat)

		for field in self.fields:
			new_data = {
				"class": 'form-control',
			}
			self.fields[str(field)].widget.attrs.update(
				new_data
			)
		
		if self.instance.groupedcat:

			self.fields['category'].widget.attrs.update(
				{
					"hx-get": "/trans/load-gc",
					"hx-target": "#id_groupedcat",
					"hx-trigger": "change",
					"hx-swap": "innerHTML",
				}
			)

		else:

			self.fields['category'].widget.attrs.update(
				{
					"hx-get": "/trans/load-gc",
					"hx-target": "#id_groupedcat",
					"hx-trigger": "change, load delay:500ms",
					"hx-swap": "innerHTML",
				}
			)
			
