from django.urls import (
	path
)

from issues.views import (
	UpdateIssue,
	IssueCreateView,
	IssueListView,
)

app_name = 'issues'

urlpatterns = [
	path("", IssueListView.as_view(), name="view-issues"),
	path("add/", IssueCreateView.as_view(), name="add-issue"),
	path("update/<pk>/", UpdateIssue.as_view(), name="update-issue"),

]
