from librehatti.catalog.models import *
from django.contrib import admin
from django.contrib.auth.admin import *
from librehatti.suspense.models import *
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

admin.autodiscover()
admin.site.register(Category)
admin.site.register(Attributes)
admin.site.register(Catalog)
#admin.site.register(SuspenseOrder)

class CatalogInline(admin.TabularInline):
    model = Catalog
    fields = ['attribute', 'value']
    extra = 10


class ProductAdmin(admin.ModelAdmin):
    fields = ['name', 'category', 'price', 'organisation']
    inlines = [CatalogInline] 


class PurchasedItemInline(admin.StackedInline):
    model = PurchasedItem
    fields = ['item', 'qty', 'discount']
    extra = 10


class PurchaseOrderAdmin(admin.ModelAdmin):
    exclude=('is_suspense',)
    inlines = [PurchasedItemInline]
    model = PurchaseOrder
    def response_add(self, request, obj, post_url_continue=None):
        if obj.is_suspense == True:
            return HttpResponseRedirect('/suspense/susp/')
        else:
            obj.save()
            return HttpResponseRedirect('/admin/catalog/purchaseorder/')


admin.site.register(PurchaseOrder, PurchaseOrderAdmin)
admin.site.register(Product, ProductAdmin) 

