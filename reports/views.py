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

from fin.models import Trans

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

pd.options.display.float_format = '{:,}'.format

# Create your views here.

### REPORTING ###

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


####   PANDAS  ####

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

	return render(request, "reports/ptran.html", context)

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