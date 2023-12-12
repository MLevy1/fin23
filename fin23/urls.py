from django.contrib import admin

from django.views.generic.dates import ArchiveIndexView

from django.urls import (
	include, 
	path
)

from accounts.views import (
	login_view,
	logout_view
)

from projections.views import (
	budget,
       BudgetItemDeleteView,
	BudgetItemUpdateView, 
	BudgetItemCreateView, 
	BudgetItemView, 
)

from moving.views import (
	move
)

from issues.views import (
	UpdateIssue, 
	IssueCreateView, 
	IssueListView, 
)

from reports.views import (
	testform,
	MonthlyCashFlow,
	ptran,
	testg,
)

from transactions.views import (
       TransDeleteView,
       TransYearArchiveView, 
       transactionMonthArchiveView,
       tlist,
       atran,
       utran,
       utran_act,
)

from transactions.models import Transaction, SubTransaction

urlpatterns = [
	path('', include('fin.urls')),
       path('trans/', include('transactions.urls')),
	path('recipes/', include('recipes.urls')),
	path('login/', login_view),
	path('admin/', admin.site.urls),
	path('logout/', logout_view),
	path("budget/", budget, name="budget"),
	path("move/", move, name="move"),
	path("issues/", IssueListView.as_view(), name="view-issues"),
	path("aissue/", IssueCreateView.as_view(), name="add-issue"),
	path("uissue/<pk>/", UpdateIssue.as_view(), name="update-issue"),
	path('pd/', ptran, name="pd-trans"),
	path("test/", testform.as_view(), name="test"),
	path("mrep/", MonthlyCashFlow.as_view(), name ="mrep"),
	path("g/", testg, name="g"),
       path("budgetitem/", BudgetItemView.as_view(), name="list-budgetitems"),
	path("abudgetitem/", BudgetItemCreateView.as_view(), name="add-budgetitem"),
	path("ubudgetitem/<pk>/", BudgetItemUpdateView.as_view(), name="update-budgetitem"),
	path('dbudgetitem/<pk>/', BudgetItemDeleteView.as_view(), name='delete-budgetitem'),

       path("tlist/<str:acc>/<str:cat>/<str:gcat>/<str:pay>/<str:ord>/", tlist, name="tlist"),

       path("tlist/<str:acc>/<str:cat>/<str:gcat>/<str:pay>/<str:ord>/<str:gnull>", tlist, name="tlist"),

       path("tlist/<str:acc>/<str:cat>/<str:gcat>/<str:pay>/", tlist, name="tlist"),

	path("tlist/", tlist, name="tlist"),
	
       path('archive/', ArchiveIndexView.as_view(model=Transaction, date_field="tdate", template_name="trans_years.html"), name='trans-years'),
	path('<int:year>/<int:month>/', transactionMonthArchiveView.as_view(month_format='%m'), name="trans-monthly"),
	path('<int:year>/', TransYearArchiveView.as_view(), name="trans-months"),
	path("atran/<dpay>/", atran, name="add-trans"),
	path("atran/", atran, name="add-trans"),

	path("utran/<int:t_id>/", utran, name="update-trans"),
       path("utran_act/<int:t_id>/", utran_act, name="update-trans-act"),

	path('trans/<int:pk>/delete/', TransDeleteView.as_view(), name='delete-trans'),

]
