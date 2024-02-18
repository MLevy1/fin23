from django.contrib import admin

# Register your models here.
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
              'payee',
              'match',
              'note',
              'oldCat',
              'oldPayee'
       ]

admin.site.register(Transaction, TransactionAdmin)
