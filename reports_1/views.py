from django.shortcuts import render

from .forms import TransListForm

from django.http import (
	HttpResponseRedirect,
)

from django.urls import (
	reverse_lazy,
)

# Create your views here.
def index(request):
    template="reports_1/main.html"
    return render(request, template)

def tform(request, act=True):

    form = TransListForm(request.POST, aAct=act, pAct=act)

    template="reports_1/form.html"

    context={
        "form": form,
        "title": "Transaction Query",
    }

    if request.method == "POST":

        if form.is_valid():

            kwargs = {"gcat": "all", "ord": "-tdate"}

            if form.cleaned_data['i_acct']:
                kwargs["acc"] = form.cleaned_data['i_acct'].id
            else:
                kwargs["acc"] = 'all'

            if form.cleaned_data['i_payee']:
                kwargs["pay"] = form.cleaned_data['i_payee'].id
            else:
                kwargs["pay"] = 'all'

            if form.cleaned_data['i_cat']:
                kwargs["cat"] = form.cleaned_data['i_cat'].id
            else:
                kwargs["cat"] = 'all'

            if form.cleaned_data['i_l1']:
                kwargs["l1"] = form.cleaned_data['i_l1'].id
            else:
                kwargs["l1"] = 'all'

            if form.cleaned_data['i_min_tdate']:
                kwargs["mindate"] = form.cleaned_data['i_min_tdate']

            if form.cleaned_data['i_max_tdate']:
                kwargs["maxdate"] = form.cleaned_data['i_max_tdate']

            template = 'transactions/tlist.html'

            return HttpResponseRedirect(reverse_lazy('transactions:tlist', kwargs=kwargs))

    return render(request, template, context)
