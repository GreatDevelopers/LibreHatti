from django.contrib import admin
from librehatti.suspense.models import SuspenseOrder

admin.autodiscover()
admin.site.register(SuspenseOrder)
