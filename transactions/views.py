from django.shortcuts import (
	render,
	get_object_or_404,
	redirect,
	Http404,
)

from django.template import loader

from django.http import HttpResponse

from django.core.paginator import Paginator

from django.contrib import messages

from django.views.generic import (
	MonthArchiveView,
	YearArchiveView,
	DeleteView
)

from django.db.models import (
	F,
	Sum,
	Window,
)

from .forms import (
	AddTransaction,
	TransSubTransForm,
	TransForm,
	TransferForm,
	CreditCardPaymentForm,
	PaycheckForm,
	PaycheckItemsForm,
)

from transactions.models import (
	Transaction,
	SubTransaction,
	Paycheck,
	PaycheckItems,
)

from fin.models import (
    Payee,
    GroupedCat,
    Account,
)

from django.urls import (
	reverse_lazy,
	reverse
)

from datetime import datetime

from csv_importer.models import (
    Staged_Transaction,
)

### VIEW ALL TRANS ###

def transactions(request):
	transactions = Transaction.objects.all().order_by('tdate')
	template = loader.get_template('transactions.html')
	paginator = Paginator(transactions, 50)

	page_number = request.GET.get("page")
	page_obj = paginator.get_page(page_number)

	context = {"page_obj": page_obj}

	return HttpResponse(template.render(context, request))

### ARCHIVE VIEWS

class TransYearArchiveView(YearArchiveView):
	queryset = Transaction.objects.all()
	date_field = "tdate"
	make_object_list = True
	template_name = "transactions/trans_months.html"

class transactionMonthArchiveView(MonthArchiveView):

	queryset = Transaction.objects.all().annotate(cumsum=Window(Sum('subtransaction__amount'), order_by=(F('tdate').asc(), F('tid').asc())))

	date_field = "tdate"
	template_name = "transactions/trans_monthly.html"

### ADD TRANSACTION ###

def atran(request, dpay=None):

	context = {}

	lt=Transaction.objects.all().order_by("-tid").first().tid

	nt=lt+1

	if request.method == 'POST':
		form = AddTransaction(request.POST)

		if form.is_valid():
			form.save()
			lt=Transaction.objects.all().order_by("-tid").first().tid
			nt=lt+1
			la=Transaction.objects.all().order_by("-tid").first().account
			ld=Transaction.objects.all().order_by("-tid").first().tdate
			form = AddTransaction(initial={'tid': nt, 'account': la, 'tdate': ld })

	else:
		form = AddTransaction(initial={'tid': nt, 'payee': dpay })

	context['form'] = form

	return render(request, "add.html", context)

### TLIST ###

def tlist(request, acc='all', cat='all', gcat='all', pay='all', l1='all', ord='-tdate', mindate=None, maxdate=None, **kwargs):

	if maxdate == None:
		maxdate = datetime.today().strftime('%Y-%m-%d')

	filters = {}

	if acc != 'all':
		filters['account'] = acc

	if cat != 'all':
		filters['subtransaction__groupedcat__category'] = cat

	if gcat != 'all':
		filters['subtransaction__groupedcat'] = gcat

	if pay != 'all':
		filters['payee'] = pay

	if l1 != 'all':
		filters['subtransaction__groupedcat__l1group'] = l1

	if mindate is not None:
		filters['tdate__range'] = [mindate, maxdate]

	trans_query = Transaction.objects.all()

	if filters:
		trans_query = trans_query.filter(**filters)

	trans_query = trans_query.annotate(
		cumsum=Window(
			Sum('subtransaction__amount'),
			order_by=(F('tdate').asc(), F('tid').asc())
		)
	).order_by(ord, '-tid')

	tqcnt = trans_query.count()

	trans_list = list(trans_query)

	listCnt = len(trans_list)

	template = loader.get_template('transactions/tlist.html')

	paginator = Paginator(trans_list, 50)

	page_number = request.GET.get("page")

	page_obj = paginator.get_page(page_number)

	context = {
		"page_obj": page_obj,
		"acc": acc,
		"cat": cat,
		"gcat": gcat,
		"pay": pay,
		"l1": l1,
		"ord": ord,
		"listCnt": listCnt,
		"tqcnt": tqcnt
	}

	return HttpResponse(template.render(context, request))

### UPDATE TRANSACTION ###

def utran_act(response, t_id):

	tran = Transaction.objects.get(pk=t_id)

	form = AddTransaction(response.POST or None, instance=tran)

	next = response.POST.get('next', '/')

	if form.is_valid():
		form.save()

		return redirect(next)

	return render(response, 'update.html', {"tran": tran, 'form': form})

def utran(request, t_id):

	obj = Transaction.objects.get(pk=t_id)

	form = TransForm(request.POST or None, instance=obj)

	form2 = TransSubTransForm(request.POST or None)

	subtrans_forms = []

	for subtran_obj in obj.transsubtrans_set.all():
		subtrans_forms.append(
			TransSubTransForm(request.POST or None, instance=subtran_obj)
		)

	context = {
		'form': form,
		'subtrans_forms': subtrans_forms,
		'object': obj,
	}

	template = "transactions/update.html"

	next = request.POST.get('next', '/')

	my_forms = all([form.is_valid() for form in subtrans_forms])

	if my_forms and form.is_valid():
		parent = form.save()
		parent.save()
		for form2 in subtrans_forms:
			child = form2.save()
			child.trans = parent
			child.save()

		context['message'] = 'saved'

		return redirect(next)

	return render(request, template, context)


def Transaction_list_view(request):
	qs = Transaction.objects.all()
	template = "transactions/list.html"
	context = {
		"object_list": qs
	}
	return render(request, template, context)

def Transaction_detail_view(request, id=None):
	hx_url = reverse("transactions:hx-detail", kwargs={"id": id})

	template = "transactions/detail.html"

	context = {
		"hx_url": hx_url
	}

	return render(request, template, context)

def Transaction_detail_hx_view(request, id=None):
	try:
		obj = Transaction.objects.get(id=id)
	except:
		obj = None
	if obj is None:
		return HttpResponse("Not Found")
	template = "transactions/partials/detail.html"

	context = {
		"object": obj
	}

	return render(request, template, context)

def Transaction_delete_view(request, id=None):
	try:
		obj = Transaction.objects.get(id=id)
	except:
		obj = None

	if obj is None:
		if request.htmx:
			return HttpResponse("Not Found")
		raise Http404

	next = request.POST.get('next', '/')

	success_url = next

	template = "transactions/delete.html"

	if request.method == "POST":
		obj.delete()
		if request.htmx:
			headers = {
				'HX-Redirect': success_url
			}
			return HttpResponse("Deleted", headers=headers)
		return redirect(next)

	context = {
		"object": obj
	}

	return render(request, template, context)

def TransSubTrans_delete_view(request, parent_id=None, id=None):
	try:
		obj = SubTransaction.objects.get(id=id, trans_id=parent_id)
	except:
		obj = None

	if obj is None:
		if request.htmx:
			return HttpResponse("Not Found")
		raise Http404

	success_url = "/"

	template = "transactions/delete.html"

	if request.method == "POST":

		obj.delete()
		if request.htmx:
			headers = {
				'HX-Redirect': success_url
			}
			return HttpResponse("Deleted")
		return redirect(success_url)

	context = {
		"object": obj
	}

	return render(request, template, context)

def Transaction_create_view(request):

	lt=Transaction.objects.all().order_by("-tid").first().tid
	nt=lt+1

	ld=Transaction.objects.all().order_by("-tid").first().tdate

	la=Transaction.objects.all().order_by("-tid").first().account

	initial_values = {
		'tid': nt,
		'tdate': ld,
		'account': la,

    	}

	form = TransForm(request.POST or None, initial=initial_values)

	template = "transactions/create-update.html"

	context = {
		"form": form,
	}

	if form.is_valid():
		obj = form.save()
		obj.save()
		if request.htmx:
			headers = {
                "HX-Redirect": obj.get_edit_url()
			}
			return HttpResponse("Created", headers=headers)

		return redirect(obj.get_edit_url())

	return render(request, template, context)

def Transaction_update_view(request, id=None):
	obj = get_object_or_404(Transaction, id=id)
	aAct = obj.account.active
	pAct = obj.payee.active
	form = TransForm(request.POST or None, instance=obj, aAct=aAct, pAct=pAct)
	new_subtran_url = reverse('transactions:hx-subtran-create', kwargs={"parent_id": obj.id})
	template = "transactions/create-update.html"

	context = {
		"form": form,
		"object": obj,
		"new_subtran_url": new_subtran_url,
	}

	if form.is_valid():
		form.save()
		context['message'] = 'saved'

	if request.htmx:
		return render(request, "transactions/partials/forms.html", context)

	return render(request, template, context)

class TransDeleteView(DeleteView):
	model = Transaction
	success_url = reverse_lazy('main')
	template_name = "confirm_delete.html"


def Transaction_subtran_update_hx_view(request, parent_id=None, id=None):

	if not request.htmx:
		raise Http404

	try:
		parent_obj = Transaction.objects.get(id=parent_id)

	except:
		parent_obj = None

	if parent_obj is None:
		return HttpResponse("Not Found")

	instance = None
	if id is not None:
		try:
			instance = SubTransaction.objects.get(trans=parent_obj, id=id)

		except:
			instance = None

	if instance is not None:
	    form = TransSubTransForm(request.POST or None, instance=instance)
	else:
	    form = TransSubTransForm(request.POST or None, initial={'groupedcat': parent_obj.payee.def_gcat })

	url = instance.get_hx_edit_url() if instance else reverse('transactions:hx-subtran-create', kwargs={"parent_id": parent_obj.id})

	context = {
		"url": url,
		"form": form,
		"object": instance,
	}

	if form.is_valid():
		new_obj = form.save(commit=False)

		if instance is None:
			new_obj.trans = parent_obj
		new_obj.save()

		context['object'] = new_obj

		return render(request, "transactions/partials/subtran-inline.html", context)

	return render(request, "transactions/partials/subtran-form.html", context)

def Transfer_create_view(request):

    last_tid =Transaction.objects.all().order_by("-tid").first().tid

    current_tid = last_tid + 1

    last_tdate = Transaction.objects.all().order_by("-tid").first().tdate

    last_tacct =Transaction.objects.all().order_by("-tid").first().account

    initial_values = {
        'tid': current_tid,
		'tdate': last_tdate,
		'acct_out': last_tacct,
    }

    form = TransferForm(request.POST or None, initial=initial_values)

    template = "transactions/create-transfer.html"

    context = { "form": form, }

    if form.is_valid():
        payee_instance = get_object_or_404(Payee, pk=21)
        gc_instance = get_object_or_404(GroupedCat, pk=88)

        trans = Transaction.objects.create(
            tid = form.cleaned_data['tid'],
            tdate = form.cleaned_data['tdate'],
            account = form.cleaned_data['acct_out'],
            payee = payee_instance,
            match = form.cleaned_data['tid']+1
        )
        trans.save()
        sub_trans = SubTransaction.objects.create(
            trans = trans,
            amount = -1 * form.cleaned_data['tamt'],
            groupedcat = gc_instance
        )
        sub_trans.save()
        trans2 = Transaction.objects.create(
            tid = form.cleaned_data['tid']+1,
            tdate = form.cleaned_data['tdate'],
            account = form.cleaned_data['acct_in'],
            payee = payee_instance,
            match = form.cleaned_data['tid']
        )
        trans2.save()
        sub_trans2 = SubTransaction.objects.create(
            trans = trans2,
            amount = form.cleaned_data['tamt'],
            groupedcat = gc_instance
        )
        sub_trans2.save()

        messages.success(request, 'transfer successfully added')

        if request.htmx:
            return render(request, "transactions/partials/form.html", context)
        #return redirect('transactions:transfer')

    return render(request, template, context)

def CC_Pmt_create_view(request):

    last_tid =Transaction.objects.all().order_by("-tid").first().tid

    current_tid = last_tid + 1

    last_tdate = Transaction.objects.all().order_by("-tid").first().tdate

    def_tacct = get_object_or_404(Account, pk=24)

    initial_values = {
        'tid': current_tid,
		'tdate': last_tdate,
		'acct_out': def_tacct.id,
    }

    form = CreditCardPaymentForm(request.POST or None, initial=initial_values)

    template = "transactions/create-transfer.html"

    context = { "form": form, }

    if form.is_valid():
        payee_instance = get_object_or_404(Payee, pk=17)
        gc_instance = get_object_or_404(GroupedCat, pk=78)

        trans = Transaction.objects.create(
            tid = form.cleaned_data['tid'],
            tdate = form.cleaned_data['tdate'],
            account = form.cleaned_data['acct_out'],
            payee = payee_instance,
            match = form.cleaned_data['tid']+1
        )
        trans.save()
        sub_trans = SubTransaction.objects.create(
            trans = trans,
            amount = -1 * form.cleaned_data['tamt'],
            groupedcat = gc_instance
        )
        sub_trans.save()
        trans2 = Transaction.objects.create(
            tid = form.cleaned_data['tid']+1,
            tdate = form.cleaned_data['tdate'],
            account = form.cleaned_data['acct_in'],
            payee = payee_instance,
            match = form.cleaned_data['tid']
        )
        trans2.save()
        sub_trans2 = SubTransaction.objects.create(
            trans = trans2,
            amount = form.cleaned_data['tamt'],
            groupedcat = gc_instance
        )
        sub_trans2.save()

        messages.success(request, 'credit card payment successfully added')

        if request.htmx:
            return render(request, "transactions/partials/form.html", context)
        #return redirect('transactions:cc-pmt')

    return render(request, template, context)

def add_staged_trans(request, st):

    st = Staged_Transaction.objects.get(pk=st)

    #Create a new transaction
    lt=Transaction.objects.all().order_by("-tid").first().tid
    nt=lt+1

    trans = Transaction.objects.create(
        tid = nt,
        tdate = st.tdate,
        account= st.account,
        payee = st.imported_payee.payee
    )

    st_amt = st.amount * -1

    #Create a subtransaction
    strans = SubTransaction.objects.create(
        trans = trans,
	    groupedcat = st.imported_payee.payee.def_gcat,
	    amount = st_amt
    )

    st.imported = True
    st.save()

    rurl = '/csv/staged-transactions'+'?filter=False'

    return redirect(rurl)


def paycheck_list_view(request):
    qs = Paycheck.objects.all()
    context = {
        "object_list": qs
    }
    return render(request, "transactions/paycheck-list.html", context)

def paycheck_detail_view(request, id=None):
    obj = get_object_or_404(Paycheck, id=id)
    context = {
        "object": obj
    }
    return render(request, "transactions/paycheck-detail.html", context)

def paycheck_create_view(request):
    form = PaycheckForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        obj = form.save()
        return redirect(obj.get_absolute_url())
    return render(request, "transactions/paycheck-create-update.html", context)

def paycheck_update_view(request, id=None):
    obj = get_object_or_404(Paycheck, id=id)
    form = PaycheckForm(request.POST or None, instance=obj)
    new_item_url = reverse("transactions:paycheck_item_create_hx", kwargs={"parent_id": obj.id})
    context = {
        "form": form,
        "object": obj,
        "new_item_url": new_item_url,
    }
    if form.is_valid():
        form.save()
        context['message'] = "Data Saved."

    if request.htmx:
        return render(request, "transactions/partials/paycheck-form.html", context)

    return render(request, "transactions/paycheck-create-update.html", context)


def paycheck_item_update_hx_view(request, parent_id=None, id=None):

    #if the request is not an htmx request, it's unauthorized > end of view
    if not request.htmx:
        raise Http404

    #this block ensures that a parent object (the paycheck that the paycheck line items will be attached to exists. if it doesn't > end of view

    try:
        parent_obj = Paycheck.objects.get(id=parent_id)
    except:
        parent_obj = None
    if parent_obj is None:
        return HttpResponse("Not Found")

    #at this point, it has been confirmed that a parent_object exists

    #instance is set to "none" assuming that no instances exist
    instance = None

    #if an id has been passed to the view it means that an instance does exist and can be retrieved
    if id is not None:
        try:
            instance = PaycheckItems.objects.get(paycheck=parent_id, id=id)
        except:
            instance = None

    #this will return an empty form if a paycheck item that doesn't exist is passed to the view

    form = PaycheckItemsForm(request.POST or None, instance=instance)

    url = instance.get_hx_edit_url() if instance else reverse("transactions:paycheck_item_create_hx", kwargs={"parent_id": parent_obj.id})

    context = {
        "url": url,
        "form": form,
        "object": instance,
    }


    if form.is_valid():

        #the form is saved without committing in case there is no instance
        new_obj = form.save(commit=False)

        #if there is no instance, the paycheck is set to the parent_object
        if instance is None:
            new_obj.paycheck = parent_obj

        #then the form is saved with committing
        new_obj.save()
        context['i'] = new_obj
        return render(request, "transactions/partials/paycheck-item-inline.html", context)

    return render(request, "transactions/partials/paycheck-item-form.html", context)


def paycheck_item_del_view(request, parent_id=None, id=None):
    try:
        obj = PaycheckItems.objects.get(id=id, parent_id=parent_id)
    except:
        obj = None

    if obj is None:
        return HttpResponse("Not Found")

    success_url = reverse("transactions:paycheck-detail", kwargs={'parent_id': parent_id })

    template = "transactions/delete.html"

    if request.method == "POST":
        obj.delete()
        if request.htmx:
            headers = {
                'HX-Redirect': success_url
            }
            return HttpResponse("Deleted!")
        return redirect(success_url)

    context = {
        "object": object
    }

    return render(request, template, context)