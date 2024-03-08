from django.urls import (
	path,
)

from .views import (
    index,
    TaxReturn_list_view,
    TaxReturn_create_view,
    TaxReturn_update_view,
    TaxReturn_delete_view,
    TaxReturn_detail_view,
    TaxReturnForm_create_view,

)

app_name = 'tax'

urlpatterns = [
    path("", index, name="index"),
    path("TaxReturn/create/", TaxReturn_create_view, name="tax-return-create"),
    path("TaxReturn/update/<id>/", TaxReturn_update_view, name="tax-return-update"),
    path("TaxReturn/list/", TaxReturn_list_view, name="tax-return-list"),
    path("TaxReturn/detail/<id>/", TaxReturn_detail_view, name="tax-return-detail"),
    path("TaxReturn/delete/<id>/", TaxReturn_delete_view, name="tax-return-delete"),
    path("TaxReturn/Form/create/<parent_id>/", TaxReturnForm_create_view, name="tax-return-form-create"),
    path("TaxReturn/Form/list/<parent_id>/", TaxReturn_list_view, name="tax-return-form-list"),


]


