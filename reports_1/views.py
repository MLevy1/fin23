from django.shortcuts import render

from .forms import TransListForm

from django.http import (
	HttpResponseRedirect,
)

from django.urls import (
	reverse_lazy,
)

from datetime import datetime

from transactions.models import (
	Transaction
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