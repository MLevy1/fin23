from django.urls import (
	path,
)

from .views import (
    upload_file,
    upload_file_view,
)

app_name = 'csv'

urlpatterns = [
    path('', upload_file_view, name='upload-view'),
	path('upload/', upload_file, name='upload-file'),

]