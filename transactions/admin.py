from django.contrib import admin

from .models import (
       Transaction,
       SubTransaction,
)

class SubTransactionInline(admin.StackedInline):
       model = SubTransaction
       extra = 0

class TransactionAdmin(admin.ModelAdmin):
        inlines = [SubTransactionInline]
        list_display=[
            'tid',
            'tdate',
            'account',
            'payee',
            'get_transaction_total',
            'match',
            'note',
        ]

        list_filter = [
		    'account',
		    'payee',
	    ]

# Register your models here.

admin.site.register(Transaction, TransactionAdmin)