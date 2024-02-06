from django.shortcuts import render

from django.http import (
	HttpResponse,
	HttpResponseRedirect,
)

from django.urls import (
	reverse,
	reverse_lazy,
)

from django.db.models import (
#	F, 
	Sum, 
#	Window, 
#	Q, 	
#	Avg, 
#	Max, 
#	Count
)

from transactions.models import (
	Transaction,
	SubTransaction,
)

from matplotlib.backends.backend_agg import FigureCanvasAgg

from slick_reporting.views import (
       ReportView, 
       Chart
)

from slick_reporting.fields import (
       SlickReportField,
       ComputationField
)

import pandas as pd

import matplotlib.pyplot as plt

from django_pandas.io import read_frame 

from .forms import (
	TransQueryForm,
)

from datetime import datetime

pd.options.display.float_format = '{:,}'.format

# Create your views here.

### REPORTING ###

def qform(request):

	form = TransQueryForm
	template = 'reports/form.html'

	context = {
	
			"form": form,
	}
	
	if request.method == 'POST':
		form = TransQueryForm(request.POST)

		if form.is_valid():
			
			kwargs = {"gcat": "all", "ord": "-tdate"}

			if form.cleaned_data['sel_account']:
				kwargs["acc"] = form.cleaned_data['sel_account'].id
			else:
				kwargs["acc"] = 'all'

			if form.cleaned_data['sel_payee']:
				kwargs["pay"] = form.cleaned_data['sel_payee'].id
			else:
				kwargs["pay"] = 'all'

			if form.cleaned_data['sel_category']:
				kwargs["cat"] = form.cleaned_data['sel_category'].id
			else:
				kwargs["cat"] = 'all'

			if form.cleaned_data['sel_l1']:
				kwargs["l1"] = form.cleaned_data['sel_l1'].id
			else:
				kwargs["l1"] = 'all'

			if form.cleaned_data['sel_min_tdate']:
				kwargs["mindate"] = form.cleaned_data['sel_min_tdate']

			if form.cleaned_data['sel_max_tdate']:
				kwargs["maxdate"] = form.cleaned_data['sel_max_tdate']

			template = 'transactions/tlist.html'

			return HttpResponseRedirect(reverse_lazy('transactions:tlist', kwargs=kwargs))

	return render(request, template, context)

class SumValueComputationField(ComputationField):
	calculation_method = Sum
	calculation_field = "subtransaction__amount"
	verbose_name = ("Total")
	name = "amount_sum"


class TotalPerCategory(ReportView):
    report_model = Transaction
    date_field = "tdate"
    group_by = "subtransaction__groupedcat__l1group__l1group"
    columns = [
        "subtransaction__groupedcat__l1group__l1group",
        ComputationField.create(
            Sum, "subtransaction__amount", name="sum__value", verbose_name="Total"
        ),
    ]

    chart_settings = [
        Chart(
            "Total",
            Chart.COLUMN,
            data_source=["sum__value"],
            title_source=["subtransaction__groupedcat__l1group__l1group"],
        ),
        Chart(
            "Total",
            Chart.PIE,
            data_source=["sum__value"],
            title_source=["subtransaction__groupedcat__l1group__l1group"],
        ),
    ]


class MonthlyCashFlow(ReportView):
	report_model = Transaction
	date_field = "tdate"
	group_by = "subtransaction__groupedcat__l1group__l1group"
	columns = ["subtransaction__groupedcat__l1group__l1group"]


	time_series_pattern = "monthly"
	time_series_columns = [
		SumValueComputationField,
    	]

	chart_settings = [
		Chart(
			("Monthly Cash Flow"),
			Chart.COLUMN,
			data_source=["amount_sum"],
			title_source=["subtransaction__groupedcat__l1group__l1group"],
		),
	]


####   PANDAS  ####

def ptran(request):
	
	qs = Transaction.objects.all().values(
		"tdate",
		"subtransaction__groupedcat__category__category",
		"subtransaction__amount",
	)
	df = read_frame(qs)

	# Convert the 'tdate' column to a datetime series
	df['tdate'] = pd.to_datetime(df['tdate'])

	# Create a new 'month' column from the 'tdate' column
	df['year'] = df['tdate'].dt.to_period('Y')

	# Pivot the DataFrame to group data by 'month' and 'category_id', and calculate the sum of 'amount'
	pt = pd.pivot_table(df, values='subtransaction__amount', index='year', columns='subtransaction__groupedcat__category__category', aggfunc='sum', fill_value=0).astype(float)

	pt.loc[:,'Total H'] = pt.sum(axis=1).round(0).astype(float)
	pt.loc['Total']= pt.sum().round(0).astype(float)

	# Reset the index to have 'month' as a regular column
	pt = pt.reset_index()

	pt = pt.iloc[:, :].reset_index(drop=True)

	# Convert the pivot table to an HTML table
	pivot_data = pt.to_html(
		index=False,
		index_names=False,
		escape=False, 
		justify="center",
		formatters={'numbers': '{:,2f}'.format}
	)
	
	
	context = {
		'pivot' : pivot_data,
	}

	return render(request, "reports/ptran.html", context)


#GRAPH


def testg(request, acc='all', cat='all', pay='all', l1='all', mindate=None, maxdate=None, **kwargs):
	
	if maxdate == None:
		maxdate = datetime.today().strftime('%Y-%m-%d')

	filters = {}

	if acc != 'all':
		filters['account'] = acc

	if cat != 'all':
		filters['subtransaction__groupedcat__category'] = cat
	
	if pay != 'all':
		filters['payee'] = pay

	if l1 != 'all':
		filters['subtransaction__groupedcat__l1group'] = l1
	
	if mindate is not None:
		filters['tdate__range'] = [mindate, maxdate]

	trans_query = Transaction.objects.all()

	if filters:
		trans_query = trans_query.filter(**filters)


	qs = trans_query.values(
		"tdate",
		"subtransaction__groupedcat__category__category",
		"subtransaction__amount",
	)

	df = read_frame(qs)

	# Convert the 'tdate' column to a datetime series
	df['tdate'] = pd.to_datetime(df['tdate'])

	# Create a new 'year' column from the 'tdate' column
	df['year'] = df['tdate'].dt.to_period('Y')
	
	# Convert the 'year' column to a string
	df['year'] = df['year'].astype(str)
	df['year'] = df['year'].str[2:]

	# Pivot the DataFrame to group data by 'year' and 'category_id', and calculate the sum of 'amount'
	pt = pd.pivot_table(df, values='subtransaction__amount', index='year', columns='subtransaction__groupedcat__category__category', aggfunc='sum', fill_value=0).astype(float)

	# Reset the index to have 'month' as a regular column
	pt = pt.reset_index()
		
	#pt = pt[['year', 'work food']]

	fig, ax = plt.subplots()
	
	# Plot the data
	for column in pt.columns[1:]:
		ax.bar(pt['year'], pt[column], label=f'subtransaction__groupedcat {column}')

	ax.set(xlabel='Year', ylabel='Total Amount',
		title='Total Amount by Year and subtransaction__groupedcat')
	
	ax.legend(loc='lower center')
	
	ax.grid()
	
	response = HttpResponse(content_type = 'image/png')
	
	canvas = FigureCanvasAgg(fig)
	
	canvas.print_png(response)
	
	return response
	
	
	### TCHART ###


def tchart(request, acc='all', cat='all', pay='all', l1='all', mindate=None, maxdate=None, **kwargs):
	
	if maxdate == None:
		maxdate = datetime.today().strftime('%Y-%m-%d')

	filters = {}

	if acc != 'all':
		filters['account'] = acc

	if cat != 'all':
		filters['subtransaction__groupedcat__category'] = cat
	
	if pay != 'all':
		filters['payee'] = pay

	if l1 != 'all':
		filters['subtransaction__groupedcat__l1group'] = l1
	
	if mindate is not None:
		filters['tdate__range'] = [mindate, maxdate]

	trans_query = Transaction.objects.all()

	if filters:
		trans_query = trans_query.filter(**filters)


	qs = trans_query.values(
		"tdate",
		"subtransaction__groupedcat__category__category",
		"subtransaction__amount",
	)
	df = read_frame(qs)

	# Convert the 'tdate' column to a datetime series
	df['tdate'] = pd.to_datetime(df['tdate'])

	# Create a new 'month' column from the 'tdate' column
	df['year'] = df['tdate'].dt.to_period('Y')

	# Pivot the DataFrame to group data by 'month' and 'category_id', and calculate the sum of 'amount'
	pt = pd.pivot_table(df, values='subtransaction__amount', index='year', columns='subtransaction__groupedcat__category__category', aggfunc='sum', fill_value=0).astype(float)

	pt.loc[:,'Total H'] = pt.sum(axis=1).round(0).astype(float)
	pt.loc['Total']= pt.sum().round(0).astype(float)

	# Reset the index to have 'month' as a regular column
	pt = pt.reset_index()

	pt = pt.iloc[:, :].reset_index(drop=True)

	# Convert the pivot table to an HTML table
	pivot_data = pt.to_html(
		index=False,
		index_names=False,
		escape=False, 
		justify="center",
		formatters={'numbers': '{:,2f}'.format}
	)
	
	
	context = {
		'pivot' : pivot_data,
	}

	return render(request, "reports/ptran.html", context)
	
def qpdform(request):

	form = TransQueryForm
	template = 'reports/form.html'

	context = {
	
			"form": form,
	}
	
	if request.method == 'POST':
		form = TransQueryForm(request.POST)

		if form.is_valid():
			
			kwargs={}
			
			if form.cleaned_data['sel_account']:
				kwargs["acc"] = form.cleaned_data['sel_account'].id
			else:
				kwargs["acc"] = 'all'

			if form.cleaned_data['sel_payee']:
				kwargs["pay"] = form.cleaned_data['sel_payee'].id
			else:
				kwargs["pay"] = 'all'

			if form.cleaned_data['sel_category']:
				kwargs["cat"] = form.cleaned_data['sel_category'].id
			else:
				kwargs["cat"] = 'all'

			if form.cleaned_data['sel_l1']:
				kwargs["l1"] = form.cleaned_data['sel_l1'].id
			else:
				kwargs["l1"] = 'all'

			if form.cleaned_data['sel_min_tdate']:
				kwargs["mindate"] = form.cleaned_data['sel_min_tdate']

			if form.cleaned_data['sel_max_tdate']:
				kwargs["maxdate"] = form.cleaned_data['sel_max_tdate']

			return HttpResponseRedirect(reverse_lazy('reports:tchart', kwargs=kwargs))

	return render(request, template, context)



def qgform(request):

	form = TransQueryForm
	template = 'reports/form.html'

	context = {
	
		"form": form,
	}
	
	if request.method == 'POST':
		form = TransQueryForm(request.POST)

		if form.is_valid():
			
			kwargs={}
			
			if form.cleaned_data['sel_account']:
				kwargs["acc"] = form.cleaned_data['sel_account'].id
			else:
				kwargs["acc"] = 'all'

			if form.cleaned_data['sel_payee']:
				kwargs["pay"] = form.cleaned_data['sel_payee'].id
			else:
				kwargs["pay"] = 'all'

			if form.cleaned_data['sel_category']:
				kwargs["cat"] = form.cleaned_data['sel_category'].id
			else:
				kwargs["cat"] = 'all'

			if form.cleaned_data['sel_l1']:
				kwargs["l1"] = form.cleaned_data['sel_l1'].id
			else:
				kwargs["l1"] = 'all'

			if form.cleaned_data['sel_min_tdate']:
				kwargs["mindate"] = form.cleaned_data['sel_min_tdate']

			if form.cleaned_data['sel_max_tdate']:
				kwargs["maxdate"] = form.cleaned_data['sel_max_tdate']

			return HttpResponseRedirect(reverse_lazy('reports:tg', kwargs=kwargs))

	return render(request, template, context)