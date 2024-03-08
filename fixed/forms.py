from django import forms

from .models import (
	Flow,
	FlowItem,
)

class FlowForm(forms.ModelForm):
    class Meta:
        model = Flow
        fields = ['payee', 'account', 'desc', 'active']

class FlowItemForm(forms.ModelForm):
    class Meta:
        model = FlowItem
        fields = ['groupedcat', 'amount', 'note']

