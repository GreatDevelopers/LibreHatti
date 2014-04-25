from librehatti.catalog.models import *
from django.contrib import admin


admin.autodiscover()
admin.site.register(category)
admin.site.register(product)
admin.site.register(attributes)
admin.site.register(catalog)
admin.site.register(admin_organisations)
admin.site.register(address)
admin.site.register(organisation_type)