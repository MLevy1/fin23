from django.contrib.auth.decorators import login_required

from django.http import HttpResponse

from django.template import loader

from .models import (
	Category, 
	Payee, 
	Account, 
	L1Group, 
	GroupedCat
)

from projections.models import BudgetedItem

from .forms import (
	CategoryGroupedCatUpdateAll, 		
	PayeeGroupedCatUpdateAll, 
	AddPayee, 
	PayeeMergeForm, 
	PayeeCategoryUpdate, 
	PayeeAccountUpdate, 
	PayeeCategoryUpdateAll
)

from django.shortcuts import (
	render, 
	get_list_or_404, 
	redirect
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

from django.views.generic import (
	DetailView, 
	ListView, 
	MonthArchiveView, 
	YearArchiveView, 
	CreateView, 
	UpdateView, 
	DeleteView
)

from transactions.models import (
       Transaction,
       SubTransaction,
)

from django.utils import timezone

from django.apps import apps

from datetime import datetime, timedelta
from django.forms import modelformset_factory
from django.urls import reverse_lazy

from django.core.paginator import Paginator

PayeeFormSet = modelformset_factory(Payee, form=AddPayee, extra=0)

def get_start_date():
	return datetime.now() - timedelta(days=1000)

@login_required
def main(request):
	template = loader.get_template('main.html')
	return HttpResponse(template.render())

#++++++++++++
#  PAYEES
#++++++++++++

def payees(request, a='act', o='payee'):

	if a=="all":
		payees = Payee.objects.all().annotate(
	 		trans_count=Count('transaction', filter=Q(transaction__subtransaction__groupedcat__isnull=True)),
	 		total_transactions=Sum('transaction__subtransaction__amount'),
	 		most_recent_transaction=Max('transaction__tdate')
		).order_by(o)

	else:
		payees = Payee.objects.filter(active=True).annotate(
			trans_count=Count('transaction', filter=Q(transaction__subtransaction__groupedcat__isnull=True)),
			total_transactions=Sum('transaction__subtransaction__amount'),
			most_recent_transaction=Max('transaction__tdate')
    		).order_by(o)

	nogcat = Transaction.objects.filter(subtransaction__groupedcat__isnull=True)
	
	tcount = nogcat.count()
	template = 'payees.html'
	paginator = Paginator(payees, 25)

	page_number = request.GET.get("page")
	page_obj = paginator.get_page(page_number)

	context = {
		"page_obj": page_obj,
		"tcount": tcount, 
		"nogcat": nogcat 
	}

	return render(request, template, context)

### SEARCH ###

class SearchResultsView(ListView):
	model = Payee
	template_name = ('payees.html')
	context_object_name = "page_obj"

	def get_queryset(self):
		results = Payee.objects.filter(payee__contains=self.request.GET.get("q")).annotate(
			trans_count=Count('trans'),
			total_transactions=Sum('trans__amount'),
			most_recent_transaction=Max('trans__tdate')
		)
	 
		paginator = Paginator(results, 25)
		page_number = self.request.GET.get("page")
		page_obj = paginator.get_page(page_number)

		return page_obj

### PAYEE DETAIL ###

class PayeeDetailView(DetailView):
	model = Payee
	template_name = "detail.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		next = self.request.GET.get("next")
		dcat = self.request.GET.get("dcat")
		context["now"] = timezone.now()
		context["next"] = next
		context["dcat"] = dcat
		return context
  
### ADD PAYEE ###

class PayeeCreateView(CreateView):
	model = Payee
	fields = "__all__"
	template_name = "add.html"

### UPDATE PAYEE ###

class UpdatePayee(UpdateView):
	model = Payee
	fields = "__all__"
	template_name = "update.html"

	def get_success_url(self):
		next = self.request.GET.get("next")

		if next:

			return next
		
		return reverse_lazy('list-payees', kwargs={"a": "act", "o": "payee"})
	
### INACTIVATE PAYEE ###

def make_inactive(request, pk):
	payee = Payee.objects.get(pk=pk)
	payee.active = False
	payee.save()
	return redirect('/pay/act')

### DELETE PAYEE ###

class PayeeDeleteView(DeleteView):
	model = Payee
	success_url = reverse_lazy('payees', kwargs={"a": "act", "o": "payee"})
	template_name = "confirm_delete.html"

### MERGE 2 PAYEES ###
@login_required
def merge_payees(request, dpay=None):

	next = request.GET.get('next', '/')

	if request.method == 'POST':
		form = PayeeMergeForm(request.POST)
		
		if form.is_valid():
			source_payee = form.cleaned_data['source_payee']
			target_payee = form.cleaned_data['target_payee']

			# Update transactions with the target payee to use the source payee
			Transaction.objects.filter(payee=target_payee).update(payee=source_payee)

			# Delete the target payee
			target_payee.delete()

			return redirect(next) 

	else:
		form = PayeeMergeForm(initial={'target_payee': dpay })

	return render(request, 'merge_payees.html', {'form': form  })

### UPDATE PAYEES CATEGORY ###

def payee_category_update_all(request, dpay=None):

	if request.method == 'POST':
		form = PayeeCategoryUpdateAll(request.POST or None)
		
		next = request.POST.get('next', '/')

		if form.is_valid():
			source_payee = form.cleaned_data['source_payee']
			target_category = form.cleaned_data['target_category']

			qs = Transaction.objects.filter(payee=source_payee)
			
			for t in qs:
				t.get_subtrans_children().update(category=target_category)
				
			return redirect(next)
  
	else:
		
		form = PayeeCategoryUpdateAll(initial={'source_payee': dpay})
	context = {
		
			"form": form,

	}

	return render(request, 'qupdate.html', context)
	
#active only#

def payee_category_update(request):
	if request.method == 'POST':
		form = PayeeCategoryUpdate(request.POST)

		if form.is_valid():
			source_payee = form.cleaned_data['source_payee']
			target_category = form.cleaned_data['target_category']
			Transaction.objects.filter(payee=source_payee).update(category=target_category)

			return redirect('/qupdate/') # Redirect placholder
  
	else:
		form = PayeeCategoryUpdate()

	return render(request, 'qupdate.html', {'form': form  })

### UPDATE PAYEES GROUP CATEGORY ###

def payee_groupedcat_update_all(request, dpay=None, dcat=None):

	dcat = request.GET.get('dcat')
	
	if dcat is None and dpay is not None:
		pass
	
	template = 'gc_payee.html'

	if request.method == 'POST':
		form = PayeeGroupedCatUpdateAll(request.POST)

		next = request.POST.get('next', '/')

		if form.is_valid():
			payee = form.cleaned_data['payee']
			category = form.cleaned_data['category']
			groupedcat = form.cleaned_data['groupedcat']

			qs = Transaction.objects.filter(payee=payee)

			for t in qs:
				t.get_subtrans_children().filter(category=category).filter(groupedcat__isnull=True or groupedcat is None).update(groupedcat = groupedcat)

			return redirect(next)
  
	else:
		
		form = PayeeGroupedCatUpdateAll(initial={'payee': dpay, 'category': dcat })


	context = {
		'form': form,
		'payee': dpay, 
		'category': dcat,
	}

	return render(request, template, context)

def load_c(request, payee_id=None):
	
	payee_id = request.GET.get("payee")

	if payee_id:
		cats =Category.objects.filter(transaction__payee=payee_id).distinct()
	else:
		cats = Category.objects.all()
		

	template = "c-options.html"

	context = { "cats": cats }

	return render(request, template, context)


def load_gc(request, category_id=None):
	
	category_id = request.GET.get("category")

	if category_id:
		groupedcats = GroupedCat.objects.filter(l1group__aligned_category=category_id)
	else:
		groupedcats = GroupedCat.objects.all()
		

	template = "gc-options.html"

	context = { "groupedcats": groupedcats }

	return render(request, template, context)


### UPDATE CATEGORY'S GROUP CATEGORY ###

def category_groupedcat_update_all(request, dcat=None):

	dcat = request.GET.get('dcat')

	if request.method == 'POST':
		form = CategoryGroupedCatUpdateAll(request.POST)

		if form.is_valid():
			category = form.cleaned_data['category']
			groupedcat = form.cleaned_data['groupedcat']
			Transaction.objects.filter(category=category).filter(groupedcat__isnull=True).update(groupedcat=groupedcat)

			return redirect(reverse_lazy('list-categories'))
  
	else:
		form = CategoryGroupedCatUpdateAll(initial={'category': dcat })


	return render(request, 'qupdate.html', {'form': form  })


### UPDATE PAYEES ACCOUNT ###

def payee_account_update(request):
	if request.method == 'POST':
		form = PayeeAccountUpdate(request.POST)

		if form.is_valid():
			source_payee = form.cleaned_data['source_payee']
			target_account = form.cleaned_data['target_account']
			Transaction.objects.filter(payee=source_payee).update(account=target_account)

			return redirect('/qupdate/') # Redirect placholder
  
	else:
		form = PayeeAccountUpdate()

	return render(request, 'qupdate.html', {'form': form  })


#++++++++++++
#  ACCOUNTS
#++++++++++++

### VIEW ACCOUNTS ###

# not using generic view yet because of the need to filter and annotate #

def accounts(request, a='act'):

	if a=="all":
		accounts = Account.objects.all().annotate(
			balance=Sum('trans__amount'),
			most_recent_transaction=Max('trans__tdate')
		)
	else:
		accounts = Account.objects.filter(active=True).annotate(
			balance=Sum('trans__amount'),
			most_recent_transaction=Max('trans__tdate')
		)

	return render(request, "accounts.html", {'accounts': accounts})

### ADD ACCOUNT ###

class AccountCreateView(CreateView):
	model = Account
	fields = "__all__"
	template_name = "add.html"

### UPDATE ACCOUNT ###

class UpdateAccount(UpdateView):
	model = Account
	fields = "__all__"
	template_name = "update.html"
	success_url = reverse_lazy('accounts', kwargs={"a": "act"})

#+++++++++++++
#  CATEGORIES
#+++++++++++++

### SEARCH ###

class CatSearchView(ListView):
	model = Category
	template_name = ('categories.html')
	context_object_name = "page_obj"

	def get_queryset(self):
		
		results = Category.objects.filter(category__contains=self.request.GET.get("q")).annotate(
			trans_count=Count('trans'),
			total_transactions=Sum('trans__amount'),
			most_recent_transaction=Max('trans__tdate')
		)

		paginator = Paginator(results, 25)
		page_number = self.request.GET.get("page")
		page_obj = paginator.get_page(page_number)

		return page_obj


### VIEW CATEGORIES

class CatListView(ListView):
	model = Category
	template_name = "categories.html"
	context_object_name = 'page_obj'

	def get_queryset(self):
		categories = Category.objects.all()
		data = []

		start_date = get_start_date()

		ann_actual = 0
		ann_budget = 0

		ann_actual = float(ann_actual)
		ann_budget = float(ann_budget)

		for c in categories:
			trans_count = Transaction.objects.filter(category=c, subtransaction__groupedcat__isnull=True).count() or 0
			
			trans_total = Transaction.objects.filter(category=c, tdate__gte=start_date).aggregate(Sum('amount'))['amount__sum'] or 0
			
			ann_total = float(trans_total) * 365/1000
			
			ann_total = float(ann_total)
			
			budget_items = BudgetedItem.objects.filter(itemCat=c)
			
			budget_total = sum(item.annualAmt() for item in budget_items)
			
			budget_total = float(budget_total)

			if c.active != False:
				ann_actual += ann_total
				ann_budget += budget_total
				
			if trans_count>0:
				data.append({
					'pk': c.pk,
					'active': c.active,
					'category': c,
					'trans_count': trans_count,
					'trans_total': trans_total,
					'ann_total': ann_total,
					'budget_total': budget_total,
					'test_ann_act': ann_actual,
					'test_ann_bud': ann_budget,
				})

		surplus = ann_budget - ann_actual

		data.append({
			'ann_actual': ann_actual,
			'ann_budget': ann_budget,
			'surplus': surplus,
		})
		
		paginator = Paginator(data, 25)
		page_number = self.request.GET.get("page")
		page_obj = paginator.get_page(page_number)

		return page_obj

	def get_context_data(self,**kwargs):
		
		nogcat = Transaction.objects.filter(subtransaction__groupedcat__isnull=True)
		tcount = nogcat.count()
		
		context = super(CatListView,self).get_context_data(**kwargs)
		context['tcount'] = tcount
		context['nogcat'] = nogcat
		return context
	

### ADD CATEGORY ###

class CatCreateView(CreateView):
	model = Category
	fields = "__all__"
	template_name = "add.html"

### UPDATE CATEGORY ###

class UpdateCategory(UpdateView):
	model = Category
	fields = "__all__"
	template_name = "update.html"
	success_url = reverse_lazy('list-categories')

### VIEW L1GROUPS

class L1GroupListView(ListView):
	model = L1Group
	template_name = "l1groups.html"

### ADD L1 GROUP ###
class L1GroupCreateView(CreateView):
	model = L1Group
	fields = "__all__"
	template_name = "add.html"

### UPDATE L1 GROUP ###

class L1GroupUpdateView(UpdateView):
	model = L1Group
	fields = "__all__"
	template_name = "update.html"
	success_url = reverse_lazy('list-l1groups')

class GroupedCatListView(ListView):
	model = GroupedCat
	template_name = "groupedcats.html"
		

class GroupedCatCreateView(CreateView):
	model = GroupedCat
	fields = "__all__"
	template_name = "add.html"
	
class GroupedCatUpdateView(UpdateView):
	model = GroupedCat
	fields = "__all__"
	template_name = "update.html"
	success_url = reverse_lazy('list-gc')
	
class GroupedCatDeleteView(DeleteView):
	model = GroupedCat
	success_url = reverse_lazy('list-gc')
	template_name = "confirm_delete.html"