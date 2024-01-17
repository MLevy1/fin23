from django.urls import (
	path,
	reverse,
)

from reports.views import (
	TotalPerCategory,
	MonthlyCashFlow,
	ptran,
	testg,
	qform,
)

app_name = 'reports'

urlpatterns = [

	path('pd/', ptran, name="pd-trans"),
	path("mrep/", MonthlyCashFlow.as_view(), name ="mrep"),
	path("gby/", TotalPerCategory.as_view(), name="gby"),
	path("g/", testg, name="g"),
	path("qform/", qform, name="qform"),
]