from django.contrib import admin
from librehatti.bills.models import *
from django.contrib.auth.admin import *
from librehatti.bills.forms import ItemSelectForm
from librehatti.catalog.actions import mark_inactive, mark_active
from django.http import HttpResponse,HttpResponseRedirect
from librehatti.bills.forms import BuyerForm


import itertools
admin.autodiscover() 

"""
This class is used to add, edit or delete the details of item purchased.
"""
class QuotedItemInline(admin.StackedInline):
    model = QuotedItem
    form = ItemSelectForm
    fields = ['parent_category', 'sub_category','item','qty']
    extra = 10


"""
This class is used to add, edit or delete the details of items 
purchased but buyer has not confirmed the items purchased, this class
inherits the fields of PurchaseOrder derscribing the delivery address of
buyer , is_debit , total discount , tds and mode of payment
"""
class QuotedOrderAdmin(admin.ModelAdmin):
    form = BuyerForm
    exclude=('is_active',)
    list_display = ['id','buyer_name','delivery_address','date_time','is_active']
    inlines = [QuotedItemInline]
    model = QuotedOrder
    actions = [mark_active, mark_inactive] 
    list_filter = ['date_time']
    search_fields = ['id']
    list_per_page = 20 
    def buyer_name(self, instance):
        return "%s" % (instance.buyer.first_name + ' ' + instance.buyer.\
            last_name + ' ' + instance.buyer.customer.title)
    def response_add(self, request, obj, post_url_continue=None):
        request.session['old_post'] = request.POST
        request.session['quoted_order_id'] = obj.id
        return HttpResponseRedirect('/bills/quoted_order_of_session/')      

class NoteLineAdmin(admin.ModelAdmin):
    Model = NoteLine


admin.site.register(NoteLine,NoteLineAdmin)
admin.site.register(QuotedOrder, QuotedOrderAdmin)
