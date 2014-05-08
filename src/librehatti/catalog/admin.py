from librehatti.catalog.models import *
from django.contrib import admin


admin.autodiscover()
admin.site.register(category)
admin.site.register(attributes)
admin.site.register(catalog)
admin.site.register(admin_organisations)
admin.site.register(address)
admin.site.register(organisation_type)
admin.site.register(purchase_order)
admin.site.register(purchased_item)

class CatalogInline(admin.TabularInline):
	model = catalog
	fields = ['attribute','value']
	extra = 10

class ProductAdmin(admin.ModelAdmin):
    fields = ['name','category','price','organisation']
    inlines = [CatalogInline]

admin.site.register(product, ProductAdmin) 

