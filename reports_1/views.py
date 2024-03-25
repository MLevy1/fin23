from django.shortcuts import render

from .forms import (
    TransListForm,
    TransSummaryForm,
)

from django.http import (
	HttpResponseRedirect,
)

from django.urls import (
	reverse_lazy,
)

from datetime import datetime

from transactions.models import (
	Transaction,
	SubTransaction,
)

from django.db.models import (
	F,
	Sum,
	Window,
	Avg,
	Min,
	Max,
)

from django.core.paginator import Paginator

# Create your views here.
def index(request):
    template="reports_1/main.html"
    return render(request, template)

def tform(request, act=True):

    form = TransListForm(request.POST, aAct=act, pAct=act)

    template="reports_1/form.html"

    context={
        "form": form,
        "title": "Transaction Query",
    }

    if request.method == "POST":

        if form.is_valid():

            kwargs = {"gcat": "all", "ord": "-tdate"}

            if form.cleaned_data['i_acct']:
                kwargs["acc"] = form.cleaned_data['i_acct'].id
            else:
                kwargs["acc"] = 'all'

            if form.cleaned_data['i_payee']:
                kwargs["pay"] = form.cleaned_data['i_payee'].id
            else:
                kwargs["pay"] = 'all'

            if form.cleaned_data['i_cat']:
                kwargs["cat"] = form.cleaned_data['i_cat'].id
            else:
                kwargs["cat"] = 'all'

            if form.cleaned_data['i_l1']:
                kwargs["l1"] = form.cleaned_data['i_l1'].id
            else:
                kwargs["l1"] = 'all'

            if form.cleaned_data['i_min_tdate']:
                kwargs["mindate"] = form.cleaned_data['i_min_tdate']

            if form.cleaned_data['i_max_tdate']:
                kwargs["maxdate"] = form.cleaned_data['i_max_tdate']

            template = 'reports_1/treport.html'

            return HttpResponseRedirect(reverse_lazy('reports_1:treport', kwargs=kwargs))

    return render(request, template, context)

def stform(request):
    
    form = TransSummaryForm(request.POST or None)
    
    template = "reports_1/form.html"

    context = {

        "form": form
    }

    if request.method == "POST":
        if form.is_valid():

            kwargs = {}
            
            kwargs["group"] = form.cleaned_data['i_group']
            kwargs["active"] = form.cleaned_data['i_active']
            kwargs["mindate"] = form.cleaned_data['i_min_tdate']
            kwargs["maxdate"] = form.cleaned_data['i_max_tdate']

            template = 'reports_1/tsummary.html'

            return HttpResponseRedirect(reverse_lazy('reports_1:streport', kwargs=kwargs))

    return render(request, template, context)

def streport(request, group="p", active=True, mindate=None, maxdate=None):
    
    if maxdate == None:
        maxdate = datetime.today().strftime('%Y-%m-%d')

    filters = {}

    if mindate is not None:
        filters['trans__tdate__range'] = [mindate, maxdate]

    if active == "True":
        filters['groupedcat__category__active'] = True
        filters['groupedcat__active'] = True
        filters['groupedcat__l1group__active'] = True

    sq = SubTransaction.objects.all().order_by('-trans__tdate')

    if filters:
        sq = sq.filter(**filters)

    mnd = sq.aggregate(Min('trans__tdate'))
    mnd = mnd['trans__tdate__min']
    mxd = sq.aggregate(Max('trans__tdate'))
    mxd = mxd['trans__tdate__max']

    dys = (mxd-mnd).days
    anpct = 365/dys

    sqc = sq.count()

    obj = {}
    aobj = {}

    if group == "gc":
        for s in sq:
            if s.groupedcat not in obj:
                obj[s.groupedcat]=s.amount
                aobj[s.groupedcat]=(float(s.amount)*anpct)/12
            else:
                obj[s.groupedcat]+=s.amount
                aobj[s.groupedcat]+=(float(s.amount)*anpct)/12
    elif group == "c":
        for s in sq:
            if s.groupedcat.category not in obj:
                obj[s.groupedcat.category]=s.amount
                aobj[s.groupedcat.category]=(float(s.amount)*anpct)/12
            else:
                obj[s.groupedcat.category]+=s.amount
                aobj[s.groupedcat.category]+=(float(s.amount)*anpct)/12
    elif group =="p":
        for s in sq:
            if s.trans.payee not in obj:
                obj[s.trans.payee]=s.amount
                aobj[s.trans.payee]=(float(s.amount)*anpct)/12
            else:
                obj[s.trans.payee]+=s.amount
                aobj[s.trans.payee]+=(float(s.amount)*anpct)/12

    pobj = {}
    ptot = 0

    nobj = {}
    ntot = 0

    paobj = {}
    patot = 0

    naobj = {}
    natot = 0

    for k, v in obj.items():
        if v < 0:
            ntot +=v
            if k not in nobj:
                nobj[k] = v
            else:
                nobj[k] += v
        else:
            ptot +=v
            if k not in pobj:
                pobj[k] = v
            else:
                pobj[k] += v            

    for k, v in aobj.items():
        if v < 0:
            natot +=v
            if k not in naobj:
                naobj[k] = v
            else:
                naobj[k] += v
        else:
            patot +=v
            if k not in paobj:
                paobj[k] = v
            else:
                paobj[k] += v        

    slist = sorted(obj.items(), key=lambda x:x[1], reverse=True)
    alist = sorted(aobj.items(), key=lambda x:x[1], reverse=True)

    plist = sorted(pobj.items(), key=lambda x:x[1], reverse=True)
    nlist = sorted(nobj.items(), key=lambda x:x[1])

    palist = sorted(paobj.items(), key=lambda x:x[1], reverse=True)
    nalist = sorted(naobj.items(), key=lambda x:x[1])

    sobj = dict(slist)
    saobj = dict(alist)

    spobj = dict(plist)
    npobj = dict(nlist)

    spaobj = dict(palist)
    npaobj = dict(nalist)

    template='reports_1/tsummary.html'

    context = {

        "obj": sobj,
        "aobj": saobj,
        "spobj": spobj,
        "npobj": npobj,
        "spaobj": spaobj,
        "npaobj": npaobj,
        "cnt": sqc,
        "mnd": mnd,
        "mxd": mxd,
        "dys": dys,
        "ptot": ptot,
        "ntot": ntot,
        "patot": patot,
        "natot": natot,

    }

    return render(request, template, context)

def treport(request, acc='all', cat='all', gcat='all', pay='all', l1='all', ord='-tdate', mindate=None, maxdate=None, **kwargs):

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

	t_avg = trans_query.aggregate(Avg('subtransaction__amount'))
	t_sum = trans_query.aggregate(Sum('subtransaction__amount'))
	mnd = trans_query.aggregate(Min('tdate'))
	mxd = trans_query.aggregate(Max('tdate'))
	mxd = mxd['tdate__max']
	mnd = mnd['tdate__min']
	dr = mxd-mnd
	pd = t_sum['subtransaction__amount__sum'] / dr.days
	pw = pd*7
	py = pd*365
	pm =py/12

	template="reports_1/treport.html"

	trans_list = list(trans_query)

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
		"tqcnt": tqcnt,
		"t_avg": t_avg['subtransaction__amount__avg'],
		"t_sum": t_sum['subtransaction__amount__sum'],
		"dr": dr.days,
		"pd": pd,
		"pw": pw,
		"pm": pm,
		"py": py,
	}

	return render(request, template, context)