from django.urls import (
	path,
)

from .views import (
    flow_list_view,
    flow_detail_view,
    flow_create_view,
    flow_update_view,
    flow_item_update_hx_view,
    flow_delete_view,
    item_delete_view,
)

app_name = 'fixed'

urlpatterns = [
    #F1 [master][delete][form]
	path("", flow_list_view, name="list"),
	#F2 [list]
	path("create/", flow_create_view, name="create"),
	#F3 [mFlow-edit][list][detail]
	path("<int:id>/edit/", flow_update_view, name="update"),
	#F4 [mFlow-abs]
	path("<int:id>/", flow_detail_view, name="detail"),
	#F5 [mFlowItem-hx-edit][list][item-inline]
	path("hx/<int:parent_id>/item/<int:id>/", flow_item_update_hx_view, name="item_update_hx"),
	path("hx/<int:parent_id>/item/", flow_item_update_hx_view, name="item_create_hx"),
	#F7 [mFlow-delete]
	path("<int:id>/delete/", flow_delete_view, name='delete'),
	#F8 [mFlowItem-delete][item-inline]
	path("<int:parent_id>/subtran/<int:id>/delete/", item_delete_view, name='item-delete'),

]