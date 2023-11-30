from django import forms

from .models import Recipe, RecipeIngredient

class RecipeForm(forms.ModelForm):
	
	required_css_class = 'required-field'
	error_css_class = 'error-field'
	#name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Recipe Name"}))
	#description = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}))
	class Meta:
		model = Recipe
		fields = ['name', 'description', 'directions']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		for field in self.fields:
			new_data = {
				"placeholder": f'Recipe {str(field)}',
				"class": 'form-control'
			}
			self.fields[str(field)].widget.attrs.update(
				new_data
			)
			
		self.fields['description'].widget.attrs.update({'rows': '2'})
		self.fields['directions'].widget.attrs.update({'rows': '3'})

class RecipeIngredientForm(forms.ModelForm):
	class Meta:
		model = RecipeIngredient
		fields = ['name', 'quantity', 'unit']