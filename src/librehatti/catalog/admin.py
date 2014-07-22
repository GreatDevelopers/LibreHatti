from librehatti.catalog.models import *
from django.contrib import admin
from django.contrib.auth.admin import *


admin.autodiscover()
admin.site.register(Category)
admin.site.register(Attributes)
admin.site.register(Catalog)
admin.site.register(Surcharge)
admin.site.register(ModeOfPayment)

class CatalogInline(admin.TabularInline):
    model = Catalog
    fields = ['attribute', 'value']
    extra = 10


class ProductAdmin(admin.ModelAdmin):
    fields = ['name', 'category', 'price_per_unit', 'organisation']
    inlines = [CatalogInline] 


class PurchasedItemInline(admin.StackedInline):
    model = PurchasedItem
    fields = ['item', 'qty', ]
    extra = 10


class PurchaseOrderAdmin(admin.ModelAdmin):
    exclude=('is_suspense',)
    inlines = [PurchasedItemInline]
    model = PurchaseOrder
    def response_add(self, request, obj, post_url_continue=None):
        request.session['old_post'] = request.POST
        request.session['purchase_order_id'] = obj.id
        return HttpResponseRedirect('/suspense/add_distance/')


admin.site.register(PurchaseOrder, PurchaseOrderAdmin)
admin.site.register(Product, ProductAdmin) 
