from django import forms

from django.forms import ModelForm

from .models import (
	Account, 
	Category, 
	Payee, 
	Trans, 
	L1Group, 
	GroupedCat
)

from django.contrib.admin.widgets import AdminDateWidget

class PayeeMergeForm(forms.Form):
    source_payee = forms.ModelChoiceField(queryset=Payee.objects.filter(active=True))
    target_payee = forms.ModelChoiceField(queryset=Payee.objects.all())

class PayeeCategoryUpdate(forms.Form):
	source_payee = forms.ModelChoiceField(queryset=Payee.objects.filter(active=True))
	target_category = forms.ModelChoiceField(queryset=Category.objects.all())
	
class PayeeCategoryUpdateAll(forms.Form):
	source_payee = forms.ModelChoiceField(queryset=Payee.objects.all())
	target_category = forms.ModelChoiceField(queryset=Category.objects.all())

#uses get parameters filter the list but cant be used becuase it would have to filter by l1s and not categories

class PayeeGroupedCatUpdateAll(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Get the selected category from the form's initial data
        category = self.initial.get('category')

        # Update the groupedcat queryset based on the selected category
        if category:
            self.fields['groupedcat'].queryset = GroupedCat.objects.filter(l1group__aligned_category=category)

    payee = forms.ModelChoiceField(queryset=Payee.objects.all())
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    groupedcat = forms.ModelChoiceField(queryset=GroupedCat.objects.all())

class CategoryGroupedCatUpdateAll(forms.Form):

	category = forms.ModelChoiceField(queryset=Category.objects.all())
	groupedcat = forms.ModelChoiceField(queryset=GroupedCat.objects.all())

class PayeeAccountUpdate(forms.Form):
	source_payee = forms.ModelChoiceField(queryset=Payee.objects.all())
	target_account = forms.ModelChoiceField(queryset=Account.objects.all())

class AddAccount(ModelForm):
	class Meta:
		model = Account
		fields = "__all__"

class AddCategory(ModelForm):
	class Meta:
		model = Category
		fields = "__all__"
		
class AddPayee(ModelForm):
	class Meta:
		model = Payee
		fields = "__all__"

class L1GroupForm(ModelForm):
	class Meta:
		model = L1Group
		fields = "__all__"

class GroupedCatForm(ModelForm):
	class Meta:
		model = GroupedCat
		fields = "__all__"

class AddTransaction(ModelForm):
	class Meta:
		model = Trans
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
		model = Trans
		widgets = {
			'tdate': forms.DateInput(attrs={'format': 'yyyy-mm-dd','type':'date'}),
		}
		fields = "__all__"
		
	def __init__(self, *args, **kwargs):
			super(AddTransactionAll, self).__init__(*args, **kwargs)			

			# Filter active accounts and payees
			self.fields['account'].queryset = Account.objects.all()
			self.fields['payee'].queryset = Payee.objects.all()