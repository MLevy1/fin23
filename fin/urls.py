from django.urls import path

from .views import (
	#MAIN
	#1 [master]
	main,

	#ACCOUNT
	#2 [master][main][accounts]
	accounts,
	#3 [master][main][accounts]
	AccountCreateView,
	#4 [accounts]
	UpdateAccount,

	#CATEGORY
	#5 [master][main]
	CatListView,
	#6 [master][main][categories]
	CatCreateView,
	#7 [categories]
	UpdateCategory,
	#8 [categories]
	CatSearchView,
	#29
	load_c,

	#l1GROUP
	#9 [master][main][categories]
	L1GroupListView,
	#22 [master][main][categories][l1]
	L1GroupCreateView,
	#15 [l1]
	L1GroupUpdateView,

	#GROUPED CAT
	#19 [master][main]
	GroupedCatListView,
	#12 [master][main][gc]
	GroupedCatCreateView,
	#20 [gc]
	GroupedCatUpdateView,
	#21 [gc]
	GroupedCatDeleteView,
	#30
	load_gc,

	#PAYEE
	#13 [master][main][payees]
	payees,
	#23 [master][main][payees]
	PayeeCreateView,
	#25 [payees]
	UpdatePayee,
	#26 [payees]
	PayeeDeleteView,
	#27 [payees]
	make_inactive,
	#28 [payees]
	SearchResultsView,
	#24 [tlist][trans_monthly]
	PayeeDetailView,
)

urlpatterns = [

	#MAIN
	#1 [master]
	path('', main, name='main'),

	#ACCOUNT
	#2 [master][main][accounts][mAccount-abs]
	path('act/<str:a>/', accounts, name='list-accounts'),
	#3 [master][main][accounts]
	path("aact/", AccountCreateView.as_view(), name="add-account"),
	#4 [accounts]
	path("uact/<pk>/", UpdateAccount.as_view(), name="update-account"),

	#CATEGORY
	#5 [master][main]
	path('cat/', CatListView.as_view(), name='list-categories'),
	#6 [master][main][categories][mCategory-abs]
	path("acat/", CatCreateView.as_view(), name="add-category"),
	#7 [categories]
	path("ucat/<pk>/", UpdateCategory.as_view(), name="update-category"),
	#8 [categories]
	path("csearch/", CatSearchView.as_view(), name="results-category"),
	#29
	path("load-c/", load_c, name="load-c"),

	#L1GROUP
	#9 [master][main][categories][ml1-abs]
    path("l1g/", L1GroupListView.as_view(), name="list-l1groups"),
	#22 [master][main][categories][l1]
    path("al1g/", L1GroupCreateView.as_view(), name="add-l1group"),
	#15 [l1]
    path("ul1g/<pk>/", L1GroupUpdateView.as_view(), name="update-l1group"),

	#GROUPED CAT
	#19 [master][main]
    path("gc/", GroupedCatListView.as_view(), name="list-gc"),
	#12 [master][main][gc][mGc-abs]
    path("agc/", GroupedCatCreateView.as_view(), name="add-gc"),
	#20 [gc]
    path("ugc/<pk>/", GroupedCatUpdateView.as_view(), name="update-gc"),
	#21 [gc]
    path("dgc/<pk>/", GroupedCatDeleteView.as_view(), name="delete-gc"),
	#30
    path("load-gc/", load_gc, name="load-gc"),

	#PAYEE
	#13 [master][main][payees]
	path('pay/<str:a>/<str:o>/', payees, name='list-payees'),
	#23 [master][main][payees][mPayee-abs]
	path('apay/', PayeeCreateView.as_view(), name="add-payee"),
	#25 [payees][detail]
	path("upay/<pk>/", UpdatePayee.as_view(), name="update-payee"),
	#26 [payees][detail]
    path('payee/<int:pk>/delete/', PayeeDeleteView.as_view(), name='delete-payee'),
	#27 [payees][detail]
	path('payee/<int:pk>/make_inactive/', make_inactive, name='make-payee-inactive'),
	#28 [payees]
    path("search/", SearchResultsView.as_view(), name="results"),
	#24 [tlist][trans_monthly]
	path("paydet/<pk>/", PayeeDetailView.as_view(), name="payee-detail"),

]
