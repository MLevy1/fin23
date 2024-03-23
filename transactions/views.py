from django.shortcuts import (
	render,
	get_object_or_404,
	redirect,
	Http404,
)

from django.template import loader

from django.http import HttpResponse

from django.core.paginator import Paginator

from django.views.generic import (
	MonthArchiveView,
	YearArchiveView,
)

from django.db.models import (
	F,
	Sum,
	Window,
	Avg,
	Min,
	Max,
)

from transactions.models import (
	Transaction,
	SubTransaction,
)

from fin.models import (
    Payee,
    GroupedCat,
    Account,
)

from fixed.models import (
    Flow,
)

from csv_importer.models import (
    Staged_Transaction,
)

from .forms import (
	TransForm,
	TransSubTransForm,
	TransferForm,
	FixedForm,
)

from django.urls import (
	reverse
)

from datetime import datetime

def get_last_acct():
	    last_acct = Transaction.objects.all().order_by("-tid").first().account.id
	    return last_acct

#T2
def Transaction_create_view(request):

	lt=Transaction.objects.all().order_by("-tid").first().tid

	nt=lt+1

	ld=Transaction.objects.all().order_by("-tid").first().tdate

	la = get_last_acct()

	initial_values = {
		'tid': nt,
		'tdate': ld,
		'account': la,

    	}

	form = TransForm(request.POST or None, initial=initial_values, aAct=True, pAct=True)

	template = "transactions/create-update.html"

	context = {
		"form": form,
		"last_acct": get_last_acct(),
		"title": "Add Transaction",
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

#T3
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

	a = trans_query.aggregate(Avg('subtransaction__amount'))
	s = trans_query.aggregate(Sum('subtransaction__amount'))
	mnd = trans_query.aggregate(Min('tdate'))
	mxd = trans_query.aggregate(Max('tdate'))
	mxd = mxd['tdate__max']
	mnd = mnd['tdate__min']
	dr = mxd-mnd
	pd = s['subtransaction__amount__sum'] / dr.days
	pw = pd*7
	py = pd*365
	pm =py/12


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
		"tqcnt": tqcnt,
		"a": a['subtransaction__amount__avg'],
		"s": s['subtransaction__amount__sum'],
		"dr": dr.days,
		"pd": pd,
		"pw": pw,
		"pm": pm,
		"py": py,

	}

	return HttpResponse(template.render(context, request))

#T4
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
		"last_acct": get_last_acct(),
		"title": "Update Transaction",
	}

	if form.is_valid():
		form.save()
		context['message'] = 'saved'

		if request.htmx:
		    return render(request, "transactions/partials/forms.html", context)

	return render(request, template, context)

#T5
def Transaction_delete_view(request, id=None):

    try:
        obj = Transaction.objects.get(id=id)
    except:
        obj = None

    if obj is None:
        if request.htmx:
            return HttpResponse("Not Found")
        raise Http404

    success_url = request.GET.get('next', '/')

    if request.method == "POST":

	    strans = obj.get_subtrans_children()

	    for s in strans:
	        s.delete()

	    obj.delete()

	    if request.htmx:
	        headers = {
				'HX-Redirect': success_url
			}

	        return HttpResponse("Deleted", headers=headers)

	    return redirect(success_url)

    template = "transactions/delete.html"

    context = {
		"object": obj
	}

    return render(request, template, context)

#T6
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

#T7
def TransSubTrans_delete_view(request, parent_id=None, id=None):
	try:
		obj = SubTransaction.objects.get(id=id, trans_id=parent_id)
	except:
		obj = None

	if obj is None:
		if request.htmx:
			return HttpResponse("Not Found")
		raise Http404

	if request.method == "POST":
		obj.delete()
		success_url = reverse("transactions:update", kwargs={'id': parent_id })

		if request.htmx:
			headers = {
				'HX-Redirect': success_url
			}
			return HttpResponse("Deleted", headers=headers)
		return redirect(success_url)

	template = "transactions/delete.html"

	context = {
		"object": obj
	}

	return render(request, template, context)

#T8
def Transfer_create_view(request):

    last_tid =Transaction.objects.all().order_by("-tid").first().tid

    current_tid = last_tid + 1

    last_tdate = Transaction.objects.all().order_by("-tid").first().tdate

    last_tacct = get_last_acct()

    initial_values = {
        'tid': current_tid,
		'tdate': last_tdate,
		'acct_out': last_tacct,
    }

    form = TransferForm(request.POST or None, initial=initial_values)

    template = "transactions/create-transfer.html"

    context = { "form": form, }

    if form.is_valid():
        cc = form.cleaned_data['cc']

        if cc is False:
            payee_instance = get_object_or_404(Payee, pk=21)
            gc_instance = get_object_or_404(GroupedCat, pk=88)
        else:
            payee_instance = get_object_or_404(Payee, pk=17)
            gc_instance = get_object_or_404(GroupedCat, pk=78)

        #get the account the money is being tranfserred into
        account_instance = get_object_or_404(Account, id=form.cleaned_data['acct_in'].id)

        #create the outbound transaction
        trans = Transaction.objects.create(
            tid = form.cleaned_data['tid'],
            tdate = form.cleaned_data['tdate'],
            account = form.cleaned_data['acct_out'],
            payee = payee_instance,
            match = form.cleaned_data['tid']+1
        )
        trans.save()

        #after the outbound transaction is created, sub-transaction data is added
        sub_trans = SubTransaction.objects.create(
            trans = trans,
            amount = -1 * form.cleaned_data['tamt'],
            groupedcat = gc_instance
        )
        sub_trans.save()

        #create the inbound transaction
        trans2 = Transaction.objects.create(
            tid = form.cleaned_data['tid']+1,
            tdate = form.cleaned_data['tdate'],
            account = form.cleaned_data['acct_in'],
            payee = payee_instance,
            match = form.cleaned_data['tid']
        )
        trans2.save()

        #add subtransaction details to inbound transaction
        sub_trans2 = SubTransaction.objects.create(
            trans = trans2,
            amount = form.cleaned_data['tamt'],
            groupedcat = gc_instance
        )
        sub_trans2.save()

        success_url = reverse("transactions:tlist", kwargs={"acc":  account_instance.id})

        if request.htmx:
            headers = {
    			'HX-Redirect': success_url
    		}
            return HttpResponse("Added", headers=headers)

        return redirect(success_url)

    return render(request, template, context)




#T10
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
    SubTransaction.objects.create(
        trans = trans,
	    groupedcat = st.imported_payee.payee.def_gcat,
	    amount = st_amt
    )

    st.imported = True
    st.save()

    rurl = '/csv/staged-transactions'+'?filter=False'

    return redirect(rurl)

#T11
def add_fixed(request, flow=None):

    flow_instance = get_object_or_404(Flow, id=flow)

    flow_items = flow_instance.get_flowitem_children()

    flow_payee_id = flow_instance.payee.id

    flow_account_id = flow_instance.account.id

    lt=Transaction.objects.all().order_by("-tid").first().tid

    nt=lt+1

    ld=Transaction.objects.all().order_by("-tid").first().tdate

    payee_instance = get_object_or_404(Payee, id=flow_payee_id)

    account_instance = get_object_or_404(Account, id=flow_account_id)

    initial_values = {
        'tid': nt,
		'tdate': ld,
		'pay': payee_instance.id,
		'acct': account_instance.id,
    }

    form = FixedForm(request.POST or None, initial=initial_values)

    template = "transactions/add-fixed.html"

    context = { "form": form, }

    if form.is_valid():

        trans = Transaction.objects.create(
            tid = form.cleaned_data['tid'],
            tdate = form.cleaned_data['tdate'],
            account = form.cleaned_data['acct'],
            payee = form.cleaned_data['pay'],
        )
        trans.save()

        for i in flow_items:

            gc_instance = get_object_or_404(GroupedCat, id=i.groupedcat.id)

            print(i.amount)
            print(gc_instance)

            sub_trans = SubTransaction.objects.create(
                trans = trans,
                amount = i.amount,
                groupedcat = gc_instance,
            )
            sub_trans.save()

        success_url = reverse("transactions:tlist", kwargs={"acc":  account_instance.id})

        if request.htmx:
            headers = {
    			'HX-Redirect': success_url
    		}
            return HttpResponse("Added", headers=headers)

        return redirect(success_url)

    return render(request, template, context)

#T12
class transactionMonthArchiveView(MonthArchiveView):
	queryset = Transaction.objects.all().annotate(cumsum=Window(Sum('subtransaction__amount'), order_by=(F('tdate').asc(), F('tid').asc())))
	date_field = "tdate"
	template_name = "transactions/trans_monthly.html"

#T13
class TransYearArchiveView(YearArchiveView):
	queryset = Transaction.objects.all()
	date_field = "tdate"
	make_object_list = True
	template_name = "transactions/trans_months.html"

#T14
def Transaction_detail_view(request, id=None):
	hx_url = reverse("transactions:hx-detail", kwargs={"id": id})

	template = "transactions/detail.html"

	context = {
		"hx_url": hx_url
	}

	return render(request, template, context)

