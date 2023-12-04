from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import (
	Account, 
	Category, 
	Payee, 
	Trans, 
	BudgetItem, 
	L1Group, 
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

class GroupedCategoryInline(admin.StackedInline):
	model = GroupedCat
	extra = 0

class L1GroupAdmin(admin.ModelAdmin):
	inlines = [GroupedCategoryInline]
	list_display = [
		'l1group',
		'active',
		'aligned_category'
	]

class TransInline(admin.StackedInline):
	model = Trans
	extra = 0
	max_num = 25


class CategoryAdmin(admin.ModelAdmin):
	inlines = [TransInline]
	list_display = [
		'category',
		'active'
	]

admin.site.register(Account)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Payee, PayeeAdmin)
admin.site.register(Trans)
admin.site.register(BudgetItem)
admin.site.register(L1Group, L1GroupAdmin)
admin.site.register(GroupedCat)