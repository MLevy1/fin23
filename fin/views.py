import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg
import mpld3
from django.http import HttpResponse
from django.template import loader
from datetime import timezone as tz
from .models import Category, Payee, Account, Issue, Trans, BudgetItem
from .forms import AddPayee, Moving, Budget, AddTransaction, PayeeMergeForm, PayeeCategoryUpdate, PayeeAccountUpdate, AddTransactionAll, PayeeCategoryUpdateAll
from django.shortcuts import render, get_list_or_404, redirect
from django.db.models import F, Sum, Window, Q, Avg, Max, Count
from django.db.models.functions import ExtractYear
from django.views.generic import ArchiveIndexView, TemplateView, ListView, MonthArchiveView, YearArchiveView, CreateView, UpdateView, DeleteView
import numpy_financial as npf
import pandas as pd
from django_pandas.io import read_frame 

pd.options.display.float_format = '{:,}'.format

from datetime import datetime, timedelta
from django.forms import modelformset_factory
from django.urls import reverse_lazy

from slick_reporting.views import ReportView, Chart
from slick_reporting.fields import SlickReportField
from slick_reporting.fields import ComputationField

from django.core.paginator import Paginator

PayeeFormSet = modelformset_factory(Payee, form=AddPayee, extra=0)

def get_start_date():
	return datetime.now() - timedelta(days=1000)

def main(request):
	template = loader.get_template('main.html')
	return HttpResponse(template.render())

#++++++++++++
#  PAYEES
#++++++++++++

### VIEW PAYEES ###

def payees(request, a='act', o='payee'):

	if a=="all":
		payees = Payee.objects.all().annotate(
        		trans_count=Count('trans'),
        		total_transactions=Sum('trans__amount'),
        		most_recent_transaction=Max('trans__tdate')
    		).order_by(o)

	else:
		payees = Payee.objects.filter(active=True).annotate(
        	trans_count=Count('trans'),
        	total_transactions=Sum('trans__amount'),
        	most_recent_transaction=Max('trans__tdate')
    		).order_by(o)

	template = 'payees.html'
	paginator = Paginator(payees, 25)

	page_number = request.GET.get("page")
	page_obj = paginator.get_page(page_number)

	context = {"page_obj": page_obj}

	return render(request, template, context)


### SEARCH ###

class HomePageView(TemplateView):
	template_name = 'home.html'

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
	success_url = reverse_lazy('payees', kwargs={"a": "act"})

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

def merge_payees(request, dpay=None):

	if request.method == 'POST':
		form = PayeeMergeForm(request.POST)
	
	if form.is_valid():
		source_payee = form.cleaned_data['source_payee']
		target_payee = form.cleaned_data['target_payee']

		# Update transactions with the target payee to use the source payee
		Trans.objects.filter(payee=target_payee).update(payee=source_payee)

		# Delete the target payee
		target_payee.delete()

		return redirect('/pay/act/payee/') 

	else:
		form = PayeeMergeForm(initial={'target_payee': dpay })

	return render(request, 'merge_payees.html', {'form': form  })

### UPDATE PAYEES CATEGORY ###

def payee_category_update_all(request, dpay=None):

	if request.method == 'POST':
		form = PayeeCategoryUpdateAll(request.POST)

		if form.is_valid():
			source_payee = form.cleaned_data['source_payee']
			target_category = form.cleaned_data['target_category']
			Trans.objects.filter(payee=source_payee).update(category=target_category)

			return redirect('/pay/act/payee/') # Redirect placholder
  
	else:
		form = PayeeCategoryUpdateAll(initial={'source_payee': dpay})


	return render(request, 'qupdate.html', {'form': form  })


def payee_category_update(request):
	if request.method == 'POST':
		form = PayeeCategoryUpdate(request.POST)

		if form.is_valid():
			source_payee = form.cleaned_data['source_payee']
			target_category = form.cleaned_data['target_category']
			Trans.objects.filter(payee=source_payee).update(category=target_category)

			return redirect('/qupdate/') # Redirect placholder
  
	else:
		form = PayeeCategoryUpdate()

	return render(request, 'qupdate.html', {'form': form  })

### UPDATE PAYEES ACCOUNT ###

def payee_account_update(request):
	if request.method == 'POST':
		form = PayeeAccountUpdate(request.POST)

		if form.is_valid():
			source_payee = form.cleaned_data['source_payee']
			target_account = form.cleaned_data['target_account']
			Trans.objects.filter(payee=source_payee).update(account=target_account)

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

### VIEW CATEGORIES

class CatListView(ListView):
	model = Category
	template_name = "categories.html"
	context_object_name = 'categories'

	def get_queryset(self):
		categories = Category.objects.all()
		data = []

		start_date = get_start_date()

		ann_actual = 0
		ann_budget = 0

		ann_actual = float(ann_actual)
		ann_budget = float(ann_budget)

		for c in categories:
			trans_total = Trans.objects.filter(category=c, tdate__gte=start_date).aggregate(Sum('amount'))['amount__sum'] or 0
			ann_total = float(trans_total) * 365/1000
			ann_total = float(ann_total)
			budget_items = BudgetItem.objects.filter(itemCat=c)
			budget_total = sum(item.annualAmt() for item in budget_items)
			budget_total = float(budget_total)

			if c.active != False:
				ann_actual += ann_total
				ann_budget += budget_total

			data.append({
				'pk': c.pk,
				'active': c.active,
				'category': c,
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

		return data
  

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
	success_url = reverse_lazy('categories')

#+++++++++++++++
#  TRANSACTIONS
#+++++++++++++++

### VIEW ALL TRANS ###

def transactions(request):
	transactions = Trans.objects.all().order_by('tdate')
	template = loader.get_template('transactions.html')
	paginator = Paginator(transactions, 50)

	page_number = request.GET.get("page")
	page_obj = paginator.get_page(page_number)

	context = {"page_obj": page_obj}

	return HttpResponse(template.render(context, request))

### ARCHIVE VIEWS

class TransYearArchiveView(YearArchiveView):
	queryset = Trans.objects.all()
	date_field = "tdate"
	make_object_list = True
	template_name = "trans_months.html"
    
class transactionMonthArchiveView(MonthArchiveView):
	queryset = Trans.objects.all().annotate(cumsum=Window(Sum('amount'), order_by=(F('tdate').asc(), F('tid').asc())))
	date_field = "tdate"
	template_name = "trans_monthly.html"

### ADD TRANSACTION ###

def atran(request, dpay=None):
    
  context = {}

  lt=Trans.objects.all().order_by("-tid").first().tid
	
  nt=lt+1

  if request.method == 'POST':
    form = AddTransaction(request.POST)
    
    if form.is_valid():
      form.save()
      lt=Trans.objects.all().order_by("-tid").first().tid
      nt=lt+1
      la=Trans.objects.all().order_by("-tid").first().account
      ld=Trans.objects.all().order_by("-tid").first().tdate
      form = AddTransaction(initial={'tid': nt, 'account': la, 'tdate': ld })

  else:
    form = AddTransaction(initial={'tid': nt, 'payee': dpay })

  context['form'] = form

  return render(request, "add.html", context)

### VIEW TRANSACTIONS ###

def tlist(request, acc='all', cat='all', pay='all'):
  
  T = Trans.objects.annotate(cumsum=Window(Sum('amount'), order_by=(F('tdate').asc(), F('tid').asc()))).order_by('-tdate', '-tid')

  if acc=="all" and cat=="all" and pay=="all":
    trans_list = T
  
  elif acc!="all" and cat=="all" and pay=="all":
    trans_list = get_list_or_404(T, account=acc)
  
  elif acc=="all" and cat!="all" and pay=="all":
    trans_list = get_list_or_404(T, category=cat)
  
  elif acc=="all" and cat=="all" and pay!="all":
    trans_list = get_list_or_404(T, payee=pay)
  
  elif acc=="all" and cat!="all" and pay!="all":
    trans_list = get_list_or_404(T, category=cat, payee=pay)
  
  elif acc!="all" and cat!="all" and pay=="all":
    trans_list = get_list_or_404(T, account=acc, category=cat)
  
  elif acc=="all" and cat!="all" and pay=="all":
    trans_list = get_list_or_404(T, account=acc, payee=pay)
  
  elif acc!="all" and cat!="all" and pay!="all":
    trans_list = get_list_or_404(T, account=acc, category=cat, payee=pay)
  
  context = { "trans_list": trans_list }
  
  template = loader.get_template('tlist.html')
  paginator = Paginator(trans_list, 50)

  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)

  context = {"page_obj": page_obj}

  return HttpResponse(template.render(context, request))

### UPDATE TRANSACTION ###

def utran_act(response, t_id):

  tran = Trans.objects.get(pk=t_id)

  form = AddTransaction(response.POST or None, instance=tran)

  next = response.POST.get('next', '/')

  if form.is_valid():
    form.save()
    
    return redirect(next)

  return render(response, 'update.html', {"tran": tran, 'form': form})

def utran(response, t_id):

  tran = Trans.objects.get(pk=t_id)

  form = AddTransactionAll(response.POST or None, instance=tran)

  next = response.POST.get('next', '/')

  if form.is_valid():
    form.save()
    
    return redirect(next)

  return render(response, 'update.html', {"tran": tran, 'form': form})

### DELETE TRANSACTION ###

class TransDeleteView(DeleteView):
    model = Trans
    success_url = reverse_lazy('main')
    template_name = "confirm_delete.html"


#++++++++++++
#   ISSUES
#++++++++++++

### VIEW ISSUES

class IssueListView(ListView):
	model = Issue
	template_name = "issues.html"

### ADD ISSUE ###

class IssueCreateView(CreateView):
	model = Issue
	fields = "__all__"
	template_name = "add.html"
	success_url = reverse_lazy('issues')

### UPDATE ISSUE ###

class UpdateIssue(UpdateView):
	model = Issue
	fields = "__all__"
	template_name = "update.html"
	success_url = reverse_lazy('issues')


'''
**************************
      BUDGET ITEMS
**************************
'''

### VIEW BUDGET ITEMS ###

class BudgetItemView(ListView):
	model = BudgetItem
	template_name = "budgetitems.html"

### ADD BUDGET ITEM ###

class BudgetItemCreateView(CreateView):
	model = BudgetItem
	fields = "__all__"
	template_name = "add.html"
	success_url = reverse_lazy('budgetitems')

### UPDATE BUDGET ITEM ###

class BudgetItemUpdateView(UpdateView):
	model = BudgetItem
	fields = "__all__"
	template_name = "update.html"
	success_url = reverse_lazy('budgetitems')


### DELETE BUDGET ITEM ###

class BudgetItemDeleteView(DeleteView):
	model = BudgetItem
	success_url = reverse_lazy('budgetitems')
	template_name = "confirm_delete.html"

'''
++++++++++++++
   REPORTING
++++++++++++++
'''

class testform(ReportView):

	report_model = Trans
	date_field = "tdate"
	group_by = "category"
    
	columns = [
		"category",
		SlickReportField.create(

            		method=Sum, field="amount", name="amount__sum", verbose_name=("Total Amount")
			     
		),
	]

	# Charts
	charts_settings = [
		Chart(
			"Totals",
			Chart.BAR,
			data_source="amount__sum",
			title_source="title",
		),
	]

class SumValueComputationField(ComputationField):
	calculation_method = Sum
	calculation_field = "amount"
	verbose_name = ("Total")
	name = "amount_sum"


class MonthlyCashFlow(ReportView):
	report_model = Trans
	date_field = "tdate"
	group_by = "category"
	columns = ["category"]


	time_series_pattern = "monthly"
	time_series_columns = [
		SumValueComputationField,
    	]

	chart_settings = [
		Chart(
			("Monthly Cash Flow"),
			Chart.AREA,
			data_source=["amount_sum"],
			title_source=["category"],
			plot_total=True,
		),
	]


'''
#++++++++++
#   MOVING
#++++++++++
'''

def move(response):
  if response.method=="POST":
    result=response.POST

    irate = float(result.get("irate"))
    term = float(result.get("term"))
    pprice = float(result.get("purchprice"))
    dpp = float(result.get("dppct"))/100

    dpa = pprice*dpp

    pv = pprice-dpa

    mrate = (irate/12) / 100
    nper = term*12
    
    mtg = npf.pmt(mrate, nper, pv, fv=0)
    mins = -1*float(result.get("annins"))/12

    ptr = float(result.get("ptaxrate"))/100
    mpt = -1*(ptr*pprice)/12

    tmpmt=mtg+mins+mpt

    result = {"tmpmt": tmpmt, "mpt": mpt, "mins": mins, "mtg": mtg, "dpa":dpa, "pprice": pprice }

    return render(response, "movecalcs.html", {"result":result})

  else:
    form = Moving(initial={"irate": 6.15, "term": 30, "ptaxrate": 1.813, "annins": 4000, "purchprice": 1210000, "dppct": 20 })

  return render(response, "move.html", {"form":form})

'''
++++++++++++
     BUDGET
++++++++++++
'''

def budget(response):
  if response.method=="POST":
    result=response.POST

    res={}

    aval = res["a_gross_pay"] = a_gross_pay = float(result.get("a_gross_pay"))
    res["q_gross_pay"] = aval/4
    res["m_gross_pay"] = aval/12
    res["b_gross_pay"] = aval/26
    res["w_gross_pay"] = aval/52
    res["d_gross_pay"] = aval/365
    
    
    aval = res["a_gross_bonus"] = a_gross_bonus = float(result.get("a_gross_bonus"))
    res["q_gross_bonus"] = aval/4
    res["m_gross_bonus"] = aval/12
    res["b_gross_bonus"] = aval/26
    res["w_gross_bonus"] = aval/52
    res["d_gross_bonus"] = aval/365
    

    res["a_al_taxable"] = a_al_taxable = float(result.get("a_al_taxable"))

    aval = res["a_total_pay"] = a_total_pay = a_gross_pay + a_gross_bonus + a_al_taxable
    res["q_total_pay"] = aval/4
    res["m_total_pay"] = aval/12
    res["b_total_pay"] = aval/26
    res["w_total_pay"] = aval/52
    res["d_total_pay"] = aval/365
    
    bw_medical = float(result.get("bw_medical"))
    bw_dental = float(result.get("bw_dental"))
    bw_daycare = float(result.get("bw_daycare"))

    aval = res["a_medical"] = bw_medical*26
    res["q_medical"] = aval /4
    res["m_medical"] = aval /12
    res["b_medical"] = aval /26
    res["w_medical"] = aval /52
    res["d_medical"] = aval /365

    aval = res["a_dental"] = bw_dental*26
    res["q_dental"] = aval /4
    res["m_dental"] = aval /12
    res["b_dental"] = aval /26
    res["w_dental"] = aval /52
    res["d_dental"] = aval /365
    
    aval = res["a_daycare"] = bw_daycare*26
    res["q_daycare"] = aval /4
    res["m_daycare"] = aval /12
    res["b_daycare"] = aval /26
    res["w_daycare"] = aval /52
    res["d_daycare"] = aval /365
    
    rate_401k = float(result.get("rate_401k"))

    max_401k_23 = -22500

    aval = res["a_401k"] = a_401k = (7/9)*max_401k_23
    res["q_401k"] = aval /4
    res["m_401k"] = aval /12
    res["b_401k"] = aval /26
    res["w_401k"] = aval /52
    res["d_401k"] = aval /365

    w_train = float(result.get("w_train"))

    aval = res["a_train"] = a_train = w_train * 48
    res["q_train"] = aval /4
    res["m_train"] = aval /12
    res["b_train"] = aval /26
    res["w_train"] = aval /52
    res["d_train"] = aval /365

    aval = res["a_pretax_ded"] = a_pretax_ded = a_train + a_401k + (26 * (bw_medical + bw_dental + bw_daycare))
    res["q_pretax_ded"] = aval /4
    res["m_pretax_ded"] = aval /12
    res["b_pretax_ded"] = aval /26
    res["w_pretax_ded"] = aval /52
    res["d_pretax_ded"] = aval /365

    aval = res["a_total_taxable"] = a_total_taxable = a_total_pay + a_pretax_ded
    res["q_total_taxable"] = aval /4
    res["m_total_taxable"] = aval /12
    res["b_total_taxable"] = aval /26
    res["w_total_taxable"] = aval /52
    res["d_total_taxable"] = aval /365

    std_ded_23 = -27700

    fedtaxable = a_total_taxable+std_ded_23

    if fedtaxable <= 22000:
      a_fed_tax = fedtaxable*-0.10
    elif fedtaxable <= 89450:
      a_fed_tax = -2200 + ((fedtaxable-22000)*-0.12)
    elif fedtaxable <= 190750:
      a_fed_tax = -10294 + ((fedtaxable-89450)*-0.22)
    elif fedtaxable <= 364200:
      a_fed_tax = -32580 + ((fedtaxable-190750)*-0.24)
    elif fedtaxable <= 462500:
      a_fed_tax = -74208 + ((fedtaxable-364200)*-0.32)
    elif fedtaxable <= 693750:
      a_fed_tax = -105664 + ((fedtaxable-462500)*-0.35)
    elif fedtaxable > 693750:
      a_fed_tax = -186601.5 + ((fedtaxable-693750)*-0.37)

    aval = res["a_al_fwh"] = a_al_fwh = float(result.get("a_al_fwh"))
    res["q_al_fwh"] = aval /4
    res["m_al_fwh"] = aval /12
    res["b_al_fwh"] = aval /26
    res["w_al_fwh"] = aval /52
    res["d_al_fwh"] = aval /365
    
    aval = res["a_fedtax"] = a_fed_tax  + a_al_fwh
    res["q_fedtax"] = aval /4
    res["m_fedtax"] = aval /12
    res["b_fedtax"] = aval /26
    res["w_fedtax"] = aval /52
    res["d_fedtax"] = aval /365

    ny_std_ded_23 = -17400
    ny_dep_exemption_23 = -2000

    ny_taxable = a_total_taxable + ny_std_ded_23 + ny_dep_exemption_23

    if ny_taxable<=323200 and ny_taxable>161550:
      ny_tw_line_3 = -9021-(0.0625*(ny_taxable-161550))
      ny_tw_line_6 = a_total_taxable-161550

      if ny_tw_line_6 < 50000:
        ny_tw_line_7 = ny_tw_line_6

      else:
        ny_tw_line_7 = 50000

      ny_tw_line_8 = ny_tw_line_7/50000
      ny_tw_line_4 = -430
      ny_tw_line_5 = -646
      ny_tw_line_9 = ny_tw_line_5 * ny_tw_line_8
      ny_tax_all_inc = ny_tw_line_3 + ny_tw_line_4 + ny_tw_line_9

    elif ny_taxable <= 2155350 and ny_taxable > 323200:
      ny_tw_line_3 = -19124-(0.0685*(ny_taxable-323200))
      ny_tw_line_6 = a_total_taxable-323200

      if ny_tw_line_6 < 50000:
        ny_tw_line_7 = ny_tw_line_6

      else:
        ny_tw_line_7 = 50000

      ny_tw_line_8 = ny_tw_line_7/50000
      ny_tw_line_4 = -1076
      ny_tw_line_5 = -1940
      ny_tw_line_9 = ny_tw_line_5 * ny_tw_line_8
      ny_tax_all_inc = ny_tw_line_3 + ny_tw_line_4 + ny_tw_line_9

    ny_source = a_total_taxable - a_al_taxable
    ny_pct = ny_source / a_total_taxable
    
    aval = res["a_nystax"] = a_nystax = ny_tax_all_inc * ny_pct
    res["q_nystax"] = aval /4
    res["m_nystax"] = aval /12
    res["b_nystax"] = aval /26
    res["w_nystax"] = aval /52
    res["d_nystax"] = aval /365

    aval = res["a_al_swh"] = a_al_swh = float(result.get("a_al_swh"))
    res["q_al_swh"] = aval /4
    res["m_al_swh"] = aval /12
    res["b_al_swh"] = aval /26
    res["w_al_swh"] = aval /52
    res["d_al_swh"] = aval /365

    nj_exemptions = -5000
    nj_prop_tax_ded = -15000
    nj_taxable = a_total_taxable + nj_exemptions + nj_prop_tax_ded
    nj_tax_rate = -0.0637
    nj_sub_amt = 4042.50
    nj_gross_tax = (nj_taxable * nj_tax_rate)+nj_sub_amt
    nj_nycredit = ny_pct * nj_gross_tax
    
    aval = res["a_njstax"] = a_njstax = nj_gross_tax - nj_nycredit + a_al_swh
    res["q_njstax"] = aval /4
    res["m_njstax"] = aval /12
    res["b_njstax"] = aval /26
    res["w_njstax"] = aval /52
    res["d_njstax"] = aval /365

    rate_sstax = float(result.get("rate_sstax"))

    if(a_total_pay<160200):
      aval = res["a_sstax"] = a_sstax = rate_sstax*a_total_pay

    else:
      aval = res["a_sstax"] = a_sstax = -9932.40

    res["q_sstax"] = aval /4
    res["m_sstax"] = aval /12
    res["b_sstax"] = aval /26
    res["w_sstax"] = aval /52
    res["d_sstax"] = aval /365

    rate_medicare = float(result.get("rate_medicare"))

    if a_total_pay>=200000:
      aval = res["a_medicare"] = a_medicare = (a_total_pay*rate_medicare)+((a_total_pay-200000)*0.009)
   
    else:
      aval = res["a_medicare"] = a_medicare = (a_total_pay*rate_medicare)

    res["q_medicare"] = aval /4
    res["m_medicare"] = aval /12
    res["b_medicare"] = aval /26
    res["w_medicare"] = aval /52
    res["d_medicare"] = aval /365

    aval = res["a_post_tax_inc"] = a_post_tax_inc = a_total_taxable + a_fed_tax + a_sstax + a_medicare + a_nystax + a_njstax
    res["q_post_tax_inc"] = aval /4
    res["m_post_tax_inc"] = aval /12
    res["b_post_tax_inc"] = aval /26
    res["w_post_tax_inc"] = aval /52
    res["d_post_tax_inc"] = aval /365

    aval = res["a_ml_post_tax_inc"] = a_ml_post_tax_inc = a_post_tax_inc - a_al_taxable
    res["q_ml_post_tax_inc"] = aval /4
    res["m_ml_post_tax_inc"] = aval /12
    res["b_ml_post_tax_inc"] = aval /26
    res["w_ml_post_tax_inc"] = aval /52
    res["d_ml_post_tax_inc"] = aval /365

    rate_r401k = float(result.get("rate_r401k"))

    aval = res["a_r401k"] = a_r401k = (2/9)*max_401k_23
    res["q_r401k"] = aval /4
    res["m_r401k"] = aval /12
    res["b_r401k"] = aval /26
    res["w_r401k"] = aval /52
    res["d_r401k"] = aval /365

    bw_arag = float(result.get("bw_arag"))

    aval = res["a_arag"] = a_arag = bw_arag*26
    res["q_arag"] = aval /4
    res["m_arag"] = aval /12
    res["b_arag"] = aval /26
    res["w_arag"] = aval /52
    res["d_arag"] = aval /365

    a_daycare_payback = float(result.get("a_daycare_payback"))
    w_school = float(result.get("w_school"))
    m_internet = float(result.get("m_internet"))
    m_phone = float(result.get("m_phone"))
    m_electric = float(result.get("m_electric"))
    m_natgas = float(result.get("m_natgas"))
    m_homeins = float(result.get("m_homeins")) 
    m_apple = float(result.get("m_apple"))
    a_carins = float(result.get("a_carins"))

    aval = res["a_fixed"] = a_fixed = (12*(m_internet + m_phone + m_electric + m_natgas + m_homeins + m_apple))+ a_carins + (52*w_school) + a_daycare_payback
    res["q_fixed"] = aval /4
    res["m_fixed"] = aval /12
    res["b_fixed"] = aval /26
    res["w_fixed"] = aval /52
    res["d_fixed"] = aval /365

    aval = res["a_post_fc_inc"] = a_post_fc_inc = a_ml_post_tax_inc + a_r401k + a_arag + a_fixed
    res["q_post_fc_inc"] = aval /4
    res["m_post_fc_inc"] = aval /12
    res["b_post_fc_inc"] = aval /26
    res["w_post_fc_inc"] = aval /52
    res["d_post_fc_inc"] = aval /365

    m_cabin_mtg = float(result.get("m_cabin_mtg"))
    m_cabin_electric = float(result.get("m_cabin_electric"))
    m_cabin_cable = float(result.get("m_cabin_cable"))
    a_cabin_hoa = float(result.get("a_cabin_hoa"))
    a_cabin_ptax = float(result.get("a_cabin_ptax"))
    a_cabin_ins = float(result.get("a_cabin_ins"))

    aval = res["a_cabin_exp"] = a_cabin_exp = a_cabin_hoa + a_cabin_ptax + a_cabin_ins + (12*(m_cabin_mtg +  m_cabin_electric + m_cabin_cable))
    res["q_cabin_exp"] = aval /4
    res["m_cabin_exp"] = aval /12
    res["b_cabin_exp"] = aval /26
    res["w_cabin_exp"] = aval /52
    res["d_cabin_exp"] = aval /365

    avg_cabin_inc = Trans.objects.filter(payee__payee__exact="rental income: tn").aggregate(Avg("amount")).get("amount__avg")

    aval = res["avg_a_cabin_inc"] = avg_a_cabin_inc = avg_cabin_inc*12
    res["avg_q_cabin_inc"] = aval /4
    res["avg_m_cabin_inc"] = aval /12
    res["avg_b_cabin_inc"] = aval /26
    res["avg_w_cabin_inc"] = aval /52
    res["avg_d_cabin_inc"] = aval /365

    m_car = float(result.get("m_car"))

    a_car = m_car*12

    m_mtg = float(result.get("m_mtg"))

    aval = res["a_mtg"] = a_mtg = m_mtg*12
    res["q_mtg"] = aval /4
    res["m_mtg"] = aval /12
    res["b_mtg"] = aval /26
    res["w_mtg"] = aval /52
    res["d_mtg"] = aval /365

    aval = res["a_ptax"] = a_ptax = float(result.get("a_ptax"))
    res["q_ptax"] = aval /4
    res["m_ptax"] = aval /12
    res["b_ptax"] = aval /26
    res["w_ptax"] = aval /52
    res["d_ptax"] = aval /365

    aval = res["a_post_h_inc"] = a_post_h_inc = a_post_fc_inc + a_mtg + a_ptax
    res["q_post_h_inc"] = aval /4
    res["m_post_h_inc"] = aval /12
    res["b_post_h_inc"] = aval /26
    res["w_post_h_inc"] = aval /52
    res["d_post_h_inc"] = aval /365

    aval = res["a_post_c_inc"] = a_post_c_inc = a_post_h_inc + float(avg_a_cabin_inc) + a_cabin_exp
    res["q_post_c_inc"] = aval /4
    res["m_post_c_inc"] = aval /12
    res["b_post_c_inc"] = aval /26
    res["w_post_c_inc"] = aval /52
    res["d_post_c_inc"] = aval /365

    denom = 1000

    a_avg_variable = 0

    sum_food = Trans.objects.filter(category__category__exact="food").filter(tdate__gte=datetime.now()-timedelta(days=1000)).aggregate(Sum("amount")).get("amount__sum")

    aval = res["a_avg_food"] = a_avg_food = float(sum_food) * (365/denom)
    res["q_avg_food"] = aval /4
    res["m_avg_food"] = aval /12
    res["b_avg_food"] = aval /26
    res["w_avg_food"] = aval /52
    res["d_avg_food"] = aval /365

    a_avg_variable += a_avg_food

    sum_entertainment = Trans.objects.filter(category__category__exact="entertainment").filter(tdate__gte=datetime.now()-timedelta(days=1000)).aggregate(Sum("amount")).get("amount__sum")

    aval = res["a_avg_entertainment"] = a_avg_entertainment = float(sum_entertainment) * (365/denom)
    res["q_avg_entertainment"] = aval /4
    res["m_avg_entertainment"] = aval /12
    res["b_avg_entertainment"] = aval /26
    res["w_avg_entertainment"] = aval /52
    res["d_avg_entertainment"] = aval /365

    a_avg_variable += a_avg_entertainment

    sum_kids = Trans.objects.filter(category__category__exact="kids").filter(tdate__gte=datetime.now()-timedelta(days=1000)).aggregate(Sum("amount")).get("amount__sum")

    aval = res["a_avg_kids"] = a_avg_kids = float(sum_kids) * (365/denom)
    res["q_avg_kids"] = aval /4
    res["m_avg_kids"] = aval /12
    res["b_avg_kids"] = aval /26
    res["w_avg_kids"] = aval /52
    res["d_avg_kids"] = aval /365

    a_avg_variable += a_avg_kids

    sum_coffee = Trans.objects.filter(category__category__exact="coffee").filter(tdate__gte=datetime.now()-timedelta(days=1000)).aggregate(Sum("amount")).get("amount__sum")

    aval = res["a_avg_coffee"] = a_avg_coffee = float(sum_coffee) * (365/denom)
    res["q_avg_coffee"] = aval /4
    res["m_avg_coffee"] = aval /12
    res["b_avg_coffee"] = aval /26
    res["w_avg_coffee"] = aval /52
    res["d_avg_coffee"] = aval /365

    a_avg_variable += a_avg_coffee

    sum_furniture = Trans.objects.filter(category__category__exact="furniture").filter(tdate__gte=datetime.now()-timedelta(days=1000)).aggregate(Sum("amount")).get("amount__sum")

    aval = res["a_avg_furniture"] = a_avg_furniture = float(sum_furniture) * (365/denom)
    res["q_avg_furniture"] = aval /4
    res["m_avg_furniture"] = aval /12
    res["b_avg_furniture"] = aval /26
    res["w_avg_furniture"] = aval /52
    res["d_avg_furniture"] = aval /365

    a_avg_variable += a_avg_furniture

    sum_health = Trans.objects.filter(category__category__exact="health").filter(tdate__gte=datetime.now()-timedelta(days=1000)).aggregate(Sum("amount")).get("amount__sum")

    aval = res["a_avg_health"] = a_avg_health = float(sum_health) * (365/denom)
    res["q_avg_health"] = aval /4
    res["m_avg_health"] = aval /12
    res["b_avg_health"] = aval /26
    res["w_avg_health"] = aval /52
    res["d_avg_health"] = aval /365

    a_avg_variable += a_avg_health

    sum_hs = Trans.objects.filter(category__category__exact="home services").filter(tdate__gte=datetime.now()-timedelta(days=1000)).aggregate(Sum("amount")).get("amount__sum")

    aval = res["a_avg_hs"] = a_avg_hs = float(sum_hs) * (365/denom)
    res["q_avg_hs"] = aval /4
    res["m_avg_hs"] = aval /12
    res["b_avg_hs"] = aval /26
    res["w_avg_hs"] = aval /52
    res["d_avg_hs"] = aval /365

    a_avg_variable += a_avg_hs

    sum_household = Trans.objects.filter(category__category__exact="household").filter(tdate__gte=datetime.now()-timedelta(days=1000)).aggregate(Sum("amount")).get("amount__sum")

    aval = res["a_avg_household"] = a_avg_household = float(sum_household) * (365/denom)
    res["q_avg_household"] = aval /4
    res["m_avg_household"] = aval /12
    res["b_avg_household"] = aval /26
    res["w_avg_household"] = aval /52
    res["d_avg_household"] = aval /365

    a_avg_variable += a_avg_household

    sum_other = Trans.objects.filter(category__category__exact="other").filter(tdate__gte=datetime.now()-timedelta(days=1000)).aggregate(Sum("amount")).get("amount__sum")

    aval = res["a_avg_other"] = a_avg_other = float(sum_other) * (365/denom)
    res["q_avg_other"] = aval /4
    res["m_avg_other"] = aval /12
    res["b_avg_other"] = aval /26
    res["w_avg_other"] = aval /52
    res["d_avg_other"] = aval /365

    a_avg_variable += a_avg_other

    sum_pc = Trans.objects.filter(category__category__exact="personal care").filter(tdate__gte=datetime.now()-timedelta(days=1000)).aggregate(Sum("amount")).get("amount__sum")

    aval = res["a_avg_pc"] = a_avg_pc = float(sum_pc) * (365/denom)
    res["q_avg_pc"] = aval /4
    res["m_avg_pc"] = aval /12
    res["b_avg_pc"] = aval /26
    res["w_avg_pc"] = aval /52
    res["d_avg_pc"] = aval /365

    a_avg_variable += a_avg_pc

    sum_pets = Trans.objects.filter(category__category__exact="pets").filter(tdate__gte=datetime.now()-timedelta(days=1000)).aggregate(Sum("amount")).get("amount__sum")

    aval = res["a_avg_pets"] = a_avg_pets = float(sum_pets) * (365/denom)
    res["q_avg_pets"] = aval /4
    res["m_avg_pets"] = aval /12
    res["b_avg_pets"] = aval /26
    res["w_avg_pets"] = aval /52
    res["d_avg_pets"] = aval /365

    a_avg_variable += a_avg_pets

    sum_shopping = Trans.objects.filter(category__category__exact="shopping").filter(tdate__gte=datetime.now()-timedelta(days=1000)).aggregate(Sum("amount")).get("amount__sum")

    aval = res["a_avg_shopping"] = a_avg_shopping = float(sum_shopping) * (365/denom)
    res["q_avg_shopping"] = aval /4
    res["m_avg_shopping"] = aval /12
    res["b_avg_shopping"] = aval /26
    res["w_avg_shopping"] = aval /52
    res["d_avg_shopping"] = aval /365

    a_avg_variable += a_avg_shopping

    sum_transport = Trans.objects.filter(category__category__exact="transport").filter(tdate__gte=datetime.now()-timedelta(days=1000)).aggregate(Sum("amount")).get("amount__sum")

    aval = res["a_avg_transport"] = a_avg_transport = float(sum_transport) * (365/denom)
    res["q_avg_transport"] = aval /4
    res["m_avg_transport"] = aval /12
    res["b_avg_transport"] = aval /26
    res["w_avg_transport"] = aval /52
    res["d_avg_transport"] = aval /365

    a_avg_variable += a_avg_transport

    sum_vacation = Trans.objects.filter(category__category__exact="vacation").filter(tdate__gte=datetime.now()-timedelta(days=1000)).aggregate(Sum("amount")).get("amount__sum")

    aval = res["a_avg_vacation"] = a_avg_vacation = float(sum_vacation) * (365/denom)
    res["q_avg_vacation"] = aval /4
    res["m_avg_vacation"] = aval /12
    res["b_avg_vacation"] = aval /26
    res["w_avg_vacation"] = aval /52
    res["d_avg_vacation"] = aval /365

    a_avg_variable += a_avg_vacation

    sum_alcohol = Trans.objects.filter(category__category__exact="alcohol").filter(tdate__gte=datetime.now()-timedelta(days=1000)).aggregate(Sum("amount")).get("amount__sum")

    aval = res["a_avg_alcohol"] = a_avg_alcohol = float(sum_alcohol) * (365/denom)
    res["q_avg_alcohol"] = aval /4
    res["m_avg_alcohol"] = aval /12
    res["b_avg_alcohol"] = aval /26
    res["w_avg_alcohol"] = aval /52
    res["d_avg_alcohol"] = aval /365

    a_avg_variable += a_avg_alcohol

    sum_hi = Trans.objects.filter(category__category__exact="home improvement").filter(tdate__gte=datetime.now()-timedelta(days=1000)).aggregate(Sum("amount")).get("amount__sum")

    aval = res["a_avg_hi"] = a_avg_hi = float(sum_hi) * (365/denom)
    res["q_avg_hi"] = aval /4
    res["m_avg_hi"] = aval /12
    res["b_avg_hi"] = aval /26
    res["w_avg_hi"] = aval /52
    res["d_avg_hi"] = aval /365

    a_avg_variable += a_avg_hi

    aval = res["a_avg_variable"] = a_avg_variable
    res["q_avg_variable"] = aval /4
    res["m_avg_variable"] = aval /12
    res["b_avg_variable"] = aval /26
    res["w_avg_variable"] = aval /52
    res["d_avg_variable"] = aval /365

    aval = res["a_post_var_inc"] = a_post_var_inc = a_post_c_inc + a_avg_variable
    res["q_post_var_inc"] = aval /4
    res["m_post_var_inc"] = aval /12
    res["b_post_var_inc"] = aval /26
    res["w_post_var_inc"] = aval /52
    res["d_post_var_inc"] = aval /365

    sum_alyssa = Trans.objects.filter(category__category__exact="alyssa").filter(tdate__gte=datetime.now()-timedelta(days=1000)).aggregate(Sum("amount")).get("amount__sum")

    aval = res["a_avg_alyssa"] = a_avg_alyssa = float(sum_alyssa) * (365/denom)
    res["q_avg_alyssa"] = aval /4
    res["m_avg_alyssa"] = aval /12
    res["b_avg_alyssa"] = aval /26
    res["w_avg_alyssa"] = aval /52
    res["d_avg_alyssa"] = aval /365

    sum_gifts = Trans.objects.filter(category__category__exact="gifts given").filter(tdate__gte=datetime.now()-timedelta(days=1000)).aggregate(Sum("amount")).get("amount__sum")

    aval = res["a_avg_gifts"] = a_avg_gifts = float(sum_gifts) * (365/denom)
    res["q_avg_gifts"] = aval /4
    res["m_avg_gifts"] = aval /12
    res["b_avg_gifts"] = aval /26
    res["w_avg_gifts"] = aval /52
    res["d_avg_gifts"] = aval /365

    aval = res["a_total"] = a_post_var_inc + a_avg_alyssa + a_avg_gifts
    res["q_total"] = aval /4
    res["m_total"] = aval /12
    res["b_total"] = aval /26
    res["w_total"] = aval /52
    res["d_total"] = aval /365

    return render(response, "budgetresults.html", {"result":res})

  else:
    form = Budget(initial={"a_gross_pay": 212000, "a_gross_bonus": 75000, "a_al_taxable": 0, "a_al_fwh": 0, "a_al_swh": 0, "bw_medical": -327.18, "bw_dental": -21.12, "bw_daycare": -96.15, "rate_sstax": -0.062, "rate_medicare": -0.0145, "rate_401k": -0.07, "w_train": -91.50, "rate_r401k": -0.02, "bw_arag": -5.76, "m_internet": -50, "m_phone": -200,  "m_electric": -150, "m_natgas": -50, "a_carins": -2000, "m_homeins": -333, "m_apple": -35, "m_cabin_mtg": -1033.26, "a_cabin_ptax": -694, "a_cabin_ins": -2046.71, "m_cabin_electric": -140, "m_cabin_cable": -300, "a_cabin_hoa": -300, "w_school": -653.20, "m_car": 0, "m_mtg": -4435.46, "a_ptax": -19420.32, "a_daycare_payback": 2500})

  return render(response, "budget.html", {"form":form})


'''

===================

####   PANDAS  ####

===================

'''

def ptran(request):
	
	qs = Trans.objects.all().values()
	df = read_frame(qs)

	# Convert the 'tdate' column to a datetime series
	df['tdate'] = pd.to_datetime(df['tdate'])

	# Create a new 'month' column from the 'tdate' column
	df['year'] = df['tdate'].dt.to_period('Y')

	# Pivot the DataFrame to group data by 'month' and 'category_id', and calculate the sum of 'amount'
	pt = pd.pivot_table(df, values='amount', index='year', columns='category_id', aggfunc='sum', fill_value=0).astype(float)

	pt.loc[:,'Total H'] = pt.sum(axis=1).round(0).astype(float)
	pt.loc['Total']= pt.sum().round(0).astype(float)

	# Reset the index to have 'month' as a regular column
	pt = pt.reset_index()

	pt = pt.iloc[:, :].reset_index(drop=True)

	# Convert the pivot table to an HTML table
	pivot_data = pt.to_html(index=False, escape=False, formatters={'numbers': '{:,2f}'.format})
	
	context = {

		'pivot' : pivot_data,

	}

	return render(request, "ptran.html", context)

def testg(request):
	
	qs = Trans.objects.all().values()
	
	df = read_frame(qs)

	# Convert the 'tdate' column to a datetime series
	df['tdate'] = pd.to_datetime(df['tdate'])

	# Create a new 'year' column from the 'tdate' column
	df['year'] = df['tdate'].dt.to_period('Y')
	
	# Convert the 'year' column to a string
	df['year'] = df['year'].astype(str)
	df['year'] = df['year'].str[2:]

	# Pivot the DataFrame to group data by 'year' and 'category_id', and calculate the sum of 'amount'
	pt = pd.pivot_table(df, values='amount', index='year', columns='category_id', aggfunc='sum', fill_value=0).astype(float)

	# Reset the index to have 'month' as a regular column
	pt = pt.reset_index()
	
	#pt = pt.drop(columns=["waxhaw house", "middletown house purchase", "sunset beach condo", "concord house", "ga rental property", "tn rental property", "investments", "income"])
	
	pt = pt[['year', 'income']]

	fig, ax = plt.subplots()
	
	# Plot the data
	for column in pt.columns[1:]:
		ax.bar(pt['year'], pt[column], label=f'Category {column}')

	ax.set(xlabel='Year', ylabel='Total Amount',
		title='Total Amount by Year and Category')
	
	ax.legend(loc='lower center')
	
	ax.grid()
	
	response = HttpResponse(content_type = 'image/png')
	
	canvas = FigureCanvasAgg(fig)
	
	canvas.print_png(response)
	
	return response