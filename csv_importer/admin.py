from django.contrib import admin
from .models import (
    Csv,
    Imported_Payee,
    Staged_Transaction,
)

class Imported_Payee_Admin(admin.ModelAdmin):
	list_display = [
		'payee',
		'imported_payee',
		'added',
	]

	list_filter = [
		'payee',
		'added',
	]

	date_hierarchy = "added"

@admin.action(description="Set Account to Venture")
def set_acct_venture(modeladmin, request, queryset):
    queryset.update(account=31)

@admin.action(description="Set Imported to True")
def set_imported_True(modeladmin, request, queryset):
    queryset.update(imported=True)

class Staged_Transaction_Admin(admin.ModelAdmin):

	list_display = [
		'tdate',
		'account',
		'imported_payee',
		'amount',
		'uploaded',
		'imported',
	]

	list_filter = [
		'tdate',
		'account',
		'uploaded',
		'imported',
	]
	date_hierarchy = "tdate"
	actions = [set_acct_venture, set_imported_True]
	ordering = ['tdate']


# Register your models here.
admin.site.register(Csv)
admin.site.register(Imported_Payee, Imported_Payee_Admin)
admin.site.register(Staged_Transaction, Staged_Transaction_Admin)