from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpRequest
from django.template import loader
from .models import Category, Payee, Account, Issue, Trans
from .forms import AddAccount, AddCategory, AddPayee, Moving, AddIssue, Budget, AddTransaction, PayeeMergeForm
from django.shortcuts import get_object_or_404, render, get_list_or_404, redirect
from django_pandas.io import read_frame
from django.db.models import F, Sum, Window, FloatField, Func, Value, DecimalField, Q, Avg, Max, Count
from django.db.models.functions import Round, Cast
from django.views.generic import TemplateView, ListView
import numpy_financial as npf
from datetime import datetime, timedelta

from django.forms import modelformset_factory

from slick_reporting.views import ReportView
from slick_reporting.fields import SlickReportField
from slick_reporting.generator import Chart

PayeeFormSet = modelformset_factory(Payee, form=AddPayee, extra=0)

def delete_payee(request, pk):
    payee = Payee.objects.get(pk=pk)
    payee.delete()
    return redirect('/pay/act/')

def make_inactive(request, pk):
    payee = Payee.objects.get(pk=pk)
    payee.active = False
    payee.save()
    return redirect('/pay/act')

def merge_payees(request):
    if request.method == 'POST':
        form = PayeeMergeForm(request.POST)
        
        if form.is_valid():
            source_payee = form.cleaned_data['source_payee']
            target_payee = form.cleaned_data['target_payee']

            # Update transactions with the target payee to use the source payee
            Trans.objects.filter(payee=target_payee).update(payee=source_payee)

            # Delete the target payee
            target_payee.delete()

            return redirect('/pay/act/')  # Redirect to a success page

    else:
        form = PayeeMergeForm(initial={'source_payee': 2860 })

    return render(request, 'merge_payees.html', {'form': form  })


def editpayees(request):
    queryset = Payee.objects.all()
    formset = PayeeFormSet(queryset=queryset)

    if request.method == 'POST':
        formset = PayeeFormSet(request.POST)
        if formset.is_valid():
            formset.save()

    return render(request, 'editpayees.html', {'formset': formset})


class testform(ReportView):

    report_model = Trans
    date_field = "tdate"
    group_by = "tdate"
    
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

def main(request):
  template = loader.get_template('main.html')
  return HttpResponse(template.render())


def accounts(request, a='act'):

  if a=="all":
    accounts = Account.objects.all()
  else:
    accounts = Account.objects.filter(active=True)

  return render(request, "accounts.html", {'accounts': accounts})


def payees(request, a='act'):

  if a=="all":
    payees = Payee.objects.all().annotate(
        trans_count=Count('trans'),
        total_transactions=Sum('trans__amount'),
        most_recent_transaction=Max('trans__tdate')
    ).order_by('most_recent_transaction')

  else:
    payees = Payee.objects.filter(active=True).annotate(
        trans_count=Count('trans'),
        total_transactions=Sum('trans__amount'),
        most_recent_transaction=Max('trans__tdate')
    ).order_by('trans_count')

  return render(request, "payees.html", {'payees': payees})
  

def categories(request):
  categories = Category.objects.all()
  template = loader.get_template('categories.html')
  context = {
    'categories': categories,
  }
  return HttpResponse(template.render(context, request))



def transactions(request):
  transactions = Trans.objects.all().order_by('tdate')
  template = loader.get_template('transactions.html')
  context = {
    'transactions': transactions,
  }
  return HttpResponse(template.render(context, request))


def aact(response):
  if response.method=="POST":
    form=AddAccount(response.POST)
    
    if form.is_valid():
      n=form.cleaned_data["act"]
      t=Account(account=n)
      t.save()

    return HttpResponseRedirect("/act/")

  else:
    form = AddAccount()

  return render(response, "add.html", {"form":form})

def acat(response):
  if response.method=="POST":
    form=AddCategory(response.POST)
    
    if form.is_valid():
      n=form.cleaned_data["cat"]
      t=Category(category=n)
      t.save()
    
    return HttpResponseRedirect("/cat/")

  else:
    form = AddCategory()
  return render(response, "add.html", {"form":form})


def apay(response):
  if response.method=="POST":
    form=AddPayee(response.POST)
    
    if form.is_valid():
      n=form.cleaned_data["pay"]
      t=Payee(payee=n)
      t.save()

    return HttpResponseRedirect("/pay/")

  else:
    form = AddPayee()

  return render(response, "add.html", {"form":form})

def atran(request):
    
	context = {}

	lt=Trans.objects.all().order_by("-tid").first().tid
	
	nt=lt+1

	form = AddTransaction(request.POST or None, initial={'tid': nt})

	if form.is_valid():
		form.save()

	context['form'] = form

	return render(request, "add.html", context)

def tlist(request, acc='all', cat='all', pay='all'):
  
  T = Trans.objects.annotate(
     cumsum=Window(Sum('amount'), order_by=F('id').asc())
  ).order_by('tdate', 'cumsum')

  if acc=="all" and cat=="all" and pay=="all":
    trans_list = T[:500]
  
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
  
  return render (request, "tlist.html", context)
	
def tdetail(request, t_id):
	
	tran = get_object_or_404(Transaction, pk=t_id)
	
	return render	(request, "tdetail.html", {"tran": tran})
	


#ISSUES

def issues(request):
  issues = Issue.objects.all().order_by('opendate').values()
  template = loader.get_template('issues.html')
  context = {
    'issues': issues,
  }
  return HttpResponse(template.render(context, request))

def aissue(response):
  if response.method=="POST":
    form = AddIssue(response.POST)

    if form.is_valid():
      form.save()

    return HttpResponseRedirect("/issues/")

  else:
    form = AddIssue()

  return render(response, "aissue.html", {"form": form})

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


def uact(request, act_id):
  act = Account.objects.get(pk=act_id)
  form = AddAccount(request.POST or None, instance=act)
  if form.is_valid():
      form.save()

      return redirect("/act/act/")
  return render(request, 'update.html', {"act": act, 'form': form})

def ucat(request, cat_id):
  cat = Category.objects.get(pk=cat_id)
  form = AddCategory(request.POST or None, instance=cat)
  if form.is_valid():
      form.save()

      return redirect("/cat/")
  return render(request, 'update.html', {"cat": cat, 'form': form})

def upay(request, pay_id):
  pay = Payee.objects.get(pk=pay_id)
  form = AddPayee(request.POST or None, instance=pay)
  if form.is_valid():
      form.save()

      return redirect("/pay/act/")
  return render(request, 'update.html', {"pay": pay, 'form': form})


def uissue(response, issue_id):

  issue = Issue.objects.get(pk=issue_id)

  form = AddIssue(response.POST or None, instance=issue)

  if form.is_valid():
    form.save()

    return redirect("/issues/")

  return render(response, 'update.html', {"issue": issue, 'form': form})


def utran(response, t_id):

  tran = Trans.objects.get(pk=t_id)

  form = AddTransaction(response.POST or None, instance=tran)

  if form.is_valid():
    form.save()

    return redirect("/tlist/all/all/all/")

  return render(response, 'update.html', {"tran": tran, 'form': form})


class HomePageView(TemplateView):
    template_name = 'home.html'

class SearchResultsView(ListView):
    model = Payee
    template_name = 'results.html'
    
    def get_queryset(self):
        query = self.request.GET.get("q")
        return Payee.objects.filter(Q(payee__icontains=query))


def budget(response):
  if response.method=="POST":
    result=response.POST

    res={}

    res["a_gross_pay"] = a_gross_pay = float(result.get("a_gross_pay"))
    
    res["a_gross_bonus"] = a_gross_bonus = float(result.get("a_gross_bonus"))

    res["a_al_taxable"] = a_al_taxable = float(result.get("a_al_taxable"))

    res["a_total_pay"] = a_total_pay = a_gross_pay + a_gross_bonus + a_al_taxable

    bw_medical = float(result.get("bw_medical"))
    bw_dental = float(result.get("bw_dental"))
    bw_daycare = float(result.get("bw_daycare"))

    res["a_medical"] = bw_medical*26
    res["a_dental"] = bw_dental*26
    res["a_daycare"] = bw_daycare*26
    
    rate_401k = float(result.get("rate_401k"))

    max_401k_23 = -22500

    res["a_401k"] = a_401k = (7/9)*max_401k_23

    w_train = float(result.get("w_train"))

    res["a_train"] = a_train = w_train * 48

    res["a_pretax_ded"] = a_pretax_ded = a_train + a_401k + (26 * (bw_medical + bw_dental + bw_daycare))

    res["a_total_taxable"] = a_total_taxable = a_total_pay + a_pretax_ded

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

    res["a_al_fwh"] = a_al_fwh = float(result.get("a_al_fwh"))

    res["a_fedtax"] = a_fed_tax  + a_al_fwh
    
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
    
    res["a_nystax"] = a_nystax = ny_tax_all_inc * ny_pct

    res["a_al_swh"] = a_al_swh = float(result.get("a_al_swh"))

    nj_exemptions = -5000
    nj_prop_tax_ded = -15000
    nj_taxable = a_total_taxable + nj_exemptions + nj_prop_tax_ded
    nj_tax_rate = -0.0637
    nj_sub_amt = 4042.50
    nj_gross_tax = (nj_taxable * nj_tax_rate)+nj_sub_amt
    nj_nycredit = ny_pct * nj_gross_tax
    res["a_njstax"] = a_njstax = nj_gross_tax - nj_nycredit + a_al_swh
	
    rate_sstax = float(result.get("rate_sstax"))

    if(a_total_pay<160200):
      res["a_sstax"] = a_sstax = rate_sstax*a_total_pay
    else:
      res["a_sstax"] = a_sstax = -9932.40

    rate_medicare = float(result.get("rate_medicare"))

    if a_total_pay>=200000:
      res["a_medicare"] = a_medicare = (a_total_pay*rate_medicare)+((a_total_pay-200000)*0.009)
    else:
      res["a_medicare"] = a_medicare = (a_total_pay*rate_medicare)

    res["a_post_tax_inc"] = a_post_tax_inc = a_total_taxable + a_fed_tax + a_sstax + a_medicare + a_nystax + a_njstax

    res["a_ml_post_tax_inc"] = a_ml_post_tax_inc = a_post_tax_inc - a_al_taxable

    rate_r401k = float(result.get("rate_r401k"))

    res["a_r401k"] = a_r401k = (2/9)*max_401k_23

    bw_arag = float(result.get("bw_arag"))

    res["a_arag"] = a_arag = bw_arag*26

    m_internet = float(result.get("m_internet"))
    m_phone = float(result.get("m_phone"))
    m_electric = float(result.get("m_electric"))
    m_natgas = float(result.get("m_natgas"))
    m_homeins = float(result.get("m_homeins")) 
    m_apple = float(result.get("m_apple"))
    a_carins = float(result.get("a_carins"))

    res["a_fixed"] = a_fixed = (12*(m_internet + m_phone + m_electric + m_natgas + m_homeins + m_apple))+ a_carins

    res["a_post_fc_inc"] = a_post_fc_inc = a_ml_post_tax_inc + a_r401k + a_arag

    m_cabin_mtg = float(result.get("m_cabin_mtg"))
    m_cabin_electric = float(result.get("m_cabin_electric"))
    m_cabin_cable = float(result.get("m_cabin_cable"))
    a_cabin_hoa = float(result.get("a_cabin_hoa"))
    a_cabin_ptax = float(result.get("a_cabin_ptax"))
    a_cabin_ins = float(result.get("a_cabin_ins"))

    res["a_cabin_exp"] = a_cabin_exp = a_cabin_hoa + a_cabin_ptax + a_cabin_ins + (12*(m_cabin_mtg +  m_cabin_electric + m_cabin_cable))

    avg_cabin_inc = Trans.objects.filter(payee__payee__exact="rental income: tn").aggregate(Avg("amount")).get("amount__avg")

    res["avg_a_cabin_inc"] = avg_a_cabin_inc = avg_cabin_inc*12

    m_car = float(result.get("m_car"))

    a_car = m_car*12

    m_mtg = float(result.get("m_mtg"))

    res["a_mtg"] = a_mtg = m_mtg*12

    res["a_ptax"] = a_ptax = float(result.get("a_ptax"))

    res["a_post_h_inc"] = a_post_h_inc = a_post_fc_inc + a_mtg + a_ptax

    res["a_post_c_inc"] = a_post_c_inc = a_post_h_inc + float(avg_a_cabin_inc) + a_cabin_exp

    denom = 977

    a_avg_variable = 0

    sum_food = Trans.objects.filter(category__category__exact="food").filter(tdate__gte=datetime.now()-timedelta(days=1000)).aggregate(Sum("amount")).get("amount__sum")

    res["a_avg_food"] = a_avg_food = float(sum_food) * (365/denom)

    a_avg_variable += a_avg_food

    sum_entertainment = Trans.objects.filter(category__category__exact="entertainment").filter(tdate__gte=datetime.now()-timedelta(days=1000)).aggregate(Sum("amount")).get("amount__sum")

    res["a_avg_entertainment"] = a_avg_entertainment = float(sum_entertainment) * (365/denom)

    a_avg_variable += a_avg_entertainment

    sum_coffee = Trans.objects.filter(category__category__exact="coffee").filter(tdate__gte=datetime.now()-timedelta(days=1000)).aggregate(Sum("amount")).get("amount__sum")

    res["a_avg_coffee"] = a_avg_coffee = float(sum_coffee) * (365/denom)

    a_avg_variable += a_avg_coffee

    sum_furniture = Trans.objects.filter(category__category__exact="furniture").filter(tdate__gte=datetime.now()-timedelta(days=1000)).aggregate(Sum("amount")).get("amount__sum")

    res["a_avg_furniture"] = a_avg_furniture = float(sum_furniture) * (365/denom)

    a_avg_variable += a_avg_furniture

    sum_health = Trans.objects.filter(category__category__exact="health").filter(tdate__gte=datetime.now()-timedelta(days=1000)).aggregate(Sum("amount")).get("amount__sum")

    res["a_avg_health"] = a_avg_health = float(sum_health) * (365/denom)

    a_avg_variable += a_avg_health

    sum_hs = Trans.objects.filter(category__category__exact="home services").filter(tdate__gte=datetime.now()-timedelta(days=1000)).aggregate(Sum("amount")).get("amount__sum")

    res["a_avg_hs"] = a_avg_hs = float(sum_hs) * (365/denom)

    a_avg_variable += a_avg_hs

    sum_household = Trans.objects.filter(category__category__exact="household").filter(tdate__gte=datetime.now()-timedelta(days=1000)).aggregate(Sum("amount")).get("amount__sum")

    res["a_avg_household"] = a_avg_household = float(sum_household) * (365/denom)

    a_avg_variable += a_avg_household

    sum_other = Trans.objects.filter(category__category__exact="other").filter(tdate__gte=datetime.now()-timedelta(days=1000)).aggregate(Sum("amount")).get("amount__sum")

    res["a_avg_other"] = a_avg_other = float(sum_other) * (365/denom)

    a_avg_variable += a_avg_other

    sum_pc = Trans.objects.filter(category__category__exact="personal care").filter(tdate__gte=datetime.now()-timedelta(days=1000)).aggregate(Sum("amount")).get("amount__sum")

    res["a_avg_pc"] = a_avg_pc = float(sum_pc) * (365/denom)

    a_avg_variable += a_avg_pc

    sum_pets = Trans.objects.filter(category__category__exact="pets").filter(tdate__gte=datetime.now()-timedelta(days=1000)).aggregate(Sum("amount")).get("amount__sum")

    res["a_avg_pets"] = a_avg_pets = float(sum_pets) * (365/denom)

    a_avg_variable += a_avg_pets

    sum_shopping = Trans.objects.filter(category__category__exact="shopping").filter(tdate__gte=datetime.now()-timedelta(days=1000)).aggregate(Sum("amount")).get("amount__sum")

    res["a_avg_shopping"] = a_avg_shopping = float(sum_shopping) * (365/denom)

    a_avg_variable += a_avg_shopping

    sum_transport = Trans.objects.filter(category__category__exact="transport").filter(tdate__gte=datetime.now()-timedelta(days=1000)).aggregate(Sum("amount")).get("amount__sum")

    res["a_avg_transport"] = a_avg_transport = float(sum_transport) * (365/denom)

    a_avg_variable += a_avg_transport

    sum_vacation = Trans.objects.filter(category__category__exact="vacation").filter(tdate__gte=datetime.now()-timedelta(days=1000)).aggregate(Sum("amount")).get("amount__sum")

    res["a_avg_vacation"] = a_avg_vacation = float(sum_vacation) * (365/denom)

    a_avg_variable += a_avg_vacation

    sum_alcohol = Trans.objects.filter(category__category__exact="alcohol").filter(tdate__gte=datetime.now()-timedelta(days=1000)).aggregate(Sum("amount")).get("amount__sum")

    res["a_avg_alcohol"] = a_avg_alcohol = float(sum_alcohol) * (365/denom)

    a_avg_variable += a_avg_alcohol

    sum_hi = Trans.objects.filter(category__category__exact="home improvement").filter(tdate__gte=datetime.now()-timedelta(days=1000)).aggregate(Sum("amount")).get("amount__sum")

    res["a_avg_hi"] = a_avg_hi = float(sum_hi) * (365/denom)

    a_avg_variable += a_avg_hi

    res["a_avg_variable"] = a_avg_variable

    res["a_post_var_inc"] = a_post_var_inc = a_post_c_inc + a_avg_variable

    sum_alyssa = Trans.objects.filter(category__category__exact="alyssa").filter(tdate__gte=datetime.now()-timedelta(days=1000)).aggregate(Sum("amount")).get("amount__sum")

    res["a_avg_alyssa"] = a_avg_alyssa = float(sum_alyssa) * (365/denom)

    sum_gifts = Trans.objects.filter(category__category__exact="gifts given").filter(tdate__gte=datetime.now()-timedelta(days=1000)).aggregate(Sum("amount")).get("amount__sum")

    res["a_avg_gifts"] = a_avg_gifts = float(sum_gifts) * (365/denom)

    res["a_total"] = a_post_var_inc + a_avg_alyssa + a_avg_gifts

    return render(response, "budgetresults.html", {"result":res})

  else:
    form = Budget(initial={"a_gross_pay": 212000, "a_gross_bonus": 75000, "a_al_taxable": 75000, "a_al_fwh": 9000, "a_al_swh": 3000, "bw_medical": -327.18, "bw_dental": -21.12, "bw_daycare": -96.15, "rate_sstax": -0.062, "rate_medicare": -0.0145, "rate_401k": -0.07, "w_train": -91.50, "rate_r401k": -0.02, "bw_arag": -5.76, "m_internet": -50, "m_phone": -200,  "m_electric": -150, "m_natgas": -50, "a_carins": -2800, "m_homeins": -333, "m_apple": -35, "m_cabin_mtg": -1033.26, "a_cabin_ptax": -694, "a_cabin_ins": -2046.71, "m_cabin_electric": -140, "m_cabin_cable": -300, "a_cabin_hoa": -300, "m_car": -637.18, "m_mtg": -4435.46, "a_ptax": -19420.32})

  return render(response, "budget.html", {"form":form})

def trans_data(request):
  tdata = Account.objects.all()

  tdf = read_frame(tdata)

  return render(request, 'pdtest.html', {'tdf': tdf})
