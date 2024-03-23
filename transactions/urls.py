from django.urls import (
	path,
)

from .views import (
	#T2
	Transaction_create_view,
	#T3
	tlist,
	#T4
	Transaction_update_view,
    #T5
	Transaction_delete_view,
    #T6
	Transaction_subtran_update_hx_view,
	#T7
	TransSubTrans_delete_view,
    #T8
    Transfer_create_view,
    #T10
    add_staged_trans,
    #T11
    add_fixed,
	#T12
    transactionMonthArchiveView,
    #T13
    TransYearArchiveView,
    #T14
	Transaction_detail_view,

)

from django.views.generic.dates import ArchiveIndexView

from .models import Transaction

app_name = 'transactions'

urlpatterns = [
	path("", ArchiveIndexView.as_view(model=Transaction, template_name = "transactions/trans_years.html", date_field="tdate"), name="list"),
	path('archive/', ArchiveIndexView.as_view(model=Transaction, date_field="tdate", template_name="trans_years.html"), name='trans-years'),
	path("create/", Transaction_create_view, name='create'),
	path("tlist/<str:acc>/<str:cat>/<str:gcat>/<str:pay>/<str:l1>/<str:ord>/<mindate>/<maxdate>/", tlist, name="tlist"),
	path("tlist/<str:acc>/<str:cat>/<str:gcat>/<str:pay>/<str:l1>/<str:ord>/<mindate>/", tlist, name="tlist"),
	path("tlist/<str:acc>/<str:cat>/<str:gcat>/<str:pay>/<str:l1>/<str:ord>/", tlist, name="tlist"),
	path("tlist/<str:acc>/<str:cat>/<str:gcat>/<str:pay>/", tlist, name="tlist"),
	path("tlist/<str:acc>/", tlist, name="tlist"),
	path("tlist/", tlist, name="tlist"),
	path("<int:id>/edit/", Transaction_update_view, name='update'),
	path("<int:id>/delete/", Transaction_delete_view, name='delete'),
	path("hx/<int:parent_id>/subtran/<int:id>/", Transaction_subtran_update_hx_view, name='hx-subtran-update'),
	path("hx/<int:parent_id>/subtran/", Transaction_subtran_update_hx_view, name='hx-subtran-create'),
	path("<int:parent_id>/subtran/<int:id>/delete/", TransSubTrans_delete_view, name='subtran-delete'),
	path("transfer/", Transfer_create_view, name='transfer'),
	path('import/<st>/', add_staged_trans, name='add-staged-trans'),
	path('fixed/<flow>/', add_fixed, name='add-fixed'),
	path('tmonth/<int:year>/<int:month>/', transactionMonthArchiveView.as_view(month_format='%m'), name="trans-monthly"),
	path('tyear/<int:year>/', TransYearArchiveView.as_view(), name="trans-months"),
	path("<int:id>/", Transaction_detail_view, name='detail'),
]