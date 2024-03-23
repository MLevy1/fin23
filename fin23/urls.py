from django.contrib import admin

from django.urls import (
	include,
	path
)

urlpatterns = [
	path('', include('fin.urls')),
    path('trans/', include('transactions.urls')),
    path('csv/', include('csv_importer.urls')),
    path('issues/', include('issues.urls')),
    path('accounts/', include('accounts.urls')),
    path('fixed/', include('fixed.urls')),
    path('tax/', include('tax.urls')),
    path('proj/', include('proj_1.urls')),
    path('reports/', include('reports_1.urls')),
	path('admin/', admin.site.urls),
]
