from django.contrib import admin
from django.urls import include, path

from accounts.views import (
	login_view,
	logout_view
)

from projections.views import (
	budget
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

urlpatterns = [
	path('', include('fin.urls')),
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
]
