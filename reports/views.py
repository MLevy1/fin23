from django.shortcuts import render

from django.http import HttpResponse

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

pd.options.display.float_format = '{:,}'.format

# Create your views here.

### REPORTING ###

def qform(request):
	form = TransQueryForm
	template = 'reports/form.html'
	context = {
	
			"form": form,
	}
	
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


def testg(request):
	
	qs = Transaction.objects.all().values(
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
	
	#pt = pt.drop(columns=["waxhaw house", "middletown house purchase", "sunset beach condo", "concord house", "ga rental property", "tn rental property", "investments", "income"])
	
	pt = pt[['year', 'groceries']]

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