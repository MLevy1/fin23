from django.contrib import admin

from .models import (
	Account,
	Category,
	Payee,
	L1Group,
	GroupedCat
)

from transactions.models import (
	Transaction
)

class GroupedCategoryInline(admin.StackedInline):
	model = GroupedCat
	list_display = [
		'l1group',
		'category'
	]
	readonly_fields = ['pk']
	extra = 0

class L1GroupAdmin(admin.ModelAdmin):
	inlines = [GroupedCategoryInline]
	list_display = [
		'l1group',
		'active'
	]


class TransInline(admin.StackedInline):
	model = Transaction
	extra = 0
	max_num = 25


class PayeeAdmin(admin.ModelAdmin):
	inlines = [TransInline]
	list_display=[
		'id',
		'payee',
		'active'
	]
	search_fields = ['payee']

class CategoryAdmin(admin.ModelAdmin):
	list_display = [
		'category',
		'active'
	]

admin.site.register(Account)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Payee, PayeeAdmin)
admin.site.register(L1Group, L1GroupAdmin)
admin.site.register(GroupedCat)