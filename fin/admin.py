from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import (
	Account, 
	Category, 
	Payee, 
	Trans, 
	BudgetItem, 
	L1Group, 
	Location, 
	Job, 
	GroupedCat
)

class PayeeAdmin(admin.ModelAdmin):
       list_display=[
              'id',
              'payee',
              'slug',
              'active'
       ]
       search_fields = ['payee']

admin.site.register(Account)
admin.site.register(Category)
admin.site.register(Payee, PayeeAdmin)
admin.site.register(Trans)
admin.site.register(BudgetItem)
admin.site.register(L1Group)
admin.site.register(Location)
admin.site.register(Job)
admin.site.register(GroupedCat)