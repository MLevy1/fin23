from django import forms

from .models import(
    Tax_Return,
    Tax_Return_Form,
    Tax_Return_Form_Line,
    Tax_Return_Form_Line_Input,
    InputValue,
    DataSource,
)

class FormTaxReturn(forms.ModelForm):
	class Meta:
		model = Tax_Return
		fields = "__all__"

class FormTaxReturnForm(forms.ModelForm):
	class Meta:
		model = Tax_Return_Form
		fields = "__all__"

class FormTaxReturnFormLine(forms.ModelForm):
	class Meta:
		model = Tax_Return_Form_Line
		fields = "__all__"

class FormTaxReturnFormLineInput(forms.ModelForm):
	class Meta:
		model = Tax_Return_Form_Line_Input
		fields = "__all__"

class FormInputValue(forms.ModelForm):
	class Meta:
		model = InputValue
		fields = "__all__"

class FormDataSource(forms.ModelForm):
	class Meta:
		model = DataSource
		fields = "__all__"