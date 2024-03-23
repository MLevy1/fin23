from django.urls import path

from .views import (
    index,
    tform,
)

app_name = "reports_1"

urlpatterns = [
    path("", index, name="main"),
    path("tf/<act>/", tform, name="tform"),
    path("tf/", tform, name="tform"),
]