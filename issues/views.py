from django.shortcuts import render

from django.urls import reverse_lazy

from .models import (
	Issue, 
)

from django.views.generic import (
	ListView, 
	CreateView, 
	UpdateView, 
	DetailView,
	DeleteView
)

### VIEW ISSUES

class IssueListView(ListView):
	model = Issue
	template_name = "issues/issues.html"

### ADD ISSUE ###

class IssueCreateView(CreateView):
	model = Issue
	fields = ["issuename", "issuedesc", "priority", "issueopen"]
	template_name = "add.html"
	success_url = reverse_lazy('view-issues')

### UPDATE ISSUE ###

class UpdateIssue(UpdateView):
	model = Issue
	fields = ["issuename", "issuedesc", "priority", "issueopen"]
	template_name = "update.html"
	success_url = reverse_lazy('view-issues')