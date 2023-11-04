from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Account, Category, Payee, Issue, Trans, BudgetItem, L1Group, Location, Job, GroupedCat

admin.site.register(Account)
admin.site.register(Category)
admin.site.register(Payee)
admin.site.register(Trans)
admin.site.register(Issue)
admin.site.register(BudgetItem)
admin.site.register(L1Group)
admin.site.register(Location)
admin.site.register(Job)
admin.site.register(GroupedCat)