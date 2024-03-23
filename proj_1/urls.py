from django.urls import path

from .views import (
    index,
    fcflowListView,
    fcflowDetailView,
    fcflowCreateView,
    fcflowUpdateView,
    fcflowDeleteView,
    withholding,
)

app_name = "proj"

urlpatterns = [

    path("", index, name="index"),
    path("wh/", withholding, name="withholding"),
    path("list/", fcflowListView.as_view(), name="list"),
    path("create/", fcflowCreateView.as_view(), name="create"),
    path("<pk>/update/", fcflowUpdateView.as_view(), name="update"),
    path("<pk>/delete/", fcflowDeleteView.as_view(), name="delete"),
    path("<pk>/", fcflowDetailView.as_view(), name="detail"),

]