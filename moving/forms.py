from django import forms

class Moving(forms.Form):
	irate = forms.DecimalField(label="Interest Rate (APR)", decimal_places=3)
	term = forms.DecimalField(label="Mortgage Term (years)", decimal_places=0)
	ptaxrate = forms.DecimalField(label="PropertyTax Rate", decimal_places=3)
	annins = forms.DecimalField(label="Homeowners insurance (Annual)", decimal_places=2)
	purchprice = forms.DecimalField(label="Purchase Price", decimal_places=0)
	dppct = forms.DecimalField(label="Downpayment (pct)", decimal_places=0)