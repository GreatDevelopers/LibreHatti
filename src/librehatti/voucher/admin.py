from django.contrib import admin
from librehatti.voucher.models import *
from django.contrib.auth.admin import *

from librehatti.voucher.forms import AssignDistributionForm

admin.autodiscover()


class FinancialSessionAdmin(admin.ModelAdmin):
    model = FinancialSession
    list_display = ['id','session_start_date','session_end_date']


class DistributionAdmin(admin.ModelAdmin):
    model = Distribution
    list_display = ['name','ratio']


class CategoryDistributionTypeAdmin(admin.ModelAdmin):
    form = AssignDistributionForm
    model = CategoryDistributionType
    list_display = ['category','parent_category','distribution']
    list_filter = ['category','parent_category']

class VoucherIdAdmin(admin.ModelAdmin):
	model = VoucherId
	list_display = ['id','voucher_no','session','ratio']

admin.site.register(VoucherId, VoucherIdAdmin)
admin.site.register(FinancialSession, FinancialSessionAdmin)
admin.site.register(Distribution, DistributionAdmin)
admin.site.register(CategoryDistributionType, CategoryDistributionTypeAdmin)