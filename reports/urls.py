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
	tchart,
	qpdform,
	qgform,
)

app_name = 'reports'

urlpatterns = [

	path('pd/', ptran, name="pd-trans"),
	path("mrep/", MonthlyCashFlow.as_view(), name ="mrep"),
	path("gby/", TotalPerCategory.as_view(), name="gby"),
	path("g/", testg, name="g"),
	path("qform/", qform, name="qform"),
	path("qpdform/", qpdform, name="qpdform"),
	path("qgform/", qgform, name="qgform"),
	path("tchart/<acc>/<cat>/<pay>/<l1>/<mindate>/<maxdate>/", tchart, name="tchart"),
	path("tchart/<acc>/<cat>/<pay>/<l1>/", tchart, name="tchart"),
	path("tg/<acc>/<cat>/<pay>/<l1>/<mindate>/<maxdate>/", testg, name="tg"),
	path("tg/<acc>/<cat>/<pay>/<l1>/", testg, name="tg"),
	
]