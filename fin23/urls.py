from django.contrib import admin

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
	TotalPerCategory,
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
	path('rep/', include('reports.urls')),
	path('login/', login_view),
	path('admin/', admin.site.urls),
	path('logout/', logout_view),
	path("budget/", budget, name="budget"),
	path("move/", move, name="move"),
	path("issues/", IssueListView.as_view(), name="view-issues"),
	path("aissue/", IssueCreateView.as_view(), name="add-issue"),
	path("uissue/<pk>/", UpdateIssue.as_view(), name="update-issue"),
       path("budgetitem/", BudgetItemView.as_view(), name="list-budgetitems"),
	path("abudgetitem/", BudgetItemCreateView.as_view(), name="add-budgetitem"),
	path("ubudgetitem/<pk>/", BudgetItemUpdateView.as_view(), name="update-budgetitem"),
	path('dbudgetitem/<pk>/', BudgetItemDeleteView.as_view(), name='delete-budgetitem'),

]
