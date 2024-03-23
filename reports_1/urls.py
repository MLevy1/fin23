from django.urls import path

from .views import (
    index,
    tform,
    treport,
)

app_name = "reports_1"

urlpatterns = [
    path("", index, name="main"),
    path("tf/<act>/", tform, name="tform"),
    path("tf/", tform, name="tform"),
    path("treport/<str:gcat>/<str:ord>/<str:acc>/<str:pay>/<str:cat>/<str:l1>/<mindate>/<maxdate>/", treport, name="treport"),
    path("treport/<str:acc>/<str:cat>/<str:gcat>/<str:pay>/<str:l1>/<str:ord>/", treport, name="treport"),
]