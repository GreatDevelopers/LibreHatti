from django.contrib import admin
from librehatti.voucher.models import *
from django.contrib.auth.admin import *
admin.autodiscover()


class FinancialSessionAdmin(admin.ModelAdmin):
    model = FinancialSession
    list_display = ['id']
    

admin.site.register(FinancialSession)
