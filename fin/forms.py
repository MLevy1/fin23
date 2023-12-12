from django import forms

from django.forms import ModelForm

from .models import (
	Account, 
	Category, 
	Payee, 
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
		super(PayeeGroupedCatUpdateAll, self).__init__(*args, **kwargs)
		for field in self.fields:
			new_data = {
				"class": 'form-control',
			}
			self.fields[str(field)].widget.attrs.update(
				new_data
			)
		
		self.fields['payee'].widget.attrs.update(
			{
				"hx-get": "/load-c",
				"hx-target": "#id_category",
				"hx-trigger": "change, load",
				"hx-swap": "innerHTML",
			}
		)

		self.fields['category'].widget.attrs.update(
			{
				"hx-get": "/load-gc",
				"hx-target": "#id_groupedcat",
				"hx-trigger": "change, load delay:500ms",
				"hx-swap": "innerHTML",
			}
		)

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

