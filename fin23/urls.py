from django.contrib import admin

from django.urls import (
	include,
	path
)

urlpatterns = [
	path('', include('fin.urls')),
    path('trans/', include('transactions.urls')),
    path('csv/', include('csvimp.urls')),
    path('issues/', include('issues.urls')),
    path('accounts/', include('accounts.urls')),
	path('admin/', admin.site.urls),
]
