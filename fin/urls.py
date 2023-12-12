from django.urls import path

from . import views

from .views import (
	PayeeDetailView, 
	L1GroupUpdateView, 
	L1GroupListView, 
	L1GroupCreateView, 
	CatListView, 
	UpdateCategory, 
	UpdateAccount, 
	SearchResultsView, 
	PayeeCreateView, 
	AccountCreateView, 
	CatCreateView, 
	UpdatePayee, 
	PayeeDeleteView, 
	GroupedCatListView, 
	GroupedCatCreateView, 
	GroupedCatUpdateView, 
	GroupedCatDeleteView,
	CatSearchView,
)

urlpatterns = [

	path('', views.main, name='main'),
	
	path('act/<str:a>/', views.accounts, name='list-accounts'),
	path("aact/", AccountCreateView.as_view(), name="add-account"),
	path("uact/<pk>/", UpdateAccount.as_view(), name="update-account"),
	
	path('cat/', CatListView.as_view(), name='list-categories'),
	path("acat/", CatCreateView.as_view(), name="add-category"),
	path("ucat/<pk>/", UpdateCategory.as_view(), name="update-category"),
	path("csearch/", CatSearchView.as_view(), name="results-category"),
	
       path("l1g/", L1GroupListView.as_view(), name="list-l1groups"),       
       path("al1g/", L1GroupCreateView.as_view(), name="add-l1group"),
       path("ul1g/<pk>/", L1GroupUpdateView.as_view(), name="update-l1group"),

       path("gc/", GroupedCatListView.as_view(), name="list-gc"),       
       path("agc/", GroupedCatCreateView.as_view(), name="add-gc"),
       path("ugc/<pk>/", GroupedCatUpdateView.as_view(), name="update-gc"),
       path("dgc/<pk>/", GroupedCatDeleteView.as_view(), name="delete-gc"),
       path("pgcua/<dpay>/", views.payee_groupedcat_update_all, name="payee-gc-update-all"),
       path("cgcua/<dcat>/", views.category_groupedcat_update_all, name="category-gc-update-all"),

	path('pay/<str:a>/<str:o>/', views.payees, name='list-payees'),
	path('apay/', PayeeCreateView.as_view(), name="add-payee"),
	path("upay/<pk>/", UpdatePayee.as_view(), name="update-payee"),
	path("paydet/<pk>/", PayeeDetailView.as_view(), name="payee-detail"),
       path("search/", SearchResultsView.as_view(), name="results"),
	path('payee/<int:pk>/make_inactive/', views.make_inactive, name='make-payee-inactive'),
       path('payee/<int:pk>/delete/', PayeeDeleteView.as_view(), name='delete-payee'),
	path("merge/<dpay>/", views.merge_payees, name="merge"),
	path("merge/", views.merge_payees, name="merge"),
	path('qupdate/', views.payee_category_update, name="payee-category-update"),
       path('pcupdateall/<dpay>/', views.payee_category_update_all, name="payee-category-update-all"),
	path('pau/', views.payee_account_update, name="payee-account-update"),
	path("load-c/", views.load_c, name="load-c"),
       path("load-gc/", views.load_gc, name="load-gc"),

]
