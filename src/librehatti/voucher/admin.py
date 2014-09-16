from django.contrib import admin
from librehatti.voucher.models import *
from django.contrib.auth.admin import *
admin.autodiscover()


class FinancialSessionAdmin(admin.ModelAdmin):
    model = FinancialSession
    list_display = ['id']


class DistributionAdmin(admin.ModelAdmin):
    model = Distribution
    list_display = ['name']
    

class CategoryDistributionTypeAdmin(admin.ModelAdmin):
    model = CategoryDistributionType
    list_display = ['name']


admin.site.register(FinancialSession)
admin.site.register(Distribution)
admin.site.register(CategoryDistributionType)