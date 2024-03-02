from django.urls import path

from .views import (
	#MAIN
	#1 m
	main,

	#ACCOUNT
	#2 m f
	accounts,
	#3 m f
	AccountCreateView,
	#4
	UpdateAccount,

	#CATEGORY
	#5 m
	CatListView,
	#6 m
	CatCreateView,
	#7
	UpdateCategory,
	#11
	category_groupedcat_update_all,
	#8
	CatSearchView,
	#29
	load_c,

	#l1GROUP
	#9 m
	L1GroupListView,
	#22 m
	L1GroupCreateView,
	#15
	L1GroupUpdateView,

	#GROUPED CAT
	#19 m
	GroupedCatListView,
	#12
	GroupedCatCreateView,
	#20
	GroupedCatUpdateView,
	#21
	GroupedCatDeleteView,
	#30
	load_gc,

	#PAYEE
	#13 m
	payees,
	#23 m
	PayeeCreateView,
	#25
	UpdatePayee,
	#26
	PayeeDeleteView,
	#27
	make_inactive,
	#14
	merge_payees,
	#17 m
	payee_category_update_all,
	#10
	payee_groupedcat_update_all,
	#18 m
	payee_account_update,
	#28
	SearchResultsView,
	#24
	PayeeDetailView,
)

urlpatterns = [

	#MAIN
	#1
	path('', main, name='main'),

	#ACCOUNT
	#2
	path('act/<str:a>/', accounts, name='list-accounts'),
	#3
	path("aact/", AccountCreateView.as_view(), name="add-account"),
	#4
	path("uact/<pk>/", UpdateAccount.as_view(), name="update-account"),

	#CATEGORY
	#5
	path('cat/', CatListView.as_view(), name='list-categories'),
	#6
	path("acat/", CatCreateView.as_view(), name="add-category"),
	#7
	path("ucat/<pk>/", UpdateCategory.as_view(), name="update-category"),
	#11
    path("cgcua/<dcat>/", category_groupedcat_update_all, name="category-gc-update-all"),
	#8
	path("csearch/", CatSearchView.as_view(), name="results-category"),
	#29
	path("load-c/", load_c, name="load-c"),

	#L1GROUP
	#9
    path("l1g/", L1GroupListView.as_view(), name="list-l1groups"),
	#22
    path("al1g/", L1GroupCreateView.as_view(), name="add-l1group"),
	#15
    path("ul1g/<pk>/", L1GroupUpdateView.as_view(), name="update-l1group"),

	#GROUPED CAT
	#19
    path("gc/", GroupedCatListView.as_view(), name="list-gc"),
	#12
    path("agc/", GroupedCatCreateView.as_view(), name="add-gc"),
	#20
    path("ugc/<pk>/", GroupedCatUpdateView.as_view(), name="update-gc"),
	#21
    path("dgc/<pk>/", GroupedCatDeleteView.as_view(), name="delete-gc"),
	#30
    path("load-gc/", load_gc, name="load-gc"),

	#PAYEE
	#13
	path('pay/<str:a>/<str:o>/', payees, name='list-payees'),
	#23
	path('apay/', PayeeCreateView.as_view(), name="add-payee"),
	#25
	path("upay/<pk>/", UpdatePayee.as_view(), name="update-payee"),
	#26
    path('payee/<int:pk>/delete/', PayeeDeleteView.as_view(), name='delete-payee'),
	#27
	path('payee/<int:pk>/make_inactive/', make_inactive, name='make-payee-inactive'),
	#14
	path("merge/<dpay>/", merge_payees, name="merge"),
	path("merge/", merge_payees, name="merge"),
	#17
	path('pcupdateall/<dpay>/', payee_category_update_all, name="payee-category-update-all"),
	path('pcupdateall/', payee_category_update_all, name="payee-category-update-all"),
	#10
    path("pgcua/<dpay>/", payee_groupedcat_update_all, name="payee-gc-update-all"),
	#18
	path('pau/', payee_account_update, name="payee-account-update"),
	#28
    path("search/", SearchResultsView.as_view(), name="results"),
	#24
	path("paydet/<pk>/", PayeeDetailView.as_view(), name="payee-detail"),

]
