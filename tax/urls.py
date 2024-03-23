from django.urls import (
	path,
)

from .views import (
    index,
    TaxReturn_create_view,
    TaxReturn_list_view,
    TaxReturn_detail_view,
    TaxReturn_update_view,
    TaxReturn_delete_view,
    TaxReturnForm_create_view,
    TaxReturnForm_detail_view,
    TaxReturnForm_update_view,
    TaxReturnForm_delete_view,
    TaxReturnFormLine_create_view,
    TaxReturnFormLine_detail_view,
    TaxReturnFormLine_update_view,
    TaxReturnFormLine_delete_view,
    TaxReturnFormLineInput_create_view,
    TaxReturnFormLineInput_update_view,
    TaxReturnFormLineInput_delete_view,
    InputValue_create_view,
    InputValue_update_view,
    InputValue_delete_view,
    DataSource_list_view,
    DataSource_create_view,
    DataSource_detail_view,
    DataSource_update_view,
    DataSource_delete_view,

)

app_name = 'tax'

urlpatterns = [
    path("", index, name="index"),
    path("TaxReturn/create/", TaxReturn_create_view, name="tax-return-create"),
    path("TaxReturn/update/<id>/", TaxReturn_update_view, name="tax-return-update"),
    path("TaxReturn/list/", TaxReturn_list_view, name="tax-return-list"),
    path("TaxReturn/detail/<id>/", TaxReturn_detail_view, name="tax-return-detail"),
    path("TaxReturn/delete/<id>/", TaxReturn_delete_view, name="tax-return-delete"),
    path("TaxReturn/Form/create/<p_id>/", TaxReturnForm_create_view, name="tax-return-form-create"),
    path("TaxReturn/Form/detail/<id>/", TaxReturnForm_detail_view, name="tax-return-form-detail"),
    path("TaxReturn/Form/update/<id>/", TaxReturnForm_update_view, name="tax-return-form-update"),
    path("TaxReturn/Form/delete/<id>/", TaxReturnForm_delete_view, name="tax-return-form-delete"),
    path("TaxReturn/Form/Line/create/<p_id>/", TaxReturnFormLine_create_view, name="tax-return-form-line-create"),
    path("TaxReturn/Form/Line/detail/<id>/", TaxReturnFormLine_detail_view, name="tax-return-form-line-detail"),
    path("TaxReturn/Form/Line/update/<id>/", TaxReturnFormLine_update_view, name="tax-return-form-line-update"),
    path("TaxReturn/Form/Line/delete/<id>/", TaxReturnFormLine_delete_view, name="tax-return-form-line-delete"),
    path("TaxReturn/Form/Line/Input/create/<p_id>/", TaxReturnFormLineInput_create_view, name="tax-return-form-line-input-create"),
    path("TaxReturn/Form/Line/Input/update/<id>/", TaxReturnFormLineInput_update_view, name="tax-return-form-line-input-update"),
    path("TaxReturn/Form/Line/Input/delete/<id>/", TaxReturnFormLineInput_delete_view, name="tax-return-form-line-input-delete"),
    path("InputValue/create/<p_id>/", InputValue_create_view, name="inputvalue-create"),
    path("InputValue/update/<id>/", InputValue_update_view, name="inputvalue-update"),
    path("InputValue/delete/<id>/", InputValue_delete_view, name="inputvalue-delete"),
    path("DataSource/list/", DataSource_list_view, name="datasource-list"),
    path("DataSource/create/", DataSource_create_view, name="datasource-create"),
    path("DataSource/detail/<id>/", DataSource_detail_view, name="datasource-detail"),
    path("DataSource/update/<id>/", DataSource_update_view, name="datasource-update"),
    path("DataSource/delete/<id>/", DataSource_delete_view, name="datasource-delete"),

]


