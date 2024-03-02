from django.contrib import admin

from .models import (
       Transaction,
       SubTransaction,
       Paycheck,
       PaycheckItems,

)

class PayCheckItemsInline(admin.StackedInline):
    model = PaycheckItems
    extra = 0


class PaycheckAdmin(admin.ModelAdmin):
    inlines = [PayCheckItemsInline]
    list_display = [
        'payee',
        'get_net_pay',
        'note',
        'active',
        ]
    save_as = True



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
admin.site.register(Paycheck, PaycheckAdmin)