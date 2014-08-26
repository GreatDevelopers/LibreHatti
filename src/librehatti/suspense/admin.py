from django.contrib import admin
from librehatti.suspense.models import SuspenseOrder, Staff, Department

admin.autodiscover()
admin.site.register(SuspenseOrder)
admin.site.register(Staff)
admin.site.register(Department)