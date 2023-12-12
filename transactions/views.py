from django.shortcuts import (
	render, 
	get_list_or_404,
	get_object_or_404,
	redirect,
	Http404,
)

from django.template import loader

from django.http import HttpResponse

from django.core.paginator import Paginator

from django.views.generic import (
	DetailView, 
	ListView, 
	MonthArchiveView, 
	YearArchiveView, 
	CreateView, 
	UpdateView, 
	DeleteView
)

from django.db.models import (
	F, 
	Sum, 
	Window, 
	Q, 	
	Avg, 
	Max, 
	Count
)

from django.forms.models import modelformset_factory

from .forms import (
	AddTransaction, 
	AddTransactionAll, 
	TransSubTransForm,
	TransForm,
)


from .models import (
	Transaction,
	SubTransaction
)

from fin.models import (
	GroupedCat,
)

from django.urls import (
	reverse_lazy, 
	reverse
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
	queryset = Transaction.objects.all().annotate(cumsum=Window(Sum('amount'), order_by=(F('tdate').asc(), F('tid').asc())))
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

def tlist(request, acc='all', cat='all', gcat='all', pay='all', ord='-tdate', gnull='y'):
  
	filters = {}

	if acc != 'all':
		filters['account'] = acc

	if cat != 'all':
		filters['category'] = cat
	
	if gcat != 'all':
		filters['groupedcat'] = gcat
	  
	if pay != 'all':
		filters['payee'] = pay
	
	if gnull != 'y':
		trans_query = Transaction.objects.all()
	else:
		trans_query = Transaction.objects.filter(subtransaction__groupedcat__isnull=True)

	if filters:
		trans_query = trans_query.filter(**filters)

	trans_query = trans_query.annotate(
		cumsum=Window(
			Sum('amount'),
			order_by=(F('tdate').asc(), F('tid').asc())
		)
	).order_by(ord, '-tid')

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
		"gnull": gnull, 
		"ord": ord,
		"listCnt": listCnt
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

	print(obj)

	if obj is None:
		if request.htmx:
			return HttpResponse("Not Found")
		raise Http404

	success_url = "/"

	template = "transactions/delete.html"

	if request.method == "POST":
		print("POST")
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
	form = TransForm(request.POST or None)
	context = {
		"form": form
	}
	template = "transactions/create-update.html"
	if form.is_valid():
		obj = form.save()
		obj.save()
		return redirect(obj.get_absoulte_url())
	return render(request, template, context)

def Transaction_update_view(request, id=None):
	obj = get_object_or_404(Transaction, id=id)
	
	form = TransForm(request.POST or None, instance=obj)
	
	new_subtran_url = reverse("transactions:hx-subtran-create", kwargs={"parent_id": obj.id })
	
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

	form = TransSubTransForm(request.POST or None, instance=instance)
	url = reverse("transactions:hx-subtran-create", kwargs={"parent_id": parent_obj.id })
	if instance:
		url = instance.get_hx_edit_url()
	context = {
		"url": url,
		"form": form,
		"object": instance
	}

	template = "transactions/partials/subtran-inline.html"
       
	if form.is_valid():
		new_obj = form.save()
		if instance is None:
			new_obj.trans = parent_obj
		new_obj.save()
		context['object'] = new_obj
		return render(request, template, context)

	return render(request, "transactions/partials/subtran-form.html", context)

def load_groupedcats(request, category_id=None):
	
	category_id = request.GET.get("category")
	if category_id:
		groupedcats = GroupedCat.objects.filter(l1group__aligned_category=category_id)
	else:
		groupedcats = GroupedCat.objects.all()
		

	template = "transactions/partials/groupedcat_options.html"
	context = { "groupedcats": groupedcats }

	return render(request, template, context)