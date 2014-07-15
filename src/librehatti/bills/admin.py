from django.contrib import admin
from librehatti.bills.models import *
#from django.contrib.auth.admin import *

class QuotedItemInline(admin.StackedInline):
    model = QuotedItem
    fields = ['quote_item', 'quote_qty', 'quote_discount']
    extra = 10

class QuotedOrderAdmin(admin.ModelAdmin):
    inlines = [QuotedItemInline]

admin.site.register(QuotedOrder, QuotedOrderAdmin)
admin.site.register(QuotedOrder)
admin.site.register(QuotedItem)
