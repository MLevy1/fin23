from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
    Http404,
)

from django.urls import reverse

from django.http import HttpResponse, HttpResponseRedirect

from .forms import (
    FormTaxReturn,
    FormTaxReturnForm,
    FormTaxReturnFormLine,
    FormTaxReturnFormLineInput,
    FormInputValue,
    FormDataSource,
)

from .models import (
    Tax_Return,
    Tax_Return_Form,
    Tax_Return_Form_Line,
    Tax_Return_Form_Line_Input,
    InputValue,
    DataSource,
)

def index(request):
    return HttpResponse("Ugh, Taxes.")

#TAX RETURNS

def get_test():
    test=6
    return test

def TaxReturn_create_view(request):

    form = FormTaxReturn(request.POST or None)

    template = "tax/tax_return_create-update.html"

    context = {
        "form": form,
        "title": "Create Tax Return",
    }

    if form.is_valid():
        obj = form.save()
        obj.save()
        return redirect(obj)

    return render(request, template, context)

def TaxReturn_list_view(request):

    qs = Tax_Return.objects.all()

    template = "tax/list.html"

    context = {

        "qs": qs,
        "title": "Tax Return List",

    }
    return render(request, template, context)

def TaxReturn_detail_view(request, id=id):

    obj = get_object_or_404(Tax_Return, id=id)

    template = "tax/tax_return_detail.html"

    context = {

        "object": obj,
        "title": "Tax Return Detail",

    }

    return render(request, template, context)

def TaxReturn_update_view(request, id=None):

    obj = get_object_or_404(Tax_Return, id=id)

    form = FormTaxReturn(request.POST or None, instance=obj)

    template = "tax/create-update.html"

    context = {
        "form": form,
        "title": "Update Tax Return",
    }

    if form.is_valid():
        obj = form.save()
        obj.save()
        return HttpResponseRedirect(reverse('tax:tax-return-list'))

    return render(request, template, context)

def TaxReturn_delete_view(request, id=None):

    obj = get_object_or_404(Tax_Return, id=id)

    obj.delete()

    return redirect(obj)

#FORM
#Requires a tax return to be selected

def TaxReturnForm_create_view(request, p_id=None):

    initial_values = {

	    'tax_return': p_id,

    }

    form = FormTaxReturnForm(request.POST or None, initial=initial_values)

    template = "tax/tax_return_form_create-update.html"

    context = {
        "form": form,
        "title": "Create Tax Return Form",
        "p_id": p_id,
    }

    if form.is_valid():
        obj = form.save()
        obj.save()
        return redirect(obj)

    return render(request, template, context)

def TaxReturnForm_detail_view(request, id=None):

    obj = get_object_or_404(Tax_Return_Form, id=id)

    template="tax/tax_return_form_detail.html"

    context = {

        "object": obj,
        "title": "Tax Return Form Detail",

    }

    return render(request, template, context)

def TaxReturnForm_update_view(request, id=None):

    obj = get_object_or_404(Tax_Return_Form, id=id)

    form = FormTaxReturnForm(request.POST or None, instance=obj)

    template = "tax/create-update.html"

    context = {
        "form": form,
        "title": "Update Tax Return Form",
    }

    if form.is_valid():
        obj = form.save()
        obj.save()
        return redirect(obj)

    return render(request, template, context)

def TaxReturnForm_delete_view(request, id=None):

    obj = get_object_or_404(Tax_Return_Form, id=id)

    obj.delete()

    return redirect(obj)

#FORM LINE
#Form needs to be selected

def TaxReturnFormLine_create_view(request, p_id=None):

    initial_values = {

	    'tax_return_form': p_id,

    }

    form = FormTaxReturnFormLine(request.POST or None, initial=initial_values)

    template = "tax/tax_return_form_line_create-update.html"

    context = {
        "form": form,
        "title": "Create Tax Return Form Line",
        "p_id": p_id,
    }

    if form.is_valid():
        obj = form.save()
        obj.save()
        return redirect(obj)

    return render(request, template, context)

def TaxReturnFormLine_detail_view(request, id=None):

    obj = get_object_or_404(Tax_Return_Form_Line, id=id)

    template = "tax/tax_return_form_line_detail.html"

    context = {

        "object": obj,
        "title": "Tax Return Form Line Detail",

    }

    return render(request, template, context)

def TaxReturnFormLine_update_view(request, id=None):

    obj = get_object_or_404(Tax_Return_Form_Line, id=id)

    form = FormTaxReturnFormLine(request.POST or None, instance=obj)

    template = "tax/create-update.html"

    context = {
        "form": form,
        "title": "Update Tax Return Form Line",
    }

    if form.is_valid():
        obj = form.save()
        obj.save()
        return redirect(obj)

    return render(request, template, context)

def TaxReturnFormLine_delete_view(request, id=None):

    obj = get_object_or_404(Tax_Return_Form_Line, id=id)

    obj.delete()

    return redirect(obj)

#FORM LINE INPUT

#Form line needs to be selected

def TaxReturnFormLineInput_create_view(request, p_id=None):

    initial_values = {

	    'tax_return_form_line': p_id,

    }

    form = FormTaxReturnFormLineInput(request.POST or None, initial=initial_values)

    template = "tax/tax_return_form_line_input_create-update.html"

    context = {
        "form": form,
        "title": "Create Tax Return Form Line Input",
        "p_id": p_id,
    }

    if form.is_valid():
        obj = form.save()
        obj.save()
        return redirect(obj)

    return render(request, template, context)

def TaxReturnFormLineInput_update_view(request, id=None):

    obj = get_object_or_404(Tax_Return_Form_Line_Input, id=id)

    form = FormTaxReturnFormLineInput(request.POST or None, instance=obj)

    template = "tax/create-update.html"

    context = {
        "form": form,
        "title": "Update Tax Return Form Line Input",
    }

    if form.is_valid():
        obj = form.save()
        obj.save()
        return redirect(obj)

    return render(request, template, context)

def TaxReturnFormLineInput_delete_view(request, id=None):

    obj = get_object_or_404(Tax_Return_Form_Line_Input, id=id)

    obj.delete()

    return redirect(obj)

#INPUT VALUE

def InputValue_create_view(request, p_id=None):

    initial_values = {

	    'datasource': p_id,

    }

    form = FormInputValue(request.POST or None, initial=initial_values)


    template = "tax/inputvalue_create-update.html"

    context = {
        "form": form,
        "title": "Create Input Value",
        "p_id": p_id,
    }

    if form.is_valid():
        obj = form.save()
        obj.save()
        return redirect(obj)

    return render(request, template, context)

def InputValue_update_view(request, id=None):

    obj = get_object_or_404(InputValue, id=id)

    form = FormInputValue(request.POST or None, instance=obj)

    template = "tax/inputvalue_create-update.html"

    context = {
        "form": form,
        "title": "Update Input Value",
    }

    if form.is_valid():
        obj = form.save()
        obj.save()
        return redirect(obj)

    return render(request, template, context)

def InputValue_delete_view(request, id=None):

    obj = get_object_or_404(InputValue, id=id)

    obj.delete()

    return redirect(obj)

#DATA SOURCE

def DataSource_list_view(request):

    qs = DataSource.objects.all()

    template = "tax/datasource_list.html"

    context = {

        "qs": qs,
        "title": "Data Source List"

    }
    return render(request, template, context)

def DataSource_create_view(request):

    form = FormDataSource(request.POST or None)

    template = "tax/datasource_create-update.html"

    context = {
        "form": form,
        "title": "Create Data Source",
    }

    if form.is_valid():
        obj = form.save()
        obj.save()
        return redirect(obj)

    return render(request, template, context)

def DataSource_detail_view(request, id=None):

    obj = get_object_or_404(DataSource, id=id)

    template = "tax/datasource_detail.html"

    context = {

        "object": obj,
        "title": "Data Source Detail",

    }

    return render(request, template, context)


def DataSource_update_view(request, id=None):

    obj = get_object_or_404(DataSource, id=id)

    form = FormDataSource(request.POST or None, instance=obj)

    template = "tax/datasource_create-update.html"

    context = {
        "form": form,
        "title": "Update Data Source",
    }

    if form.is_valid():
        obj = form.save()
        obj.save()
        return redirect(obj)

    return render(request, template, context)

def DataSource_delete_view(request, id=None):

    obj = get_object_or_404(DataSource, id=id)

    obj.delete()

    return redirect(obj)
