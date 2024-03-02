from django.urls import (
	path,
)

from .views import (
	Transaction_detail_view,
	Transaction_create_view,
	Transaction_update_view,
	Transaction_detail_hx_view,
	Transaction_subtran_update_hx_view,
	Transaction_delete_view,
	TransSubTrans_delete_view,
	TransDeleteView,
    TransYearArchiveView,
    transactionMonthArchiveView,
    tlist,
    atran,
    utran,
    utran_act,
    Transfer_create_view,
    CC_Pmt_create_view,
    add_staged_trans,
    paycheck_list_view,
    paycheck_detail_view,
    paycheck_create_view,
    paycheck_update_view,
    paycheck_item_update_hx_view,
)

from django.views.generic.dates import ArchiveIndexView

from .models import Transaction

app_name = 'transactions'

urlpatterns = [
	path("", ArchiveIndexView.as_view(model=Transaction, template_name = "transactions/trans_years.html", date_field="tdate"), name="list"),
	path("create/", Transaction_create_view, name='create'),
	path("transfer/", Transfer_create_view, name='transfer'),
	path("ccpmt/", CC_Pmt_create_view, name='cc-pmt'),
	path("<int:id>/edit/", Transaction_update_view, name='update'),
	path("hx/<int:parent_id>/subtran/<int:id>/", Transaction_subtran_update_hx_view, name='hx-subtran-update'),
	path("hx/<int:parent_id>/subtran/", Transaction_subtran_update_hx_view, name='hx-subtran-create'),
	path("hx/<int:id>/", Transaction_detail_hx_view, name='hx-detail'),
	path("<int:id>/delete/", Transaction_delete_view, name='delete'),
	path("<int:parent_id>/subtran/<int:id>/delete/", TransSubTrans_delete_view, name='subtran-delete'),
	path("<int:id>/", Transaction_detail_view, name='detail'),
	path("tlist/<str:acc>/<str:cat>/<str:gcat>/<str:pay>/<str:l1>/<str:ord>/<mindate>/<maxdate>/", tlist, name="tlist"),
	path("tlist/<str:acc>/<str:cat>/<str:gcat>/<str:pay>/<str:l1>/<str:ord>/<mindate>/", tlist, name="tlist"),
	path("tlist/<str:acc>/<str:cat>/<str:gcat>/<str:pay>/<str:l1>/<str:ord>/", tlist, name="tlist"),
    path("tlist/<str:acc>/<str:cat>/<str:gcat>/<str:pay>/", tlist, name="tlist"),
	path("tlist/", tlist, name="tlist"),
    path('archive/', ArchiveIndexView.as_view(model=Transaction, date_field="tdate", template_name="trans_years.html"), name='trans-years'),
	path('tmonth/<int:year>/<int:month>/', transactionMonthArchiveView.as_view(month_format='%m'), name="trans-monthly"),
	path('tyear/<int:year>/', TransYearArchiveView.as_view(), name="trans-months"),
	path("atran/<dpay>/", atran, name="add-trans"),
	path("atran/", atran, name="add-trans"),
	path("utran/<int:t_id>/", utran, name="update-trans"),
    path("utran_act/<int:t_id>/", utran_act, name="update-trans-act"),
	path('trans/<int:pk>/delete/', TransDeleteView.as_view(), name='delete-trans'),
	path('import/<st>/', add_staged_trans, name='add-staged-trans'),
	path("paycheck/", paycheck_list_view, name="paycheck-list"),
	path("paycheck/create/", paycheck_create_view, name="paycheck-create"),
	path("paycheck/<int:id>/edit/", paycheck_update_view, name="paycheck-update"),
	path("paycheck/<int:id>/", paycheck_detail_view, name="paycheck-detail"),
	path("paycheck/hx/<int:parent_id>/item/<int:id>/", paycheck_item_update_hx_view, name="paycheck_item_update_hx"),
	path("paycheck/hx/<int:parent_id>/item/", paycheck_item_update_hx_view, name="paycheck_item_create_hx"),

]