from django.contrib import admin

from librehatti.voucher.models import *

from django.contrib.auth.admin import *

from librehatti.voucher.forms import AssignDistributionForm

admin.autodiscover()


class FinancialSessionAdmin(admin.ModelAdmin):
    """
    This class is used to add, edit or delete a financial session
    """

    model = FinancialSession
    list_display = ["id", "session_start_date", "session_end_date"]


class DistributionAdmin(admin.ModelAdmin):
    """
    This class is used to add, edit or delete distribution in which the
    material cost is divided accordingly
    """

    model = Distribution
    list_display = ["name", "ratio"]


class CategoryDistributionTypeAdmin(admin.ModelAdmin):
    """
    This class is used to add, edit or delete distribution types of
    material
    """

    form = AssignDistributionForm
    model = CategoryDistributionType
    list_display = ["category", "parent_category", "distribution"]
    list_filter = ["category", "parent_category"]


class VoucherIdAdmin(admin.ModelAdmin):
    """
    This class is used to add, edit or delete the voucher which includes the
    distribution of material cost according to their distribution type
    """

    model = VoucherId
    list_display = ["id", "voucher_no", "session", "ratio"]


admin.site.register(VoucherId, VoucherIdAdmin)
admin.site.register(FinancialSession, FinancialSessionAdmin)
admin.site.register(Distribution, DistributionAdmin)
admin.site.register(CategoryDistributionType, CategoryDistributionTypeAdmin)
