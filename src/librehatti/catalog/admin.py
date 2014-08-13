"""
%% admin.py %%
This file display usage information that admin requires to edit or add 
in database tables, classes in admin interface. This make the data entry
easy as one need to do it through MySQL server.
"""
from librehatti.catalog.models import *
from django.contrib import admin
from django.contrib.auth.admin import *

from librehatti.catalog.actions import mark_cancel

admin.autodiscover()
admin.site.register(Category)
admin.site.register(Attributes)
admin.site.register(Catalog)
admin.site.register(Surcharge)
admin.site.register(ModeOfPayment)

"""
This class is used to add, edit or delete the attribute and value of 
item along with inheriting the fields of Procduct class i.e. name, 
category, price_per_unit and organisation with which user deals
"""
class CatalogInline(admin.TabularInline):
    model = Catalog
    fields = ['attribute', 'value']
    extra = 10

"""
This class is used to add, edit or delete the details of product along  
with describing the organisation name and its type from where we are
purchasing or testing
"""
class ProductAdmin(admin.ModelAdmin):
    fields = ['name', 'category', 'price_per_unit', 'organisation']
    inlines = [CatalogInline] 

"""
This class is used to add, edit or delete the details of item purchased 
"""
class PurchasedItemInline(admin.StackedInline):
    model = PurchasedItem
    fields = ['item', 'qty', ]
    extra = 10

"""
This class is used to add, edit or delete the details of items 
purchased but buyer has not confirmed the items purchased, this class
inherits the fields of PurchaseOrder derscribing the delivery address of
buyer , is_debit , total discount , tds and mode of payment
"""
class PurchaseOrderAdmin(admin.ModelAdmin):
    exclude=('is_canceled',)
    list_display = ['id','buyer','delivery_address','date_time','is_canceled']
    inlines = [PurchasedItemInline]
    model = PurchaseOrder
    actions = [mark_cancel]
    list_filter = ['date_time']
    search_fields = ['id']
    list_per_page = 20 
    def response_add(self, request, obj, post_url_continue=None):
        request.session['old_post'] = request.POST
        request.session['purchase_order_id'] = obj.id
        return HttpResponseRedirect('/suspense/add_distance/')


admin.site.register(PurchaseOrder, PurchaseOrderAdmin)
admin.site.register(Product, ProductAdmin) 
