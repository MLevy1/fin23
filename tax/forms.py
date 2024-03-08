from django import forms

from .models import(
    Tax_Return,
    Tax_Return_Form,
    Tax_Return_Form_Line,
    Tax_Return_Form_Line_Input,
)

class TaxReturnFrm(forms.ModelForm):
	class Meta:
		model = Tax_Return
		fields = "__all__"

class TaxReturnFormForm(forms.ModelForm):
	class Meta:
		model = Tax_Return_Form
		fields = "__all__"

class TaxReturnFormLineForm(forms.ModelForm):
	class Meta:
		model = Tax_Return_Form_Line
		fields = "__all__"

class TaxReturnFormLineInputForm(forms.ModelForm):
	class Meta:
		model = Tax_Return_Form_Line_Input
		fields = "__all__"