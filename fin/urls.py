from django.urls import path
from . import views
from django.views.generic.dates import ArchiveIndexView
from .views import PayeeDetailView, L1GroupUpdateView, L1GroupListView, L1GroupCreateView, MonthlyCashFlow, BudgetItemDeleteView, BudgetItemUpdateView, BudgetItemCreateView, BudgetItemView, TransDeleteView, UpdateIssue, IssueCreateView, IssueListView, CatListView, UpdateCategory, UpdateAccount, SearchResultsView, testform, transactionMonthArchiveView, TransYearArchiveView, PayeeCreateView, AccountCreateView, CatCreateView, UpdatePayee, PayeeDeleteView, GroupedCatListView, GroupedCatCreateView, GroupedCatUpdateView, GroupedCatDeleteView
from .models import Trans

urlpatterns = [

	path('', views.main, name='main'),
	
	path('act/<str:a>/', views.accounts, name='list-accounts'),
	path("aact/", AccountCreateView.as_view(), name="add-account"),
	path("uact/<pk>/", UpdateAccount.as_view(), name="update-account"),
	
	path('cat/', CatListView.as_view(), name='list-categories'),
	path("acat/", CatCreateView.as_view(), name="add-category"),
	path("ucat/<pk>/", UpdateCategory.as_view(), name="update-category"),
	
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

       path("tlist/<str:acc>/<str:cat>/<str:gcat>/<str:pay>/<str:ord>/", views.tlist, name="tlist"),
       path("tlist/<str:acc>/<str:cat>/<str:gcat>/<str:pay>/<str:ord>/<str:gnull>", views.tlist, name="tlist"),
       path("tlist/<str:acc>/<str:cat>/<str:gcat>/<str:pay>/", views.tlist, name="tlist"),
	path("tlist/", views.tlist, name="tlist"),
       path('archive/', ArchiveIndexView.as_view(model=Trans, date_field="tdate", template_name="trans_years.html"), name='trans-years'),
	path('<int:year>/<int:month>/', transactionMonthArchiveView.as_view(month_format='%m'), name="trans-monthly"),
	path('<int:year>/', TransYearArchiveView.as_view(), name="trans-months"),
	path("atran/<dpay>/", views.atran, name="add-trans"),
	path("atran/", views.atran, name="add-trans"),
       path('pd/', views.ptran, name="pd-trans"),
	path("utran/<int:t_id>/", views.utran, name="update-trans"),
       path("utran_act/<int:t_id>/", views.utran_act, name="update-trans-act"),
	path('trans/<int:pk>/delete/', TransDeleteView.as_view(), name='delete-trans'),
	
	path("issues/", IssueListView.as_view(), name="view-issues"),
	path("aissue/", IssueCreateView.as_view(), name="add-issue"),
	path("uissue/<pk>/", UpdateIssue.as_view(), name="update-issue"),

	path("budgetitem/", BudgetItemView.as_view(), name="list-budgetitems"),
	path("abudgetitem/", BudgetItemCreateView.as_view(), name="add-budgetitem"),
	path("ubudgetitem/<pk>/", BudgetItemUpdateView.as_view(), name="update-budgetitem"),
	path('dbudgetitem/<pk>/', BudgetItemDeleteView.as_view(), name='delete-budgetitem'),

	path("move/", views.move, name="move"),

	path("budget/", views.budget, name="budget"),

	path("test/", testform.as_view(), name="test"),
	path("mrep/", MonthlyCashFlow.as_view(), name ="mrep"),

       path("g/", views.testg, name="g"),
]
