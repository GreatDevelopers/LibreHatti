from django.db import models
from librehatti.catalog.models import PurchaseOrder
from librehatti.catalog.models import PurchasedItem
from librehatti.catalog.models import Category 
import datetime
 
class FinancialSession(models.Model):
<<<<<<< HEAD
    session_start_date = models.DateField()
    session_end_date = models.DateField()
=======
    session_start_date = models.DateField(verbose_name='_SESSION_START_DATE')
    session_end_date = models.DateField(verbose_name='_SESSION_END_DATE')
>>>>>>> upstream/dirty
    def __unicode__(self):
    	return "%s : %s" % (self.session_start_date, self.session_end_date)


class Distribution(models.Model):
	name = models.CharField(max_length=100)
	ratio = models.CharField(max_length=10)
<<<<<<< HEAD
	college_income = models.IntegerField(default = 15)
	admin_charges = models.IntegerField(default = 5)
=======
	college_income = models.IntegerField(default = 15, verbose_name='_COLLEGE_INCOME')
	admin_charges = models.IntegerField(default = 5, verbose_name='_ADMIN_CHARGES')
>>>>>>> upstream/dirty
	def __unicode__(self):
         return self.name


class VoucherId(models.Model):
<<<<<<< HEAD
    purchase_order = models.ForeignKey(PurchaseOrder)
    purchased_item = models.ForeignKey(PurchasedItem)
=======
    purchase_order = models.ForeignKey(PurchaseOrder, verbose_name='_PURCHASE_ORDER')
    purchased_item = models.ForeignKey(PurchasedItem, verbose_name='_PURCHASED_ITEM')
>>>>>>> upstream/dirty
    voucher_no = models.IntegerField()
    purchase_order_of_session = models.IntegerField()
    purchased_item_of_session = models.IntegerField()
    session = models.ForeignKey(FinancialSession)
    distribution = models.ForeignKey(Distribution)
    ratio = models.CharField(max_length=10)
    college_income = models.IntegerField()
    admin_charges = models.IntegerField()
    def __unicode__(self):
        return "%s" % (self.voucher_no)


class CategoryDistributionType(models.Model):
    parent_category = models.ForeignKey(Category, related_name='parent_category')
    category = models.ForeignKey(Category, related_name='category')
    distribution = models.ForeignKey(Distribution)
    def __unicode__(self):
        return self.category.name


class CalculateDistribution(models.Model):
    voucher_no = models.IntegerField()
    college_income_calculated = models.IntegerField()
    admin_charges_calculated = models.IntegerField()
    consultancy_asset = models.IntegerField()
    development_fund = models.IntegerField()
    total = models.IntegerField()
    session = models.ForeignKey(FinancialSession)
