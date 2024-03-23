from django.contrib import admin

from .models import (
       Flow,
       FlowItem,

)

class FlowItemInline(admin.StackedInline):
    model = FlowItem
    extra = 0

class FlowAdmin(admin.ModelAdmin):
    inlines = [FlowItemInline]
    list_display = [
        'payee',
        'account',
        'desc',
        'get_flow_total',
        'active',
        ]
    save_as = True

# Register your models here.

admin.site.register(Flow, FlowAdmin)