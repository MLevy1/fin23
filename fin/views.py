from .models import (
	Category,
	Payee,
	Account,
	L1Group,
	GroupedCat
)

from .forms import (
	AddPayee,
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
	SubTransaction,
)

from django.utils import timezone

from datetime import datetime, timedelta
from django.forms import modelformset_factory
from django.urls import reverse_lazy

from django.core.paginator import Paginator

PayeeFormSet = modelformset_factory(Payee, form=AddPayee, extra=0)

def get_start_date():
	return datetime.now() - timedelta(days=1000)

#1 [master]
def main(request):
	template = 'fin23/main.html'
	return render(request, template)


#++++++++++++
#  ACCOUNTS
#++++++++++++

### VIEW ACCOUNTS ###

# not using generic view yet because of the need to filter and annotate #

#2 [master][main][accounts]

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

	tsum = SubTransaction.objects.all().aggregate(Sum("amount"))
	tsum = float(tsum['amount__sum'])

	tsum = f"${tsum:,.2f}"

	template = "fin/accounts.html"

	context = {'accounts': accounts, 'tsum': tsum}

	return render(request, template, context)

### ADD ACCOUNT ###

#3 [master][main][accounts]

class AccountCreateView(CreateView):
	model = Account
	fields = "__all__"
	template_name = "fin/add.html"

### UPDATE ACCOUNT ###

#4 [accounts]

class UpdateAccount(UpdateView):
	model = Account
	fields = "__all__"
	template_name = "fin/update.html"
	success_url = reverse_lazy('list-accounts', kwargs={"a": "act"})

#+++++++++++++
#  CATEGORIES
#+++++++++++++

### VIEW CATEGORIES

#5 [master][main]

class CatListView(ListView):
	model = Category
	template_name = "fin/categories.html"
	context_object_name = 'page_obj'

	def get_queryset(self):
		categories = Category.objects.all()
		data = []

		for c in categories:
			trans_count = Transaction.objects.filter(subtransaction__groupedcat__category=c).count() or 0

			trans_total = Transaction.objects.filter(subtransaction__groupedcat__category=c).aggregate(Sum('subtransaction__amount'))['subtransaction__amount__sum'] or 0

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

		ccount = Category.objects.all().count()

		context = super(CatListView,self).get_context_data(**kwargs)
		context['ccount'] = ccount

		return context

### ADD CATEGORY ###

#6 [master][main][categories]

class CatCreateView(CreateView):
	model = Category
	fields = "__all__"
	template_name = "fin/add.html"


### UPDATE CATEGORY ###

#7 [categories]

class UpdateCategory(UpdateView):
	model = Category
	fields = "__all__"
	template_name = "fin/update.html"
	success_url = reverse_lazy('list-categories')


### SEARCH ###

#8 [categories]

class CatSearchView(ListView):
	model = Category
	template_name = "fin/categories.html"
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

### VIEW L1GROUPS

#9 [master][main][categories]

class L1GroupListView(ListView):
	model = L1Group
	template_name = "fin/l1groups.html"
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

#22 [master][main][categories][l1]

class L1GroupCreateView(CreateView):
	model = L1Group
	fields = "__all__"
	template_name = "fin/add.html"

### UPDATE L1 GROUP ###

#15 [l1]

class L1GroupUpdateView(UpdateView):
	model = L1Group
	fields = "__all__"
	template_name = "fin/update.html"
	success_url = reverse_lazy('list-l1groups')

#19 [master][main]

class GroupedCatListView(ListView):
	model = GroupedCat
	template_name = "fin/groupedcats.html"
	context_object_name = 'page_obj'

	def get_queryset(self):
		gcs = GroupedCat.objects.all()
		data = []

		for c in gcs:
			trans_count = Transaction.objects.filter(subtransaction__groupedcat=c.pk).count() or 0

			trans_total = Transaction.objects.filter(subtransaction__groupedcat=c.pk).aggregate(Sum('subtransaction__amount'))['subtransaction__amount__sum'] or 0

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

#12 [master][main][gc]

class GroupedCatCreateView(CreateView):
	model = GroupedCat
	fields = "__all__"
	template_name = "fin/add.html"

#20 [gc]

class GroupedCatUpdateView(UpdateView):
	model = GroupedCat
	fields = "__all__"
	template_name = "fin/update.html"
	success_url = reverse_lazy('list-gc')

#21 [gc]

class GroupedCatDeleteView(DeleteView):
	model = GroupedCat
	success_url = reverse_lazy('list-gc')
	template_name = "fin/confirm_delete.html"


#29 TBD

def load_c(request, payee_id=None):

	payee_id = request.GET.get("payee")

	if payee_id:
		cats =Category.objects.filter(transaction__payee=payee_id).distinct()
	else:
		cats = Category.objects.all()


	template = "fin/c-options.html"

	context = { "cats": cats }

	return render(request, template, context)

#30 TBD

def load_gc(request, category_id=None):

	category_id = request.GET.get("category")

	groupedcats = GroupedCat.objects.all()

	template = "fin/gc-options.html"

	context = { "groupedcats": groupedcats }

	return render(request, template, context)

#++++++++++++
#  PAYEES
#++++++++++++

#13 [master][main][payees]
def payees(request, a='act', o='payee'):

	if a=="all":
		payees = Payee.objects.all().annotate(
	 		trans_count=Count('transaction'),
	 		total_transactions=Sum('transaction__subtransaction__amount'),
	 		most_recent_transaction=Max('transaction__tdate')
		).order_by(o)

	else:
		payees = Payee.objects.filter(active=True).annotate(
			trans_count=Count('transaction'),
			total_transactions=Sum('transaction__subtransaction__amount'),
			most_recent_transaction=Max('transaction__tdate')
    		).order_by(o)

	tcount = Payee.objects.all().count()
	template = 'fin/payees.html'
	paginator = Paginator(payees, 25)

	page_number = request.GET.get("page")
	page_obj = paginator.get_page(page_number)

	context = {
		"page_obj": page_obj,
		"tcount": tcount,
	}

	return render(request, template, context)

### PAYEE SEARCH ###

#28 [payees]
class SearchResultsView(ListView):
	model = Payee
	template_name = ('fin/payees.html')
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

#24 [tlist]
class PayeeDetailView(DetailView):
	model = Payee
	template_name = "fin/detail.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		next = self.request.GET.get("next")
		dcat = self.request.GET.get("dcat")
		context["now"] = timezone.now()
		context["next"] = next
		context["dcat"] = dcat
		return context

### ADD PAYEE ###

#23 [master][main][payees]
class PayeeCreateView(CreateView):
	model = Payee
	#fields = "__all__"
	fields = [
	    'payee',
	    'def_gcat',
	    'active',
	]
	template_name = "fin/add.html"

### UPDATE PAYEE ###

#25 [payees]
class UpdatePayee(UpdateView):
	model = Payee
	fields = "__all__"
	template_name = "fin/update.html"

	def get_success_url(self):
		next = self.request.GET.get("next")

		if next:

			return next

		return reverse_lazy('list-payees', kwargs={"a": "act", "o": "-trans_count"})

### INACTIVATE PAYEE ###

#27 [payees]
def make_inactive(request, pk):

	next = request.GET.get('next', '/')

	payee = Payee.objects.get(pk=pk)
	payee.active = False
	payee.save()
	return redirect(next)

### DELETE PAYEE ###

#26 [payees]
class PayeeDeleteView(DeleteView):
	model = Payee
	success_url = reverse_lazy('list-payees', kwargs={"a": "act", "o": "payee"})
	template_name = "fin/confirm_delete.html"


