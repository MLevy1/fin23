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

from .forms import (
	CategoryGroupedCatUpdateAll,
	PayeeGroupedCatUpdateAll,
	AddPayee,
	PayeeMergeForm,
	PayeeAccountUpdate,
	PayeeCategoryUpdateAll
)

from django.shortcuts import (
	render,
	redirect
)

from django.db.models import (
	Sum,
	Max,
	Count
)

from django.views.generic import (
	DetailView,
	ListView,
	CreateView,
	UpdateView,
	DeleteView
)

from transactions.models import (
	Transaction,
)

from django.utils import timezone

from datetime import datetime, timedelta
from django.forms import modelformset_factory
from django.urls import reverse_lazy

from django.core.paginator import Paginator

PayeeFormSet = modelformset_factory(Payee, form=AddPayee, extra=0)

def get_start_date():
	return datetime.now() - timedelta(days=1000)

#1
@login_required
def main(request):
	template = loader.get_template('main.html')
	return HttpResponse(template.render())

#++++++++++++
#  PAYEES
#++++++++++++

#13
@login_required
def payees(request, a='act', o='payee'):

	if a=="all":
		payees = Payee.objects.all().annotate(
	 		trans_count=Count('transaction'),
	 		total_transactions=Sum('transaction__subtransaction__amount'),
	 		most_recent_transaction=Max('transaction__tdate')
		).order_by(o)

	else:
		payees = Payee.objects.filter(active=True).annotate(
			trans_count=Count('transaction'), 	total_transactions=Sum('transaction__subtransaction__amount'),
			most_recent_transaction=Max('transaction__tdate')
    		).order_by(o)

	tcount = Payee.objects.all().count()
	template = 'payees.html'
	paginator = Paginator(payees, 25)

	page_number = request.GET.get("page")
	page_obj = paginator.get_page(page_number)

	context = {
		"page_obj": page_obj,
		"tcount": tcount,
	}

	return render(request, template, context)

### PAYEE SEARCH ###

#28
class SearchResultsView(ListView):
	model = Payee
	template_name = ('payees.html')
	context_object_name = "page_obj"

	def get_queryset(self):
		results = Payee.objects.filter(payee__contains=self.request.GET.get("q")).annotate(
			trans_count=Count('transaction'),
			total_transactions=Sum('transaction__subtransaction__amount'),
			most_recent_transaction=Max('transaction__tdate')
		)

		paginator = Paginator(results, 25)
		page_number = self.request.GET.get("page")
		page_obj = paginator.get_page(page_number)

		return page_obj

### PAYEE DETAIL ###

#24
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

#23
class PayeeCreateView(CreateView):
	model = Payee
	fields = "__all__"
	template_name = "add.html"

### UPDATE PAYEE ###

#25
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

#27
def make_inactive(request, pk):

	next = request.GET.get('next', '/')

	payee = Payee.objects.get(pk=pk)
	payee.active = False
	payee.save()
	return redirect(next)

### DELETE PAYEE ###

#26
class PayeeDeleteView(DeleteView):
	model = Payee
	success_url = reverse_lazy('list-payees', kwargs={"a": "act", "o": "payee"})
	template_name = "confirm_delete.html"

### MERGE 2 PAYEES ###

#14

@ login_required
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

#17

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


### UPDATE PAYEES GROUP CATEGORY ###

#10

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

### UPDATE CATEGORY'S GROUP CATEGORY ###

#11

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

#11

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

#2

def accounts(request, a='act'):

	if a=="all":
		accounts = Account.objects.all().annotate(
			balance=Sum('transaction__subtransaction__amount'),
			most_recent_transaction=Max('transaction__tdate')
		)
	else:
		accounts = Account.objects.filter(active=True).annotate(
			balance=Sum('transaction__subtransaction__amount'),
			most_recent_transaction=Max('transaction__tdate')
		)

	accounts = accounts.order_by('account')

	return render(request, "accounts.html", {'accounts': accounts})

### ADD ACCOUNT ###

#3

class AccountCreateView(CreateView):
	model = Account
	fields = "__all__"
	template_name = "add.html"

### UPDATE ACCOUNT ###

#4

class UpdateAccount(UpdateView):
	model = Account
	fields = "__all__"
	template_name = "update.html"
	success_url = reverse_lazy('list-accounts', kwargs={"a": "act"})

#+++++++++++++
#  CATEGORIES
#+++++++++++++

### VIEW CATEGORIES

#5

class CatListView(ListView):
	model = Category
	template_name = "categories.html"
	context_object_name = 'page_obj'

	def get_queryset(self):
		categories = Category.objects.all()
		data = []

		for c in categories:
			trans_count = Transaction.objects.filter(subtransaction__groupedcat__category=c).count() or 0

			trans_total = Transaction.objects.filter(subtransaction__groupedcat__category=c).aggregate(Sum('subtransaction__amount'))['subtransaction__amount__sum'] or 0

			if trans_count>0:
				data.append({
					'pk': c.pk,
					'active': c.active,
					'category': c,
					'trans_count': trans_count,
					'trans_total': trans_total,
				})

		paginator = Paginator(data, 25)
		page_number = self.request.GET.get("page")
		page_obj = paginator.get_page(page_number)

		return page_obj

	def get_context_data(self,**kwargs):

		nogcat = Transaction.objects.all()
		tcount = nogcat.count()

		context = super(CatListView,self).get_context_data(**kwargs)
		context['tcount'] = tcount

		print("no search context", context)

		return context

### SEARCH ###

#8

class CatSearchView(ListView):
	model = Category
	template_name = "categories.html"
	context_object_name = "page_obj"

	def get_queryset(self):
		results = Category.objects.filter(category__contains=self.request.GET.get("q"))
		data = []

		for c in results:

			trans_count = Transaction.objects.filter(subtransaction__groupedcat__category=c).count() or 0

			trans_total = Transaction.objects.filter(subtransaction__groupedcat__category=c).aggregate(Sum('subtransaction__amount'))['subtransaction__amount__sum'] or 0

			if trans_count>0:
				data.append({
					'pk': c.pk,
					'active': c.active,
					'category': c,
					'trans_count': trans_count,
					'trans_total': trans_total,
				})

		paginator = Paginator(data, 25)
		page_number = self.request.GET.get("page")
		page_obj = paginator.get_page(page_number)

		return page_obj

	def get_context_data(self,**kwargs):

		nogcat = Transaction.objects.all()
		tcount = nogcat.count()

		context = super(CatSearchView, self).get_context_data(**kwargs)
		context['tcount'] = tcount

		print("search context", context)

		return context



### ADD CATEGORY ###

#6

class CatCreateView(CreateView):
	model = Category
	fields = "__all__"
	template_name = "add.html"

### UPDATE CATEGORY ###

#7

class UpdateCategory(UpdateView):
	model = Category
	fields = "__all__"
	template_name = "update.html"
	success_url = reverse_lazy('list-categories')

### VIEW L1GROUPS

#9

class L1GroupListView(ListView):
	model = L1Group
	template_name = "l1groups.html"
	context_object_name = 'page_obj'

	def get_queryset(self):
		l1g = L1Group.objects.all()
		data = []

		for l in l1g:
			trans_count = Transaction.objects.filter(subtransaction__groupedcat__l1group=l.pk).count() or 0

			trans_total = Transaction.objects.filter(subtransaction__groupedcat__l1group=l.pk).aggregate(Sum('subtransaction__amount'))['subtransaction__amount__sum'] or 0

			if trans_count>0:
				data.append({
					'pk': l.pk,
					'active': l.active,
					'l1group': l,
					'trans_count': trans_count,
					'trans_total': trans_total,
				})

		paginator = Paginator(data, 25)
		page_number = self.request.GET.get("page")
		page_obj = paginator.get_page(page_number)

		return page_obj

	def get_context_data(self,**kwargs):

		nogcat = Transaction.objects.all()
		tcount = nogcat.count()

		context = super(L1GroupListView, self).get_context_data(**kwargs)
		context['tcount'] = tcount

		return context

### ADD L1 GROUP ###

#22

class L1GroupCreateView(CreateView):
	model = L1Group
	fields = "__all__"
	template_name = "add.html"

### UPDATE L1 GROUP ###

#15

class L1GroupUpdateView(UpdateView):
	model = L1Group
	fields = "__all__"
	template_name = "update.html"
	success_url = reverse_lazy('list-l1groups')

#19

class GroupedCatListView(ListView):
	model = GroupedCat
	template_name = "groupedcats.html"
	context_object_name = 'page_obj'

	def get_queryset(self):
		gcs = GroupedCat.objects.all()
		data = []

		for c in gcs:
			trans_count = Transaction.objects.filter(subtransaction__groupedcat=c.pk).count() or 0

			trans_total = Transaction.objects.filter(subtransaction__groupedcat=c.pk).aggregate(Sum('subtransaction__amount'))['subtransaction__amount__sum'] or 0

			if trans_count>0:
				data.append({
					'pk': c.pk,
					'groupedcat': c,
					'trans_count': trans_count,
					'trans_total': trans_total,
				})

		paginator = Paginator(data, 25)
		page_number = self.request.GET.get("page")
		page_obj = paginator.get_page(page_number)

		return page_obj

	def get_context_data(self,**kwargs):

		nogcat = Transaction.objects.all()
		tcount = nogcat.count()

		context = super(GroupedCatListView	,self).get_context_data(**kwargs)
		context['tcount'] = tcount

		return context

#22

class GroupedCatCreateView(CreateView):
	model = GroupedCat
	fields = "__all__"
	template_name = "add.html"

#20

class GroupedCatUpdateView(UpdateView):
	model = GroupedCat
	fields = "__all__"
	template_name = "update.html"
	success_url = reverse_lazy('list-gc')

#21

class GroupedCatDeleteView(DeleteView):
	model = GroupedCat
	success_url = reverse_lazy('list-gc')
	template_name = "confirm_delete.html"

#29

def load_c(request, payee_id=None):

	payee_id = request.GET.get("payee")

	if payee_id:
		cats =Category.objects.filter(transaction__payee=payee_id).distinct()
	else:
		cats = Category.objects.all()


	template = "c-options.html"

	context = { "cats": cats }

	return render(request, template, context)

#30

def load_gc(request, category_id=None):

	category_id = request.GET.get("category")

	groupedcats = GroupedCat.objects.all()

	template = "gc-options.html"

	context = { "groupedcats": groupedcats }

	return render(request, template, context)