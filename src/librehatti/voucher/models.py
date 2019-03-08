from django.db import models

from librehatti.catalog.models import PurchaseOrder
from librehatti.catalog.models import PurchasedItem
from librehatti.catalog.models import Category 

import datetime

 
class FinancialSession(models.Model):
    """
    This class defines start date and end date for a financial session.
    """
    session_start_date = models.DateField()
    session_end_date = models.DateField()
    def __str__(self):
        return "%s : %s" % (self.session_start_date, self.session_end_date)


class Distribution(models.Model):
    """
    This class defines the ratios for distribution for material cost
    """
    name = models.CharField(max_length=100)
    ratio = models.CharField(max_length=10)
    college_income = models.IntegerField(default = 15)
    admin_charges = models.IntegerField(default = 5)
    def __str__(self):
         return self.name


class VoucherId(models.Model):
    """
    This class defines the voucher for purchase order according to the
    materials added in order
    """
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE,)
    purchased_item = models.ForeignKey(PurchasedItem, on_delete=models.CASCADE,)
    voucher_no = models.IntegerField()
    receipt_no_of_session = models.IntegerField(null=True)
    receipt_date = models.DateField(null=True)
    purchase_order_of_session = models.IntegerField()
    purchased_item_of_session = models.IntegerField()
    session = models.ForeignKey(FinancialSession, on_delete=models.CASCADE,)
    distribution = models.ForeignKey(Distribution, on_delete=models.CASCADE,)
    ratio = models.CharField(max_length=10)
    college_income = models.IntegerField()
    admin_charges = models.IntegerField()
    is_special = models.BooleanField(default=False)
    def __str__(self):
        return "%s" % (self.voucher_no)


class CategoryDistributionType(models.Model):
    """
    This class defines distributions for category and parent 
    category of product
    """
    parent_category = models.ForeignKey\
    (Category, related_name='parent_category', on_delete=models.CASCADE,)
    category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE,)
    distribution = models.ForeignKey(Distribution, on_delete=models.CASCADE,)
    def __str__(self):
        return self.category.name


class CalculateDistribution(models.Model):
    """
    This class defines the calculated distribution values of a voucher
    """
    voucher_no = models.IntegerField()
    college_income_calculated = models.IntegerField()
    admin_charges_calculated = models.IntegerField()
    consultancy_asset = models.IntegerField()
    development_fund = models.IntegerField()
    total = models.IntegerField()
    session = models.ForeignKey(FinancialSession, on_delete=models.CASCADE,)


class VoucherTotal(models.Model):
    """
    This class defines the total value of each voucher generated
    """
    voucher_no = models.IntegerField()
    session = models.ForeignKey(FinancialSession, on_delete=models.CASCADE,)
    total = models.IntegerField()
