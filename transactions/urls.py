from django.urls import (
	path,
	reverse,
)

from .views import (
	Transaction_list_view,
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
)

from django.views.generic.dates import ArchiveIndexView

from .models import Transaction, SubTransaction

app_name = 'transactions'

urlpatterns = [
	path("", ArchiveIndexView.as_view(model=Transaction, template_name = "transactions/trans_years.html", date_field="tdate"), name="list"),
	path("create/", Transaction_create_view, name='create'),
	path("<int:id>/edit/", Transaction_update_view, name='update'),
	path("hx/<int:parent_id>/subtran/<int:id>/", Transaction_subtran_update_hx_view, name='hx-subtran-update'),
	path("hx/<int:parent_id>/subtran/", Transaction_subtran_update_hx_view, name='hx-subtran-create'),
	path("hx/<int:id>/", Transaction_detail_hx_view, name='hx-detail'),
	path("<int:id>/delete/", Transaction_delete_view, name='delete'),
	path("<int:parent_id>/subtran/<int:id>/delete/", TransSubTrans_delete_view, name='subtran-delete'),
	path("<int:id>/", Transaction_detail_view, name='detail'),
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
	
]