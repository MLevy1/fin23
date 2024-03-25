from django import forms

from django.forms.widgets import DateInput

from fin.models import (
    Account,
    Category,
    Payee,
    L1Group,
)

class TransListForm(forms.Form):
    i_payee = forms.ModelChoiceField(queryset=Payee.objects.all(), required=False, label="Payee")
    i_acct = forms.ModelChoiceField(queryset=Account.objects.all(), required=False, label="Account")
    i_cat = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, label="Category")
    i_l1 = forms.ModelChoiceField(queryset=L1Group.objects.all(), required=False, label="L1 Group")
    i_min_tdate = forms.DateField(required=False, label="Min Date", widget=DateInput(attrs={'format': 'yyyy-mm-dd', 'type': 'date'}))
    i_max_tdate = forms.DateField(required=False, label="Max Date", widget=DateInput(attrs={'format': 'yyyy-mm-dd', 'type': 'date'}))

    def __init__(self, *args, **kwargs):
        aAct = kwargs.pop("aAct", None)
        pAct = kwargs.pop("pAct", None)
        super(TransListForm, self).__init__(*args, **kwargs)

        for f in self.fields:
            new_data = {"class": "form-control"}
            self.fields [str(f)].widget.attrs.update(new_data)

        if aAct != "False":
            self.fields['i_acct'].queryset = Account.objects.filter(active="True")

        if pAct != "False":
            self.fields['i_payee'].queryset = Payee.objects.filter(active="True")

GROUP_CHOICES = (
    ("p", "Payee"),
    ("gc", "Grouped Category"),
    ("c", "Category"),
)

class TransSummaryForm(forms.Form):
    i_min_tdate = forms.DateField(required=False, label="Min Date", widget=DateInput(attrs={'format': 'yyyy-mm-dd', 'type': 'date'}))
    i_max_tdate = forms.DateField(required=False, label="Max Date", widget=DateInput(attrs={'format': 'yyyy-mm-dd', 'type': 'date'}))
    i_group = forms.ChoiceField(required=False, label="Group", choices=GROUP_CHOICES)
    i_active = forms.BooleanField(required=False, label="Active")
