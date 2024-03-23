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
    #C1
    path('', upload_file, name='upload-file'),
    #C2
    path('imported-payees/', imported_payee_ListView.as_view(), name='imported-payees-list'),
    #C3
    path('staged-transactions/', staged_transaction_ListView.as_view(), name='staged-transactions-list'),
    #C4
    path('imported-payees/update/<pk>/', imported_payee_UpdateView.as_view(), name='imported-payee-update'),
]