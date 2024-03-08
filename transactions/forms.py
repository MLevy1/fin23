from django import forms

from fin.models import (
	Account,
	Payee,
	GroupedCat,
)

from .models import (
	Transaction,
	SubTransaction,
)

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
    tdate = forms.DateField(label="Date", widget=forms.DateInput(attrs={'format': 'yyyy-mm-dd', 'type': 'date'}))
    acct_out = forms.ModelChoiceField(label="From Account", queryset=Account.objects.filter(active="True"))
    acct_in = forms.ModelChoiceField(label="To Account", queryset=Account.objects.filter(active="True"))
    tamt = forms.DecimalField(label="Amount", max_digits=18, decimal_places=2)
    cc = forms.BooleanField(label="Credit Card Payment", required=False)

class FixedForm(forms.Form):
    tid = forms.IntegerField()
    tdate = forms.DateField(widget=forms.DateInput(attrs={'format': 'yyyy-mm-dd', 'type': 'date'}))
    pay = forms.ModelChoiceField(queryset=Payee.objects.filter(active="True"))
    acct = forms.ModelChoiceField(queryset=Account.objects.filter(active="True"))