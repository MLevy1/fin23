from django import forms

from django.forms import ModelForm

from fin.models import (
	Account,
	Payee,
	GroupedCat,
)

from .models import (
	Transaction,
	SubTransaction,
	Paycheck,
	PaycheckItems,
)

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
			#self.fields['account'].queryset = Account.objects.all()
			#self.fields['payee'].queryset = Payee.objects.all()

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
			'note',
		]

	def __init__(self, *args, **kwargs):
	    aAct = kwargs.pop("aAct", None)
	    pAct = kwargs.pop("pAct", None)
	    super(TransForm, self).__init__(*args, **kwargs)


	    for field in self.fields:
	        new_data = {"class": 'form-control'}
	        self.fields[str(field)].widget.attrs.update(new_data)

	        if aAct:
	            self.fields['account'].queryset = Account.objects.filter(active="True")

	        if pAct:
	            self.fields['payee'].queryset = Payee.objects.filter(active="True")

class TransSubTransForm(forms.ModelForm):
	class Meta:
		model = SubTransaction
		fields = [
		    'groupedcat',
		    'amount',
		    'note',
		]

	def __init__(self, *args, **kwargs):
		super(TransSubTransForm, self).__init__(*args, **kwargs)

		for field in self.fields:
			new_data = {
				"class": 'form-control',
			}
			self.fields[str(field)].widget.attrs.update(
				new_data
			)

		self.fields['groupedcat'].queryset = GroupedCat.objects.filter(l1group__active="True")

class UploadFileForm(forms.Form):
    file = forms.FileField()

class TransferForm(forms.Form):
    tid = forms.IntegerField()
    tdate = forms.DateField()
    acct_out = forms.ModelChoiceField(queryset=Account.objects.filter(active="True"))
    acct_in = forms.ModelChoiceField(queryset=Account.objects.filter(active="True"))
    tamt = forms.DecimalField(max_digits=18, decimal_places=2)

class CreditCardPaymentForm(forms.Form):
    tid = forms.IntegerField()
    tdate = forms.DateField()
    acct_out = forms.ModelChoiceField(queryset=Account.objects.filter(active="True"))
    acct_in = forms.ModelChoiceField(queryset=Account.objects.filter(active="True"))
    tamt = forms.DecimalField(max_digits=18, decimal_places=2)


class PaycheckForm(forms.ModelForm):
    class Meta:
        model = Paycheck
        fields = ['payee', 'note', 'active']

class PaycheckItemsForm(forms.ModelForm):
    class Meta:
        model = PaycheckItems
        fields = ['groupedcat', 'amount', 'note']

