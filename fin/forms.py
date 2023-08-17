from django import forms
from django.forms import ModelForm
from .models import Issue, Account, Category, Payee, Trans
from django.contrib.admin.widgets import AdminDateWidget

class PayeeMergeForm(forms.Form):
    source_payee = forms.ModelChoiceField(queryset=Payee.objects.filter(active=True))
    target_payee = forms.ModelChoiceField(queryset=Payee.objects.all())

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


class AddTransaction(ModelForm):
	class Meta:
		model = Trans
		widgets = {
			'tdate': forms.DateInput(attrs={'format': 'yyyy-mm-dd','type':'date'}),
		}
		fields = "__all__"


class AddIssue(ModelForm):
	class Meta:
		model = Issue
		widgets = {
			'closedate': forms.DateInput(attrs={'format': 'yyyy-mm-dd h:m:s','type':'date'})
		}
		fields = "__all__"
		
class Moving(forms.Form):
	irate = forms.DecimalField(label="Interest Rate (APR)", decimal_places=3)
	term = forms.DecimalField(label="Mortgage Term (years)", decimal_places=0)
	ptaxrate = forms.DecimalField(label="PropertyTax Rate", decimal_places=3)
	annins = forms.DecimalField(label="Homeowners insurance (Annual)", decimal_places=2)
	purchprice = forms.DecimalField(label="Purchase Price", decimal_places=0)
	dppct = forms.DecimalField(label="Downpayment (pct)", decimal_places=0)
	
class Budget(forms.Form):
	a_gross_pay = forms.DecimalField(label="Annual Gross Salary", decimal_places=2)
	a_gross_bonus = forms.DecimalField(label="Annual Gross Bonus", decimal_places=2)
	a_al_taxable = forms.DecimalField(label="Alyssa Taxable Salary", decimal_places=2)
	a_al_fwh = forms.DecimalField(label="Alyssa Federal Withholding", decimal_places=2)
	a_al_swh = forms.DecimalField(label="Alyssa State Withholding", decimal_places=2)
	bw_medical = forms.DecimalField(label="Medical", decimal_places=2)
	bw_dental = forms.DecimalField(label="Dental", decimal_places=2)
	bw_daycare  = forms.DecimalField(label="Daycare", decimal_places=2)
	rate_sstax  = forms.DecimalField(label="Social Security Tax Rate", decimal_places=2) 
	rate_medicare  = forms.DecimalField(label="Medicare Tax Rate", decimal_places=2)
	rate_401k  = forms.DecimalField(label="401k Contribution Pct", decimal_places=2)
	w_train = forms.DecimalField(label="NJ Transit (Weekly)", decimal_places=2)
	rate_r401k = forms.DecimalField(label="Roth 401k Contribution Pct", decimal_places=2)
	bw_arag = forms.DecimalField(label="Legal", decimal_places=2)
	m_internet = forms.DecimalField(label="Internet", decimal_places=2)
	m_phone = forms.DecimalField(label="Phone", decimal_places=2)
	m_electric = forms.DecimalField(label="Electric", decimal_places=2)
	m_natgas = forms.DecimalField(label="Gas", decimal_places=2)
	a_carins = forms.DecimalField(label="Car Insurance (Annual)", decimal_places=2)
	m_homeins = forms.DecimalField(label="Homeowners Insurance (Monthly)", decimal_places=2)
	m_apple = forms.DecimalField(label="Apple", decimal_places=2)
	m_cabin_mtg = forms.DecimalField(label="Cabin Mortgage", decimal_places=2)
	a_cabin_ptax = forms.DecimalField(label="Cabin Property Tax", decimal_places=2)
	a_cabin_ins = forms.DecimalField(label="Cabin Homeowners Insurance", decimal_places=2)
	m_cabin_electric = forms.DecimalField(label="Cabin Electric", decimal_places=2)
	m_cabin_cable = forms.DecimalField(label="Cabin Cable", decimal_places=2)
	a_cabin_hoa = forms.DecimalField(label="Cabin HOA (Annual)", decimal_places=2)
	m_car = forms.DecimalField(label="Car Payment", decimal_places=2)
	m_mtg = forms.DecimalField(label="Home Mortgage", decimal_places=2)
	a_ptax = forms.DecimalField(label="Home Property Tax", decimal_places=2)