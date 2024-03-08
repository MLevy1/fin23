from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
    Http404,
)

from django.urls import reverse

from django.http import HttpResponse

from .forms import (
    TaxReturnFrm,
    TaxReturnFormForm,
    TaxReturnFormLineForm,
    TaxReturnFormLineInputForm,
)

from .models import (
    Tax_Return,
)

def index(request):
    return HttpResponse("Ugh, Taxes.")

#TAX RETURNS

def TaxReturn_create_view(request):
    initial_values = {
        'year': 2023,
    }

    form = TaxReturnFrm(request.POST or None, initial=initial_values)

    template = "tax/create-update.html"

    context = {
		"form": form,
		"title": "New Tax Return",
    }

    if form.is_valid():
        obj = form.save()
        obj.save()
        if request.htmx:
            headers = {"HX-Redirect": obj.get_list_url()}
            return HttpResponse("Created", headers=headers)
        return redirect(obj.get_list_url())
    return render(request, template, context)

def TaxReturn_list_view(request):
    qs = Tax_Return.objects.all()

    template = "tax/list.html"

    new_url = reverse("tax:tax-return-create")

    context = {
        "object_list": qs,
        "title": "Tax Returns List",
        "new_url": new_url,
    }

    return render(request, template, context)

def TaxReturn_detail_view(request, id=None):

    obj = get_object_or_404(Tax_Return, id=id)

    new_item_url = reverse('tax:tax-return-form-list', kwargs={"parent_id": obj.id})

    template = "tax/detail.html"

    #partial = "tax/partials/inline.html"

    context = {
		"object": obj,
		"title": "View TaxReturn",
		"new_item_url": new_item_url,
	}

    #if request.htmx:
	    #return render(request, partial, context)

    return render(request, template, context)

def TaxReturn_update_view(request, id=None):
    obj = get_object_or_404(Tax_Return, id=id)

    form = TaxReturnFrm(request.POST or None, instance=obj)
    new_item_url = reverse('tax:tax-return-form-create', kwargs={"parent_id": obj.id})
    template = "tax/create-update.html"

    partial = "tax/partials/forms.html"

    context = {
		"form": form,
		"object": obj,
		"new_item_url": new_item_url,
		"title": "Update TaxReturn",
	}

    if form.is_valid():
	    form.save()
	    context['message'] = "saved"

	    if request.htmx:
	        return render(request, partial, context)

    return render(request, template, context)

def TaxReturn_delete_view(request, id=None):

    try:
        obj = Tax_Return.objects.get(id=id)
    except:
        obj = None

    if obj is None:
        if request.htmx:
            return HttpResponse("not found")
        raise Http404

    if request.method == "POST":
        obj.delete()
        success_url = reverse("tax:tax-return-list")

        if request.htmx:
            headers = {
                'HX-Redirect': success_url
            }
            return HttpResponse("deleted", headers=headers)
        return redirect(success_url)

    template = "tax/delete.html"

    context = {
        "object": obj
    }

    return render(request, template, context)

#FORM
#Requires a tax return to be selected

def TaxReturnForm_create_view(request, parent_id=None):

    if not request.htmx:
        raise Http404

    try:
        parent_obj = Tax_Return.objects.get(id=parent_id)
    except:
        parent_obj = None

    if parent_obj is None:
        return HttpResponse("Not Found")

    form = TaxReturnFormForm(request.POST or None)

    template = "tax/create-update.html"

    partial = "tax/partials/inline.html"

    context = {
		"form": form,
	}

    if form.is_valid():
	    new_obj = form.save(commit=False)
	    new_obj.tax_return = parent_obj
	    new_obj.save()

	    context['object'] = new_obj

	    return render(request, partial, context)

    return render(request, template, context)

def TaxReturnForm_list_view(request, parent_id=None):

    try:
        qs = TaxReturnFormForm.objects.filter(taxreturn=parent_id)
    except:
        qs = None

    if qs is None:
        if request.htmx:
            return HttpResponse("not found")
        raise Http404

    template = "tax/list.html"

    new_url = reverse("tax:tax-return-form-create")

    context = {
        "object_list": qs,
        "title": "Tax Return Forms List",
        "new_url": new_url,
    }

    return render(request, template, context)

def TaxReturnForm_update_view(request):
    return

def TaxReturnForm_delete_view(request):
    return


#FORM LINE


#TaxReturnOutboundFormLine(models.Model):
    #taxreturnoutboundform = models.ForeignKey(TaxReturnOutboundForm, on_delete=models.PROTECT, null=True, blank=True)
    #number = models.CharField(max_length=255, null=True, blank=True)
    #line = models.CharField(max_length=255, null=True, blank=True)
    #instructions = models.CharField(max_length=255, null=True, blank=True)

def TaxReturnFormLine_create_view(request):
    form = TaxReturnFormLineForm(request.POST or None)
    template = "tax/create-update.html"

    context = {
		"form": form,
	}
    return render(request, template, context)

def TaxReturnFormLine_update_view(request):
    return

def TaxReturnFormLine_delete_view(request):
    return

#FORM LINE INPUT

#class TaxReturnFormLineInput(models.Model):
    #taxreturnoutboundformline = models.ForeignKey(TaxReturnOutboundFormLine, on_delete=models.PROTECT, null=True, blank=True)
    #amount = models.DecimalField(verbose_name='Amount', max_digits=18, decimal_places=2, null=True, blank=True)

def TaxReturnFormLineInput_create_view(request):
    form = TaxReturnFormLineInputForm(request.POST or None)
    template = "tax/create-update.html"

    context = {
		"form": form,
	}
    return render(request, template, context)

def TaxReturnFormLineInput_update_view(request):
    return

def TaxReturnFormLineInput_delete_view(request):
    return
