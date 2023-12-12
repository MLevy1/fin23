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
       load_groupedcats,
)

from django.views.generic.dates import ArchiveIndexView
from .models import Transaction, SubTransaction

app_name = 'transactions'
urlpatterns = [
	path("", ArchiveIndexView.as_view(model=Transaction, template_name = "transactions/trans_years.html", date_field="tdate"), name="list"),
	#path("", Transaction_list_view, name='list'),
	path("create/", Transaction_create_view, name='create'),
	path("<int:id>/edit/", Transaction_update_view, name='update'),
	path("hx/<int:parent_id>/subtran/<int:id>/", Transaction_subtran_update_hx_view, name='hx-subtran-update'),
	path("hx/<int:parent_id>/subtran/", Transaction_subtran_update_hx_view, name='hx-subtran-create'),
	path("hx/<int:id>/", Transaction_detail_hx_view, name='hx-detail'),
	path("<int:id>/delete/", Transaction_delete_view, name='delete'),
	path("<int:parent_id>/subtran/<int:id>/delete/", TransSubTrans_delete_view, name='subtran-delete'),
	path("<int:id>/", Transaction_detail_view, name='detail'),
       path("load-gc/", load_groupedcats, name="load-gc")
	
]