from django.urls import (
	path,
)

from .views import (
    upload_file,
    imported_payee_ListView,
    imported_payee_UpdateView,
    staged_transaction_ListView,

)

app_name = 'csv'

urlpatterns = [
    path('', upload_file, name='upload-file'),
    path('imported-payees/', imported_payee_ListView.as_view(), name='imported-payees-list'),
    path('staged-transactions/', staged_transaction_ListView.as_view(), name='staged-transactions-list'),
    path('imported-payees/update/<pk>/', imported_payee_UpdateView.as_view(), name='imported-payee-update'),
]